<script setup lang="ts">
type EntityPropertiesOptions = Record<string, string[]>;

const props = defineProps<{
  entityType: string;
  dialogType: string;
  searchAndSortState: {
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
}>();

const isOpen = ref(false);

const localState = reactive({ ...props.searchAndSortState });

const entityPropertiesOptions: EntityPropertiesOptions = {
  students: ['ID Number', 'First Name', 'Last Name', 'Year Level', 'Gender', 'Program Code'],
  programs: ['Program Code', 'Program Name', 'College Code'],
  colleges: ['College Code', 'College Name'],
};

const filterTypes = ['Starts With', 'Ends With', 'Contains'];

const sortTypes = ['Ascending', 'Descending'];

const getTextForTooltip = (): string => {
  if (props.dialogType === 'filter') {
    return `Search By: ${localState.searchBy} | Search Type: ${localState.searchType}`;
  } else {
    return `Sort Field: ${localState.sortField} | Sort Order: ${localState.sortOrder}`;
  }
};

// Watcher for searchAndSortState changes
watch(
  () => props.searchAndSortState,
  (newVal) => {
    Object.assign(localState, newVal);
  },
  { deep: true, immediate: true },
);
</script>

<template>
  <div>
    <UModal v-model:open="isOpen">
      <UTooltip
        :content="{
          align: 'center',
          side: 'top',
          sideOffset: 8,
        }"
        arrow
        :ui="{ content: 'data-[state=delayed-open]:animate-none data-[state=closed]:animate-none' }"
      >
        <template #content>
          {{ getTextForTooltip() }}
        </template>
        <UButton
          :icon="props.dialogType === 'filter' ? 'solar:filter-linear' : 'solar:sort-linear'"
          size="md"
          color="primary"
          variant="solid"
          class="cursor-pointer"
          @click="isOpen = true"
          >{{ props.dialogType === 'filter' ? 'Filters' : 'Sort Options' }}
        </UButton>
      </UTooltip>

      <template #header>
        <h2 v-if="props.dialogType === 'filter'" class="text-3xl font-semibold">Search Filters</h2>

        <h2 v-else class="text-3xl font-semibold">Sort Options</h2>
      </template>

      <template #body>
        <div>
          <div class="flex-col mb-12">
            <div v-if="props.dialogType === 'filter'" class="w-full flex gap-4 mb-2">
              <h3 class="flex-1 text-lg font-medium">Search By</h3>
              <h3 class="flex-1 text-lg font-medium">Search Type</h3>
            </div>
            <div v-else class="w-full flex gap-4 mb-2">
              <h3 class="flex-1 text-lg font-medium">Sort Field</h3>
              <h3 class="flex-1 text-lg font-medium">Sort Order</h3>
            </div>
            <div class="w-full flex gap-4 mb-2">
              <div class="flex-1 h-[2px] bg-primary" />
              <div class="flex-1 h-[2px] bg-primary" />
            </div>
            <div class="w-full flex gap-4 mb-4">
              <RadioSelectButtons
                :options="entityPropertiesOptions[props.entityType] ?? []"
                :dialog-type="props.dialogType"
                :column-position="'first'"
                :search-and-sort-state="localState"
                @update:search-by="(value: string) => (localState.searchBy = value)"
                @update:search-type="(value: string) => (localState.searchType = value)"
                @update:sort-field="(value: string) => (localState.sortField = value)"
                @update:sort-order="(value: string) => (localState.sortOrder = value)"
              />
              <RadioSelectButtons
                :options="props.dialogType === 'filter' ? filterTypes : sortTypes"
                :dialog-type="props.dialogType"
                :column-position="'second'"
                :search-and-sort-state="localState"
                @update:search-by="(value: string) => (localState.searchBy = value)"
                @update:search-type="(value: string) => (localState.searchType = value)"
                @update:sort-field="(value: string) => (localState.sortField = value)"
                @update:sort-order="(value: string) => (localState.sortOrder = value)"
              />
            </div>
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex justify-end gap-2 w-full">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="isOpen = false"
            >Close</UButton
          >
          <UButton
            size="md"
            color="primary"
            variant="solid"
            class="cursor-pointer"
            @click="
              isOpen = false;
              emit('onProceed', localState);
            "
            >Proceed</UButton
          >
        </div>
      </template>
    </UModal>
  </div>
</template>
