import type { Row } from "@tanstack/vue-table";
import type { DefineComponent } from "vue";
import type { Student } from "~/types";
import { getRowItems } from "#imports";


export function getStudentsTableColumns(callbacks :{
  openEditDialog: (row: Student) => void;
  openConfirmDeleteDialog: (row: Student) => void;
 }, components: { UButton: DefineComponent; UDropdownMenu: DefineComponent }) { 

  const {UButton, UDropdownMenu} = components

  return [
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
      cell: ({ row }: { row: Row<Student> }) => {
        return h(
          "div",
          h(
            UDropdownMenu,
            {
              content: {
                align: "end",
              },
              items: getRowItems<Student>(row, callbacks),
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
  ]};

