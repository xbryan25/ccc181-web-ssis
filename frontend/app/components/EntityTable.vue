<script setup lang="ts">
import type { DefineComponent } from 'vue';
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
}>();

const router = useRouter();
const route = useRoute();

const isOpenEditDialog = ref(false);
const isOpenConfirmDeleteDialog = ref(false);
const selectedEntity = ref('');

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

const studentData = ref<Student[]>([
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
  {
    idNumber: '2023-0022',
    firstName: 'Bryan',
    lastName: 'Agan',
    yearLevel: '3rd',
    gender: 'Male',
    programCode: 'BSCS',
  },
]);

const programData = ref<Program[]>([
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
  {
    programCode: 'BSCS',
    programName: 'Bachelor of Science in Computer Science',
    collegeCode: 'CCS',
  },
]);

const collegeData = ref<College[]>([
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'COE',
    collegeName: 'College of Engineering',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
  {
    collegeCode: 'CCS',
    collegeName: 'College of Computer Studies',
  },
]);

const entitiesData = ref<Student[] | Program[] | College[]>([]);

const UButton = resolveComponent('UButton') as DefineComponent;
const UDropdownMenu = resolveComponent('UDropdownMenu') as DefineComponent;

const tableButtons = { UButton, UDropdownMenu };

const studentTableColumns = getStudentsTableColumns(
  {
    openEditDialog: (row: Student) => openConfirmEditDialog(row),
    openConfirmDeleteDialog: (row: Student) => openConfirmDeleteDialog(row),
  },
  tableButtons,
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
    newQuery.search = internalSearchValue.value;
    newQuery.searchBy = internalSearchBy.value;
    newQuery.searchType = internalSearchType.value;
  }

  return newQuery;
};

const loadEntities = () => {
  const options = {
    rowsPerPage: rowsPerPage.value,
    pageNumber: pageNumber.value,
    searchValue: props.searchValue,
    searchBy: props.searchBy,
    searchType: props.searchType,
    sortField: props.sortField,
    sortOrder: props.sortOrder,
  };

  // const { data, error } = useEntities(props.entityType, options);

  // if (data.value) {
  //   entitiesData.value = data.value.entities;
  // }

  console.log(options);
};

const totalPages = ref(1);
const pageNumber = ref(1);
const reservedHeight = 300;
const rowsPerPage = ref(0);

const updatePagination = () => {
  calculateRows();
  getMaxPages();
};

const calculateRows = () => {
  const row = document.querySelector('table tbody tr');
  const rowHeight = row?.clientHeight ? row?.clientHeight + 1 : 64;

  const availableHeight = window.innerHeight - reservedHeight;

  rowsPerPage.value = Math.max(5, Math.floor(availableHeight / rowHeight));
};

const getMaxPages = () => {
  const options = {
    searchValue: props.searchValue,
    searchBy: props.searchBy,
    searchType: props.searchType,
  };

  totalPages.value = 5;

  // const { data, error } = useEntitiesCount(props.entityType, options);

  // if (!error.value && data.value) {
  //   totalPages.value = Math.ceil(data.value.entitiesCount / rowsPerPage.value)
  // }

  if (pageNumber.value > totalPages.value) {
    pageNumber.value = totalPages.value;
  } else if (pageNumber.value < 1) {
    pageNumber.value = 1;
  }
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
);

// These watches 'watch' any changes from [entity].vue

watch(
  () => props.searchValue,
  (newValue) => {
    internalSearchValue.value = newValue;
    emit('update:searchValue', newValue);
  },
);

watch(
  () => props.searchBy,
  (newValue) => {
    internalSearchBy.value = newValue;
    emit('update:searchBy', newValue);
  },
);

watch(
  () => props.searchType,
  (newValue) => {
    internalSearchType.value = newValue;
    emit('update:searchType', newValue);
  },
);

watch(
  () => props.sortField,
  (newValue) => {
    internalSortField.value = newValue;
    emit('update:sortField', newValue);
  },
);

watch(
  () => props.sortOrder,
  (newValue) => {
    internalSortOrder.value = newValue;
    emit('update:sortOrder', newValue);
  },
);

onMounted(() => {
  pageNumber.value = Number(route.query.page) || pageNumber.value;

  internalSearchValue.value = String(route.query.search || internalSearchValue.value);
  internalSearchBy.value = String(route.query.searchBy || internalSearchBy.value);
  internalSearchType.value = String(route.query.searchType || internalSearchType.value);
  internalSortField.value = String(route.query.sortField || internalSortField.value);
  internalSortOrder.value = String(route.query.sortOrder || internalSortOrder.value);

  updatePagination();

  // This watch function 'watches' any changes in table filters and pagination, doesn't include parent changes
  watch(
    [
      () => pageNumber.value,
      () => internalSearchValue.value,
      () => internalSearchBy.value,
      () => internalSearchType.value,
      () => internalSortField.value,
      () => internalSortOrder.value,
    ],
    () => {
      router.replace({
        query: updateUrl(),
      });

      loadEntities();
    },
    { immediate: true },
  );

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
  />

  <ConfirmDeleteEntityDialog
    v-model:is-open="isOpenConfirmDeleteDialog"
    class="ml-auto hidden"
    :entity-type="props.entityType"
    :selected-entity="selectedEntity"
  />

  <UTable
    v-if="entityType === 'students'"
    loading
    loading-color="primary"
    loading-animation="carousel"
    :data="studentData.slice(0, rowsPerPage)"
    :columns="studentTableColumns"
    class="flex-1"
  />

  <UTable
    v-if="entityType === 'programs'"
    loading
    loading-color="primary"
    loading-animation="carousel"
    :data="programData.slice(0, rowsPerPage)"
    :columns="programsTableColumns"
    class="flex-1"
  />

  <UTable
    v-if="entityType === 'colleges'"
    loading
    loading-color="primary"
    loading-animation="carousel"
    :data="collegeData.slice(0, rowsPerPage)"
    :columns="collegesTableColumns"
    class="flex-1"
  />

  <div class="flex justify-center">
    <UPagination
      v-model:page="pageNumber"
      :items-per-page="rowsPerPage"
      show-edges
      size="xl"
      :sibling-count="1"
      :total="30"
    />
  </div>
</template>
