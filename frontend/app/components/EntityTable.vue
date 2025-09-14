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
  // Copy existing query, but remove search keys if empty
  const newQuery = { ...route.query };

  if (props.searchValue === '') {
    delete newQuery.search;
    delete newQuery.searchBy;
    delete newQuery.searchType;
  } else {
    newQuery.search = props.searchValue;
    newQuery.searchBy = props.searchBy;
    newQuery.searchType = props.searchType;
  }

  newQuery.page = String(pageNumber.value);
  newQuery.rows = String(rowsPerPage.value);
  newQuery.sortField = props.sortField;
  newQuery.sortOrder = props.sortOrder;

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

  const { data, error } = useEntities(props.entityType, options);

  if (data.value) {
    entitiesData.value = data.value.entities;
  }

  console.log(options);
};

const pageNumber = ref(5);
const reservedHeight = 300;
const rowsPerPage = ref(5);

const calculateRows = () => {
  const row = document.querySelector('table tbody tr');
  const rowHeight = row?.clientHeight ? row?.clientHeight + 1 : 64;

  const availableHeight = window.innerHeight - reservedHeight;

  rowsPerPage.value = Math.max(5, Math.floor(availableHeight / rowHeight));
};

onMounted(() => {
  calculateRows();

  watch(
    [
      () => rowsPerPage.value,
      () => pageNumber.value,
      () => props.searchValue,
      () => props.searchBy,
      () => props.searchType,
      () => props.sortField,
      () => props.sortOrder,
    ],
    () => {
      router.replace({
        query: updateUrl(),
      });

      loadEntities();
    },
    { immediate: true },
  );

  window.addEventListener('resize', calculateRows);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', calculateRows);
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
    <UPagination v-model:page="pageNumber" show-edges size="xl" :sibling-count="1" :total="100" />
  </div>
</template>
