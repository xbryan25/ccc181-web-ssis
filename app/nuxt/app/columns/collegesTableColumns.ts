import type { DefineComponent } from "vue";
import type { Row } from "@tanstack/vue-table";

import type { College } from "~/types";
import { getRowItems } from "#imports";

export function getCollegesTableColumns(callbacks :{
  openEditDialog: (row: College) => void;
  openConfirmDeleteDialog: (row: College) => void;
  }, components: { UCheckbox: DefineComponent; UButton: DefineComponent; UDropdownMenu: DefineComponent }, isLoading: Ref<boolean>,
  selectedRows: Ref<Set<string>>, onCheckboxToggle: (idNumber: string, value: boolean) => void) { 

  const {UCheckbox, UButton, UDropdownMenu} = components

  return [
    {
      id: 'select',
      cell: ({ row }: { row: Row<College> }) =>
        h(UCheckbox, {
          ui: {
            base: 'cursor-pointer',
          },
          disabled: isLoading.value,
          modelValue: computed(() => selectedRows.value.has(row.original.collegeCode)).value,
          'onUpdate:modelValue': (value: boolean) => {
            onCheckboxToggle(row.original.collegeCode, value);
          },
          'aria-label': 'Select row',
        }),
      meta: {
        class: {
          th: 'w-12',
          td: 'w-12',
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
  ]
};

