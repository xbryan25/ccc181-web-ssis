<script setup lang="ts">
import { capitalizeWords } from '#imports';

const props = defineProps<{
  externalCheckboxValue: boolean | 'indeterminate';
  selectedRows: number;
  totalDisplayedRows: number;
  entityType: string;
  searchAndSortState: {
    searchValue: string;
    searchBy: string;
    searchType: string;
    sortField: string;
    sortOrder: string;
  };
}>();

const emit = defineEmits<{
  (
    e: 'onProceed',
    localState: {
      searchBy: string;
      searchType: string;
      sortField: string;
      sortOrder: string;
    },
  ): void;
  (e: 'update:searchValue', value: string): void;
  (e: 'onCreateEntitySubmit'): void;
  (e: 'toggleAll', val: boolean | 'indeterminate'): void;
}>();

const isOpenAddDialog = ref(false);

const rowsPerPageItems = ref([10, 25, 50]);
const rowsPerPage = ref(10);

const openAddDialog = () => {
  isOpenAddDialog.value = true;
};

const searchValue = computed({
  get: () => props.searchAndSortState.searchValue,
  set: (value: string) => emit('update:searchValue', value),
});

const checkboxValue = computed({
  get: () => props.externalCheckboxValue,
  set: () => {
    const nextVal =
      props.externalCheckboxValue === true || props.externalCheckboxValue === 'indeterminate'
        ? false
        : true;
    emit('toggleAll', nextVal);
  },
});
</script>

<template>
  <div class="flex gap-[10px]">
    <div class="flex-1 flex pl-3 items-center gap-3">
      <UCheckbox v-model="checkboxValue" :ui="{ base: 'cursor-pointer' }" />

      <div class="text-sm text-muted">
        {{ props.selectedRows }} of {{ props.totalDisplayedRows }}
        {{ props.totalDisplayedRows === 1 ? 'row' : 'rows' }} selected
      </div>

      <div v-if="externalCheckboxValue" class="flex gap-3">
        <UTooltip text="Edit">
          <UButton icon="material-symbols:edit-outline" color="primary" class="cursor-pointer" />
        </UTooltip>

        <UTooltip text="Delete">
          <UButton icon="material-symbols:delete-outline" color="primary" class="cursor-pointer" />
        </UTooltip>
      </div>
    </div>

    <div class="flex-[2] flex gap-3 justify-center">
      <UInput
        v-model="searchValue"
        icon="solar:magnifer-linear"
        size="md"
        variant="outline"
        placeholder="Search..."
      />

      <FilterSortDialog
        :entity-type="props.entityType"
        :dialog-type="'filter'"
        :search-and-sort-state="props.searchAndSortState"
        @on-proceed="
          (localState: {
            searchBy: string;
            searchType: string;
            sortField: string;
            sortOrder: string;
          }) => emit('onProceed', localState)
        "
      />

      <FilterSortDialog
        :entity-type="props.entityType"
        :dialog-type="'sort'"
        :search-and-sort-state="props.searchAndSortState"
        @on-proceed="
          (localState: {
            searchBy: string;
            searchType: string;
            sortField: string;
            sortOrder: string;
          }) => emit('onProceed', localState)
        "
      />

      <USelect v-model="rowsPerPage" :items="rowsPerPageItems" class="w-18" />
    </div>

    <div class="flex-1 flex justify-end">
      <UButton
        class="ml-auto cursor-pointer justify-center w-36"
        icon="solar:add-circle-linear"
        size="md"
        color="primary"
        variant="solid"
        @click="openAddDialog"
        >{{ 'Add ' + capitalizeWords(props.entityType).slice(0, -1) }}</UButton
      >

      <AddEditEntityDialog
        v-model:is-open="isOpenAddDialog"
        class="ml-auto hidden"
        :entity-type="props.entityType"
        :dialog-type="'add'"
        @on-submit="emit('onCreateEntitySubmit')"
      />
    </div>
  </div>
</template>
