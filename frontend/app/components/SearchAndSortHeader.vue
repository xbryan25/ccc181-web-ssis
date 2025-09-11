<script setup lang="ts">
const props = defineProps<{
  entityType: string;
  searchAndSortState: {
    searchBy: string;
    searchType: string;
    sortField: string;
    sortOrder: string;
  };
}>();

const emit = defineEmits<{
  (
    e:
      | "update:searchBy"
      | "update:searchType"
      | "update:sortField"
      | "update:sortOrder",
    value: string
  ): void;
}>();

const isOpenAddDialog = ref(false);

const openAddDialog = () => {
  isOpenAddDialog.value = true;
};
</script>

<template>
  <div class="flex gap-3">
    <UInput
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

    <!-- <Button class="w-44 ml-auto">
      <Icon name="solar:add-circle-linear" class="h-6 w-6" />
      <p class="font-medium">Add {{ props.entityType.slice(0, -1) }}</p>
    </Button> -->

    <!-- <UButton
      icon="solar:filter-linear"
      size="md"
      color="primary"
      variant="solid"
      class="cursor-pointer ml-auto"
      :label="`Add ${capitalizeWords(entityType).slice(0, -1)}`"
    /> -->

    <UButton
      class="ml-auto cursor-pointer justify-center w-36"
      icon="solar:add-circle-linear"
      size="md"
      color="primary"
      variant="solid"
      @click="openAddDialog"
      >{{ "Add " + capitalizeWords(props.entityType).slice(0, -1) }}</UButton
    >

    <AddEditEntityDialog
      v-model:is-open="isOpenAddDialog"
      class="ml-auto hidden"
      :entity-type="props.entityType"
      :dialog-type="'add'"
    />
  </div>
</template>
