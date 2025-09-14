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
    e:
      | 'update:searchValue'
      | 'update:searchBy'
      | 'update:searchType'
      | 'update:sortField'
      | 'update:sortOrder',
    value: string,
  ): void;
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
      @update:search-by="(value: string) => emit('update:searchBy', value)"
      @update:search-type="(value: string) => emit('update:searchType', value)"
      @update:sort-field="(value: string) => emit('update:sortField', value)"
      @update:sort-order="(value: string) => emit('update:sortOrder', value)"
    />

    <FilterSortDialog
      :entity-type="props.entityType"
      :dialog-type="'sort'"
      :search-and-sort-state="props.searchAndSortState"
      @update:search-by="(value: string) => emit('update:searchBy', value)"
      @update:search-type="(value: string) => emit('update:searchType', value)"
      @update:sort-field="(value: string) => emit('update:sortField', value)"
      @update:sort-order="(value: string) => emit('update:sortOrder', value)"
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
    />
  </div>
</template>
