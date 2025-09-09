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

console.log("imports " + props.entityType);

const isVisibleFilterSortDialog = ref(false);
const dialogType = ref("sort");

const showFilterSortDialog = (chosenDialogType: string) => {
  isVisibleFilterSortDialog.value = true;
  dialogType.value = chosenDialogType;
};
</script>

<template>
  <div class="flex gap-3">
    <IconField>
      <FloatLabel variant="on">
        <InputIcon>
          <Icon name="solar:magnifer-linear" />
        </InputIcon>
        <InputText id="over_label" />
        <label for="over_label">Search</label>
      </FloatLabel>
    </IconField>

    <Button @click="showFilterSortDialog('filter')">
      <Icon name="solar:filter-linear" class="h-6 w-6" />
      <p class="font-medium">Filters</p>
    </Button>

    <Button @click="showFilterSortDialog('sort')">
      <Icon name="solar:sort-linear" class="h-6 w-6" />
      <p class="font-medium">Sort Options</p>
    </Button>

    <FilterSortDialog
      v-model="isVisibleFilterSortDialog"
      :entity-type="props.entityType"
      :dialog-type="dialogType"
      :search-and-sort-state="props.searchAndSortState"
      @update:search-by="(value: string) => emit('update:searchBy', value)"
      @update:search-type="(value: string) => emit('update:searchType', value)"
      @update:sort-field="(value: string) => emit('update:sortField', value)"
      @update:sort-order="(value: string) => emit('update:sortOrder', value)"
    />

    <Button class="w-44 ml-auto">
      <Icon name="solar:add-circle-linear" class="h-6 w-6" />
      <p class="font-medium">Add {{ props.entityType.slice(0, -1) }}</p>
    </Button>
  </div>
</template>
