<script setup lang="ts">
const props = defineProps<{
  entityType: string;
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
    />

    <Button class="w-44 ml-auto">
      <Icon name="solar:add-circle-linear" class="h-6 w-6" />
      <p class="font-medium">Add {{ props.entityType.slice(0, -1) }}</p>
    </Button>
  </div>
</template>
