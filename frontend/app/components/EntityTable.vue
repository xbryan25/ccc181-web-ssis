<script setup lang="ts">
import type { TableColumn } from "@nuxt/ui";
import type { Row } from "@tanstack/vue-table";

const props = defineProps<{
  entityType: string;
}>();

type Student = {
  idNumber: string;
  firstName: string;
  lastName: string;
  yearLevel: "1st" | "2nd" | "3rd" | "4th" | "4th+";
  gender: "Male" | "Female" | "Others" | "Prefer not to say";
  programCode: string;
};

type Program = {
  programCode: string;
  programName: string;
  collegeCode: string;
};

type College = {
  collegeCode: string;
  collegeName: string;
};

const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const isOpenEditDialog = ref(false);
const isOpenConfirmDeleteDialog = ref(false);
const selectedEntity = ref("");

const openEditDialog = () => {
  isOpenEditDialog.value = true;
};

const openConfirmDeleteDialog = (row: Student | Program | College) => {
  isOpenConfirmDeleteDialog.value = true;

  if (props.entityType === "students") {
    selectedEntity.value = (row as Student).idNumber;
  } else if (props.entityType === "programs") {
    selectedEntity.value = (row as Program).programCode;
  } else {
    selectedEntity.value = (row as College).collegeCode;
  }
};

const studentData = ref<Student[]>([
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
  {
    idNumber: "2023-0022",
    firstName: "Bryan",
    lastName: "Agan",
    yearLevel: "3rd",
    gender: "Male",
    programCode: "BSCS",
  },
]);

const programData = ref<Program[]>([
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
  {
    programCode: "BSCS",
    programName: "Bachelor of Science in Computer Science",
    collegeCode: "CCS",
  },
]);

const collegeData = ref<College[]>([
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "COE",
    collegeName: "College of Engineering",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
  {
    collegeCode: "CCS",
    collegeName: "College of Computer Studies",
  },
]);

const studentColumns: TableColumn<Student>[] = [
  {
    accessorKey: "idNumber",
    header: "ID Number",
    meta: {
      class: {
        th: "w-28",
        td: "w-28 text-md",
      },
    },
  },
  {
    accessorKey: "firstName",
    header: "First Name",
    meta: {
      class: {
        td: "text-md",
      },
    },
  },
  {
    accessorKey: "lastName",
    header: "Last Name",
    meta: {
      class: {
        td: "text-md",
      },
    },
  },
  {
    accessorKey: "yearLevel",
    header: "Year Level",
    meta: {
      class: {
        th: "w-24",
        td: "w-24 text-md",
      },
    },
  },
  {
    accessorKey: "gender",
    header: "Gender",
    meta: {
      class: {
        th: "w-24",
        td: "w-24 text-md",
      },
    },
  },
  {
    accessorKey: "programCode",
    header: "Program Code",
    meta: {
      class: {
        th: "w-42",
        td: "w-42 text-md",
      },
    },
  },
  {
    id: "actions",
    cell: ({ row }) => {
      return h(
        "div",
        h(
          UDropdownMenu,
          {
            content: {
              align: "end",
            },
            items: getRowItems(row),
            "aria-label": "Actions dropdown",
          },
          () =>
            h(UButton, {
              icon: "i-lucide-ellipsis-vertical",
              color: "neutral",
              variant: "ghost",
              class: "ml-auto",
              "aria-label": "Actions dropdown",
            })
        )
      );
    },
    meta: {
      class: {
        th: "w-16",
        td: "w-16",
      },
    },
  },
];

const programColumns: TableColumn<Program>[] = [
  {
    accessorKey: "programCode",
    header: "Program Code",
    meta: {
      class: {
        th: "w-42",
        td: "w-42 text-md",
      },
    },
  },
  {
    accessorKey: "programName",
    header: "Program Name",
    meta: {
      class: {
        td: "text-md",
      },
    },
  },
  {
    accessorKey: "collegeCode",
    header: "College Code",
    meta: {
      class: {
        th: "w-42",
        td: "w-42 text-md",
      },
    },
  },
  {
    id: "actions",
    cell: ({ row }) => {
      return h(
        "div",
        h(
          UDropdownMenu,
          {
            content: {
              align: "end",
            },
            items: getRowItems(row),
            "aria-label": "Actions dropdown",
          },
          () =>
            h(UButton, {
              icon: "i-lucide-ellipsis-vertical",
              color: "neutral",
              variant: "ghost",
              class: "ml-auto",
              "aria-label": "Actions dropdown",
            })
        )
      );
    },
    meta: {
      class: {
        th: "w-16",
        td: "w-16",
      },
    },
  },
];

const collegeColumns: TableColumn<College>[] = [
  {
    accessorKey: "collegeCode",
    header: "College Code",
    meta: {
      class: {
        th: "w-42",
        td: "w-42 text-md",
      },
    },
  },
  {
    accessorKey: "collegeName",
    header: "College Name",
    meta: {
      class: {
        td: "text-md",
      },
    },
  },
  {
    id: "actions",
    cell: ({ row }) => {
      return h(
        "div",
        h(
          UDropdownMenu,
          {
            content: {
              align: "end",
            },
            items: getRowItems(row),
            "aria-label": "Actions dropdown",
          },
          () =>
            h(UButton, {
              icon: "i-lucide-ellipsis-vertical",
              color: "neutral",
              variant: "ghost",
              class: "ml-auto",
              "aria-label": "Actions dropdown",
            })
        )
      );
    },
    meta: {
      class: {
        th: "w-16",
        td: "w-16",
      },
    },
  },
];

function getRowItems(row: Row<Student> | Row<Program> | Row<College>) {
  return [
    {
      type: "label",
      label: "Actions",
    },
    {
      type: "separator",
    },
    {
      label: "Edit",
      onSelect() {
        openEditDialog();
      },
    },
    {
      label: "Delete",
      onSelect() {
        openConfirmDeleteDialog(row.original);
      },
    },
  ];
}

const page = ref(5);
const reservedHeight = 300;
const rowsPerPage = ref(5);

const calculateRows = () => {
  const row = document.querySelector("table tbody tr");
  const rowHeight = row ? row.clientHeight + 1 : 64;

  const availableHeight = window.innerHeight - reservedHeight;

  rowsPerPage.value = Math.max(5, Math.floor(availableHeight / rowHeight));
};

onMounted(() => {
  calculateRows();
  window.addEventListener("resize", calculateRows);
});
</script>

<template>
  <AddEditEntityDialog
    v-model:is-open="isOpenEditDialog"
    class="ml-auto hidden"
    :entity-type="props.entityType"
    :dialog-type="'edit'"
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
    :columns="studentColumns"
    class="flex-1"
  />

  <UTable
    v-if="entityType === 'programs'"
    loading
    loading-color="primary"
    loading-animation="carousel"
    :data="programData.slice(0, rowsPerPage)"
    :columns="programColumns"
    class="flex-1"
  />

  <UTable
    v-if="entityType === 'colleges'"
    loading
    loading-color="primary"
    loading-animation="carousel"
    :data="collegeData.slice(0, rowsPerPage)"
    :columns="collegeColumns"
    class="flex-1"
  />

  <div class="flex justify-center">
    <UPagination
      v-model:page="page"
      show-edges
      size="xl"
      :sibling-count="1"
      :total="100"
    />
  </div>
</template>
