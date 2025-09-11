import type { DefineComponent } from "vue";
import type { Row } from "@tanstack/vue-table";

import type { Program } from "~/types";
import { getRowItems } from "#imports";

export function getProgramsTableColumns(callbacks :{
  openEditDialog: () => void;
  openConfirmDeleteDialog: (row: Program) => void;
 }, components: { UButton: DefineComponent; UDropdownMenu: DefineComponent }) { 

  const {UButton, UDropdownMenu} = components

  return [
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
      cell: ({ row }: { row: Row<Program> }) => {
        return h(
          "div",
          h(
            UDropdownMenu,
            {
              content: {
                align: "end",
              },
              items: getRowItems<Program>(row, callbacks),
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

