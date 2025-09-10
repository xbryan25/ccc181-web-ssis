<script setup lang="ts">
import SearchAndSortHeader from "~/components/SearchAndSortHeader.vue";
import { capitalizeWords } from "~/utils/stringUtils";
import type { TableColumn } from "@nuxt/ui";
import type { Row } from "@tanstack/vue-table";

type Student = {
  idNumber: string;
  firstName: string;
  lastName: string;
  yearLevel: "1st" | "2nd" | "3rd" | "4th" | "4th+";
  gender: "Male" | "Female" | "Others" | "Prefer not to say";
  programCode: string;
};

// definePageMeta validate only decides whether the page is valid to be shown
definePageMeta({
  validate: (route) => {
    const entity = route.params.entity;
    // Ensure id is a string
    if (typeof entity !== "string") return false;

    console.log(entity);
    return ["students", "programs", "colleges"].includes(entity);
  },
});

const route = useRoute();
const entity = route.params.entity as string;

const fieldMap: Record<string, string> = {
  students: "ID Number",
  programs: "Program Code",
  colleges: "College Code",
};

const defaultField = fieldMap[entity as keyof typeof fieldMap] || "Unknown";

const searchAndSortState = reactive({
  searchBy: defaultField,
  searchType: "Starts With",
  sortField: defaultField,
  sortOrder: "Ascending",
});

const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const data = ref<Student[]>([
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

const columns: TableColumn<Student>[] = [
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

function getRowItems(row: Row<Student>) {
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
        console.log(`Edit ${row.original.idNumber}`);
      },
    },
    {
      label: "Delete",
      onSelect() {
        console.log(`Delete ${row.original.idNumber}`);
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
  <div class="flex flex-col gap-10 h-full">
    <h1 class="font-bold text-5xl">{{ capitalizeWords(entity) }}</h1>

    <SearchAndSortHeader
      :entity-type="entity"
      :search-and-sort-state="searchAndSortState"
      @update:search-by="
        (value: string) => (searchAndSortState.searchBy = value)
      "
      @update:search-type="
        (value: string) => (searchAndSortState.searchType = value)
      "
      @update:sort-field="
        (value: string) => (searchAndSortState.sortField = value)
      "
      @update:sort-order="
        (value: string) => (searchAndSortState.sortOrder = value)
      "
    />

    <UTable
      loading
      loading-color="primary"
      loading-animation="carousel"
      :data="data.slice(0, rowsPerPage)"
      :columns="columns"
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
  </div>
</template>
