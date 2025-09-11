import type { DefineComponent } from "vue";
import type { Row } from "@tanstack/vue-table";

import type { College } from "~/types";
import { getRowItems } from "#imports";

export function getCollegesTableColumns(callbacks :{
  openEditDialog: () => void;
  openConfirmDeleteDialog: (row: College) => void;
 }, components: { UButton: DefineComponent; UDropdownMenu: DefineComponent }) { 

  const {UButton, UDropdownMenu} = components

  return [
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
      cell: ({ row }: { row: Row<College> }) => {
        return h(
          "div",
          h(
            UDropdownMenu,
            {
              content: {
                align: "end",
              },
              items: getRowItems<College>(row, callbacks),
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

