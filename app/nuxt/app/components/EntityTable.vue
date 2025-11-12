<script setup lang="ts">
import type { DefineComponent } from 'vue';
import { useDebounceFn } from '@vueuse/core';

import type { Student, Program, College } from '~/types';

import {
  getStudentsTableColumns,
  getProgramsTableColumns,
  getCollegesTableColumns,
} from '~/columns';

const props = defineProps<{
  entityType: string;
  searchValue: string;
  searchBy: string;
  searchType: string;
  sortField: string;
  sortOrder: string;
  createEntitySubmitRef: boolean;
}>();

const router = useRouter();
const route = useRoute();

const isOpenEditDialog = ref(false);
const isOpenConfirmDeleteDialog = ref(false);
const selectedEntity = ref('');

const showImageModal = ref(false);
const currentAvatarUrlToDisplay = ref('');

const internalSearchValue = ref(props.searchValue);
const internalSearchBy = ref(props.searchBy);
const internalSearchType = ref(props.searchType);
const internalSortField = ref(props.sortField);
const internalSortOrder = ref(props.sortOrder);

const emit = defineEmits<{
  (
    e:
      | 'update:searchValue'
      | 'update:searchBy'
      | 'update:searchType'
      | 'update:sortField'
      | 'update:sortOrder',
    value: string,
  ): void;
  (e: 'disableCreateEntitySubmit'): void;
}>();

const openConfirmDeleteDialog = (row: Student | Program | College) => {
  isOpenConfirmDeleteDialog.value = true;

  if (props.entityType === 'students') {
    selectedEntity.value = (row as Student).idNumber;
  } else if (props.entityType === 'programs') {
    selectedEntity.value = (row as Program).programCode;
  } else {
    selectedEntity.value = (row as College).collegeCode;
  }
};

const openConfirmEditDialog = (row: Student | Program | College) => {
  isOpenEditDialog.value = true;

  if (props.entityType === 'students') {
    selectedEntity.value = (row as Student).idNumber;
  } else if (props.entityType === 'programs') {
    selectedEntity.value = (row as Program).programCode;
  } else {
    selectedEntity.value = (row as College).collegeCode;
  }
};

const entitiesData = ref<Student[] | Program[] | College[]>([]);

const UButton = resolveComponent('UButton') as DefineComponent;
const UDropdownMenu = resolveComponent('UDropdownMenu') as DefineComponent;
const UAvatar = resolveComponent('UAvatar') as DefineComponent;

const tableButtons = { UButton, UDropdownMenu };

const showAvatar = (avatarUrl: string) => {
  showImageModal.value = true;

  currentAvatarUrlToDisplay.value = avatarUrl;
};

const studentTableColumns = getStudentsTableColumns(
  {
    openEditDialog: (row: Student) => openConfirmEditDialog(row),
    openConfirmDeleteDialog: (row: Student) => openConfirmDeleteDialog(row),
  },
  tableButtons,
  UAvatar,
  showAvatar,
);

const programsTableColumns = getProgramsTableColumns(
  {
    openEditDialog: (row: Program) => openConfirmEditDialog(row),
    openConfirmDeleteDialog: (row: Program) => openConfirmDeleteDialog(row),
  },
  tableButtons,
);

const collegesTableColumns = getCollegesTableColumns(
  {
    openEditDialog: (row: College) => openConfirmEditDialog(row),
    openConfirmDeleteDialog: (row: College) => openConfirmDeleteDialog(row),
  },
  tableButtons,
);

const updateUrl = () => {
  const newQuery: Record<string, string> = {};

  newQuery.page = String(pageNumber.value);
  newQuery.sortField = internalSortField.value;
  newQuery.sortOrder = internalSortOrder.value;

  if (internalSearchValue.value !== '') {
    newQuery.searchValue = internalSearchValue.value;
    newQuery.searchBy = internalSearchBy.value;
    newQuery.searchType = internalSearchType.value;
  }

  return newQuery;
};

const isLoading = ref(true);

const loadEntities = async () => {
  // isLoading.value = true;

  const options = {
    rowsPerPage: rowsPerPage.value,
    pageNumber: pageNumber.value,
    searchValue: props.searchValue,
    searchBy: props.searchBy,
    searchType: props.searchType,
    sortField: props.sortField,
    sortOrder: props.sortOrder,
  };

  const data = await useEntities(props.entityType, options);

  entitiesData.value = data.entities;

  isLoading.value = false;
};

const debouncedLoadEntities = useDebounceFn(async () => {
  isLoading.value = true;

  await loadEntities();
}, 700); // 700ms debounce

const totalEntityCount = ref(0);
const pageNumber = ref(1);
const reservedHeight = 300;
const rowsPerPage = ref(0);

const updatePagination = () => {
  calculateRows();
  debouncedGetTotalEntityCount();
};

const calculateRows = () => {
  const row = document.querySelector('table tbody tr');
  const rowHeight = row?.clientHeight ? row?.clientHeight - 1 : 63;

  const availableHeight = window.innerHeight - reservedHeight;

  rowsPerPage.value = Math.max(5, Math.floor(availableHeight / rowHeight));
};

const getTotalEntityCount = async () => {
  const options = {
    searchValue: props.searchValue,
    searchBy: props.searchBy,
    searchType: props.searchType,
  };

  const { totalCount }: { totalCount: number } = await useEntitiesCount(props.entityType, options);

  totalEntityCount.value = totalCount;
};

const debouncedGetTotalEntityCount = useDebounceFn(async () => {
  await getTotalEntityCount();

  checkIfBeyondPageLimit();
}, 200); // 700ms debounce

const checkIfBeyondPageLimit = () => {
  const totalPages = Math.ceil(totalEntityCount.value / rowsPerPage.value) || 1;

  // If current page exceeds total pages, clamp it down
  if (pageNumber.value > totalPages) {
    pageNumber.value = totalPages;
  }

  // If there are no records, reset to page 1
  if (totalEntityCount.value === 0) {
    pageNumber.value = 1;
  }
};

const validateUrlInput = () => {
  const totalPages = Math.ceil(totalEntityCount.value / rowsPerPage.value);

  const allowedStudentFields = [
    'ID Number',
    'First Name',
    'Last Name',
    'Year Level',
    'Gender',
    'Program Code',
  ];

  const allowedProgramFields = ['Program Code', 'Program Name', 'College Code'];

  const allowedCollegeFields = ['College Code', 'College Name'];

  const allowedSearchType = ['Starts With', 'Contains', 'Ends With'];

  const allowedSortOrder = ['Ascending', 'Descending'];

  if (pageNumber.value > totalPages) {
    pageNumber.value = totalPages;
  } else if (pageNumber.value < 1) {
    pageNumber.value = 1;
  }

  if (props.entityType === 'students') {
    internalSortField.value = allowedStudentFields.includes(internalSortField.value)
      ? internalSortField.value
      : 'ID Number';
  } else if (props.entityType === 'programs') {
    internalSortField.value = allowedProgramFields.includes(internalSortField.value)
      ? internalSortField.value
      : 'Program Code';
  } else if (props.entityType === 'colleges') {
    internalSortField.value = allowedCollegeFields.includes(internalSortField.value)
      ? internalSortField.value
      : 'College Code';
  }

  internalSortOrder.value = allowedSortOrder.includes(internalSortOrder.value)
    ? internalSortOrder.value
    : 'Ascending';

  if (props.entityType === 'students') {
    internalSearchBy.value = allowedStudentFields.includes(internalSearchBy.value)
      ? internalSearchBy.value
      : 'ID Number';
  } else if (props.entityType === 'programs') {
    internalSearchBy.value = allowedProgramFields.includes(internalSearchBy.value)
      ? internalSearchBy.value
      : 'Program Code';
  } else if (props.entityType === 'colleges') {
    internalSearchBy.value = allowedCollegeFields.includes(internalSearchBy.value)
      ? internalSearchBy.value
      : 'College Code';
  }

  internalSearchType.value = allowedSearchType.includes(internalSearchType.value)
    ? internalSearchType.value
    : 'Starts With';
};

// This watch function emits changes to [entity.vue]

watch(
  [internalSearchValue, internalSearchBy, internalSearchType, internalSortField, internalSortOrder],
  ([newSearchValue, newSearchBy, newSearchType, newSortField, newSortOrder]) => {
    emit('update:searchValue', newSearchValue);
    emit('update:searchBy', newSearchBy);
    emit('update:searchType', newSearchType);
    emit('update:sortField', newSortField);
    emit('update:sortOrder', newSortOrder);
  },
  { immediate: true },
);

// These watches 'watch' any changes from [entity].vue and update internal state

watch(
  () => props.searchValue,
  (newValue) => {
    internalSearchValue.value = newValue;
  },
);

watch(
  () => props.searchBy,
  (newValue) => {
    internalSearchBy.value = newValue;
  },
);

watch(
  () => props.searchType,
  (newValue) => {
    internalSearchType.value = newValue;
  },
);

watch(
  () => props.sortField,
  (newValue) => {
    internalSortField.value = newValue;
  },
);

watch(
  () => props.sortOrder,
  (newValue) => {
    internalSortOrder.value = newValue;
  },
);

watch(
  () => props.createEntitySubmitRef,
  (newVal) => {
    if (newVal) {
      isLoading.value = true;
      debouncedLoadEntities();
      debouncedGetTotalEntityCount();
      emit('disableCreateEntitySubmit');
    }
  },
);

onMounted(() => {
  pageNumber.value = Number(route.query.page) || pageNumber.value;

  internalSearchValue.value = String(route.query.searchValue || internalSearchValue.value);
  internalSearchBy.value = String(route.query.searchBy || internalSearchBy.value);
  internalSearchType.value = String(route.query.searchType || internalSearchType.value);
  internalSortField.value = String(route.query.sortField || internalSortField.value);
  internalSortOrder.value = String(route.query.sortOrder || internalSortOrder.value);

  validateUrlInput();

  updatePagination();

  // This watch function 'watches' any changes in table filters and pagination, doesn't include parent changes
  // nextTick ensures that watcher setup will be delayed after validation is done
  nextTick(() => {
    watch(
      [
        () => rowsPerPage.value,
        () => pageNumber.value,
        () => internalSearchValue.value,
        () => internalSearchBy.value,
        () => internalSearchType.value,
        () => internalSortField.value,
        () => internalSortOrder.value,
      ],
      () => {
        router.replace({ query: updateUrl() });
        isLoading.value = true;
        debouncedLoadEntities();
        debouncedGetTotalEntityCount();
      },
      { immediate: true },
    );
  });

  window.addEventListener('resize', updatePagination);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updatePagination);
});
</script>

<template>
  <AddEditEntityDialog
    v-model:is-open="isOpenEditDialog"
    class="ml-auto hidden"
    :entity-type="props.entityType"
    :dialog-type="'edit'"
    :selected-entity="selectedEntity"
    @on-submit="
      isLoading = true;
      debouncedLoadEntities();
      debouncedGetTotalEntityCount();
    "
  />

  <ConfirmDeleteEntityDialog
    v-model:is-open="isOpenConfirmDeleteDialog"
    class="ml-auto hidden"
    :entity-type="props.entityType"
    :selected-entity="selectedEntity"
    @on-delete="
      isLoading = true;
      debouncedLoadEntities();
      debouncedGetTotalEntityCount();
    "
  />

  <UTable
    v-if="entityType === 'students'"
    :loading="isLoading"
    loading-color="primary"
    loading-animation="carousel"
    :data="(entitiesData as Student[]).slice(0, rowsPerPage)"
    :columns="studentTableColumns"
    class="flex-1"
  />

  <UTable
    v-if="entityType === 'programs'"
    :loading="isLoading"
    loading-color="primary"
    loading-animation="carousel"
    :data="(entitiesData as Program[]).slice(0, rowsPerPage)"
    :columns="programsTableColumns"
    class="flex-1"
  />

  <UTable
    v-if="entityType === 'colleges'"
    :loading="isLoading"
    loading-color="primary"
    loading-animation="carousel"
    :data="(entitiesData as College[]).slice(0, rowsPerPage)"
    :columns="collegesTableColumns"
    class="flex-1 overflow-y-hidden"
  />

  <div class="flex justify-center">
    <UPagination
      v-model:page="pageNumber"
      :items-per-page="rowsPerPage"
      show-edges
      size="xl"
      :sibling-count="0"
      :total="totalEntityCount"
    />
  </div>

  <UModal v-model:open="showImageModal">
    <template #content>
      <NuxtImg
        :src="currentAvatarUrlToDisplay"
        alt="Avatar"
        class="max-w-full max-h-200 object-contain"
      />
    </template>
  </UModal>
</template>
