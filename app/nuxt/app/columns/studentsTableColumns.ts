import type { Row } from "@tanstack/vue-table";
import type { DefineComponent, Ref } from "vue";
import type { Student } from "~/types";
import { getRowItems } from "#imports";

export function getStudentsTableColumns(callbacks :{
  openEditDialog: (row: Student) => void;
  openConfirmDeleteDialog: (row: Student) => void;
  }, components: { UCheckbox: DefineComponent; UButton: DefineComponent; UDropdownMenu: DefineComponent},
  UAvatar: DefineComponent, onAvatarClick: (avatarUrl: string) => void, isLoading: Ref<boolean>,
  selectedRows: Ref<Set<string>>, onCheckboxToggle: (idNumber: string, value: boolean) => void) { 

  const {UCheckbox, UButton, UDropdownMenu} = components

  return [
    {
      id: 'select',
      cell: ({ row }: { row: Row<Student> }) =>
        h(UCheckbox, {
          ui: {
            base: 'cursor-pointer',
          },
          disabled: isLoading.value,
          modelValue: computed(() => selectedRows.value.has(row.original.idNumber)).value,
          'onUpdate:modelValue': (value: boolean) => {
            onCheckboxToggle(row.original.idNumber, value);
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
      id: "actions",

      meta: {
        class: {
          th: "w-20",
          td: "w-20 text-md",
        },
      },

      cell: ({ row }: { row: Row<Student> }) => h(UAvatar, { src: row.original.avatarUrl || '/images/noAvatar.jpg', size: "3xl", ui: {image: "cursor-pointer"}, onClick: () => onAvatarClick(row.original.avatarUrl)})

    },
    {
      accessorKey: "idNumber",
      header: "ID Number",
      meta: {
        class: {
          th: "w-32",
          td: "w-32 text-md",
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

