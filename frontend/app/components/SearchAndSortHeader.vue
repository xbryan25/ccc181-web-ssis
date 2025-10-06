<script setup lang="ts">
const props = defineProps<{
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
}>();

const isOpenAddDialog = ref(false);

const openAddDialog = () => {
  isOpenAddDialog.value = true;
};

const searchValue = computed({
  get: () => props.searchAndSortState.searchValue,
  set: (value: string) => emit('update:searchValue', value),
});
</script>

<template>
  <div class="flex gap-3">
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
</template>
