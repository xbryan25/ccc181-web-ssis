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
  rowsPerPage: number;
  createEntitySubmitRef: boolean;
  toggleAllCounter: number;
  externalCheckboxValue: boolean | 'indeterminate';
  isOpenConfirmDeleteDialogMultipleRowsCounter: number;
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

const entitiesData = ref<Student[] | Program[] | College[]>([]);

const UCheckbox = resolveComponent('UCheckbox') as DefineComponent;
const UButton = resolveComponent('UButton') as DefineComponent;
const UDropdownMenu = resolveComponent('UDropdownMenu') as DefineComponent;
const UAvatar = resolveComponent('UAvatar') as DefineComponent;

const tableButtons = { UCheckbox, UButton, UDropdownMenu };

const selectedRows = ref<Set<string>>(new Set());
const rowsToBeDeleted = ref<Set<string>>(new Set());

const isLoading = ref(true);

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
  (e: 'update:selectedRows' | 'update:loadedRowsPerPage', val: number): void;
  (e: 'update:isLoading', value: boolean): void;
}>();

const openConfirmDeleteDialogSingleRow = (row: Student | Program | College) => {
  isOpenConfirmDeleteDialog.value = true;

  if (props.entityType === 'students') {
    rowsToBeDeleted.value = new Set<string>([(row as Student).idNumber]);
  } else if (props.entityType === 'programs') {
    rowsToBeDeleted.value = new Set<string>([(row as Program).programCode]);
  } else {
    rowsToBeDeleted.value = new Set<string>([(row as College).collegeCode]);
  }
};

const openConfirmDeleteDialog = () => {
  isOpenConfirmDeleteDialog.value = true;

  rowsToBeDeleted.value = new Set(selectedRows.value);
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

const showAvatar = (avatarUrl: string) => {
  showImageModal.value = true;

  currentAvatarUrlToDisplay.value = avatarUrl ? avatarUrl : 'images/noAvatar.jpg';
};

function getId(r: Student | Program | College): string {
  if ('idNumber' in r) return r.idNumber;
  if ('programCode' in r) return r.programCode;
  if ('collegeCode' in r) return r.collegeCode;
  return '';
}

// Handler for external checkbox
function toggleAll(value: boolean | 'indeterminate') {
  const val = value === 'indeterminate' ? true : value;
  if (val) selectedRows.value = new Set<string>(entitiesData.value.map((r) => getId(r)));
  else selectedRows.value = new Set();

  emit('update:selectedRows', selectedRows.value.size);
}

// Row checkbox toggle
function toggleRow(id: string, value: boolean) {
  const newSet = new Set(selectedRows.value);
  if (value) newSet.add(id);
  else newSet.delete(id);
  selectedRows.value = newSet;

  emit('update:selectedRows', selectedRows.value.size);
}

const studentTableColumns = getStudentsTableColumns(
  {
    openEditDialog: (row: Student) => openConfirmEditDialog(row),
    openConfirmDeleteDialog: (row: Student) => openConfirmDeleteDialogSingleRow(row),
  },
  tableButtons,
  UAvatar,
  showAvatar,
  isLoading,
  selectedRows,
  toggleRow,
);

const programsTableColumns = getProgramsTableColumns(
  {
    openEditDialog: (row: Program) => openConfirmEditDialog(row),
    openConfirmDeleteDialog: (row: Program) => openConfirmDeleteDialogSingleRow(row),
  },
  tableButtons,
  isLoading,
  selectedRows,
  toggleRow,
);

const collegesTableColumns = getCollegesTableColumns(
  {
    openEditDialog: (row: College) => openConfirmEditDialog(row),
    openConfirmDeleteDialog: (row: College) => openConfirmDeleteDialogSingleRow(row),
  },
  tableButtons,
  isLoading,
  selectedRows,
  toggleRow,
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
  emit('update:isLoading', isLoading.value);

  emit('update:loadedRowsPerPage', entitiesData.value.length);
};

const debouncedLoadEntities = useDebounceFn(async () => {
  isLoading.value = true;
  emit('update:isLoading', isLoading.value);

  await loadEntities();

  selectedRows.value = new Set();

  emit('update:selectedRows', 0);
}, 700); // 700ms debounce

const totalEntityCount = ref(0);
const pageNumber = ref(1);
const delayedPageNumber = ref(1);

const rowsPerPage = computed(() => props.rowsPerPage);
const delayedRowsPerPage = ref(10);

const updatePagination = async () => {
  await debouncedGetTotalEntityCount();
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
      emit('update:isLoading', isLoading.value);

      debouncedLoadEntities();
      debouncedGetTotalEntityCount();
      emit('disableCreateEntitySubmit');
    }
  },
);

watch(
  () => props.toggleAllCounter,
  () => {
    const val =
      props.externalCheckboxValue === 'indeterminate' ? true : props.externalCheckboxValue;
    toggleAll(val);
  },
);

watch(isLoading, (newVal) => {
  if (!newVal) {
    delayedPageNumber.value = pageNumber.value;
    delayedRowsPerPage.value = rowsPerPage.value;
  }
});

watch(
  () => props.isOpenConfirmDeleteDialogMultipleRowsCounter,
  () => openConfirmDeleteDialog(),
);

onMounted(async () => {
  pageNumber.value = Number(route.query.page) || pageNumber.value;

  internalSearchValue.value = String(route.query.searchValue || internalSearchValue.value);
  internalSearchBy.value = String(route.query.searchBy || internalSearchBy.value);
  internalSearchType.value = String(route.query.searchType || internalSearchType.value);
  internalSortField.value = String(route.query.sortField || internalSortField.value);
  internalSortOrder.value = String(route.query.sortOrder || internalSortOrder.value);

  await updatePagination();

  validateUrlInput();

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
        emit('update:isLoading', isLoading.value);
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
      emit('update:isLoading', isLoading);
      debouncedLoadEntities();
      debouncedGetTotalEntityCount();
    "
  />

  <ConfirmDeleteEntityDialog
    v-model:is-open="isOpenConfirmDeleteDialog"
    class="ml-auto hidden"
    :entity-type="props.entityType"
    :rows-to-be-deleted="rowsToBeDeleted"
    @on-delete="
      isLoading = true;
      emit('update:isLoading', isLoading);
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

  <div v-if="entitiesData.length > 0" class="grid grid-cols-3 items-center mb-5">
    <div v-if="entitiesData.length == 1" class="text-sm text-muted pl-3">
      {{ delayedRowsPerPage * (delayedPageNumber - 1) + 1 }} of {{ totalEntityCount }}.
    </div>
    <div v-else class="text-sm text-muted pl-3">
      {{ delayedRowsPerPage * (delayedPageNumber - 1) + 1 }}-{{
        delayedRowsPerPage * delayedPageNumber > totalEntityCount
          ? totalEntityCount
          : delayedRowsPerPage * delayedPageNumber
      }}
      of {{ totalEntityCount }}.
    </div>
    <UPagination
      v-model:page="pageNumber"
      :items-per-page="rowsPerPage"
      show-edges
      size="xl"
      :sibling-count="0"
      :total="totalEntityCount"
      class="flex justify-center"
    />
  </div>

  <UModal v-model:open="showImageModal" :ui="{ content: 'max-w-100' }">
    <template #content>
      <NuxtImg
        :src="currentAvatarUrlToDisplay"
        alt="Avatar"
        class="max-w-100 max-h-100 object-contain"
      />
    </template>
  </UModal>
</template>
