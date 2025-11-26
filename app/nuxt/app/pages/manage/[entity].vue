<script setup lang="ts">
import type EntityTable from '~/components/EntityTable.vue';
import SearchAndSortHeader from '~/components/SearchAndSortHeader.vue';
import auth from '~/middleware/auth';
import { capitalizeWords } from '~/utils/stringUtils';

// definePageMeta validate only decides whether the page is valid to be shown
definePageMeta({
  validate: (route) => {
    const entity = route.params.entity;
    // Ensure id is a string
    if (typeof entity !== 'string') return false;

    return ['students', 'programs', 'colleges'].includes(entity);
  },
  middleware: auth,
});

const route = useRoute();
const entity = route.params.entity as string;

const fieldMap: Record<string, string> = {
  students: 'ID Number',
  programs: 'Program Code',
  colleges: 'College Code',
};

const defaultField = fieldMap[entity as keyof typeof fieldMap] || 'Unknown';

const searchAndSortState = reactive({
  searchValue: '',
  searchBy: defaultField,
  searchType: 'Starts With',
  sortField: defaultField,
  sortOrder: 'Ascending',
});

const createEntitySubmitRef = ref(false);

const onProceed = (localState: {
  searchBy: string;
  searchType: string;
  sortField: string;
  sortOrder: string;
}) => {
  searchAndSortState.searchBy = localState.searchBy;
  searchAndSortState.searchType = localState.searchType;
  searchAndSortState.sortField = localState.sortField;
  searchAndSortState.sortOrder = localState.sortOrder;
};

const selectedRows = ref<number>(0);
const rowsPerPage = ref<number>(10);
const loadedRowsPerPage = ref<number>(0);
const isLoading = ref<boolean>(false);

const externalCheckboxValue = ref<boolean | 'indeterminate'>(false);

const toggleAllCounter = ref(0);

function handleToggleAll(nextVal: boolean | 'indeterminate') {
  toggleAllCounter.value++;
  externalCheckboxValue.value = nextVal;
}

watch(selectedRows, (newSelectedRows) => {
  if (newSelectedRows === 0) externalCheckboxValue.value = false;
  else if (newSelectedRows === loadedRowsPerPage.value) externalCheckboxValue.value = true;
  else externalCheckboxValue.value = 'indeterminate';
});
</script>

<template>
  <div class="flex flex-col gap-10 h-full">
    <h1 class="font-bold text-5xl">{{ capitalizeWords(entity) }}</h1>

    <div class="flex flex-col gap-5">
      <SearchAndSortHeader
        :external-checkbox-value="externalCheckboxValue"
        :selected-rows="selectedRows"
        :loaded-rows-per-page="loadedRowsPerPage"
        :entity-type="entity"
        :search-and-sort-state="searchAndSortState"
        :is-loading="isLoading"
        @on-create-entity-submit="() => (createEntitySubmitRef = true)"
        @on-proceed="
          (localState: {
            searchBy: string;
            searchType: string;
            sortField: string;
            sortOrder: string;
          }) => onProceed(localState)
        "
        @update:search-value="(searchValue) => (searchAndSortState.searchValue = searchValue)"
        @update:rows-per-page="(value: number) => (rowsPerPage = value)"
        @toggle-all="(value) => handleToggleAll(value)"
      />

      <EntityTable
        :entity-type="entity"
        :search-value="searchAndSortState.searchValue"
        :search-by="searchAndSortState.searchBy"
        :search-type="searchAndSortState.searchType"
        :sort-field="searchAndSortState.sortField"
        :sort-order="searchAndSortState.sortOrder"
        :create-entity-submit-ref="createEntitySubmitRef"
        :toggle-all-counter="toggleAllCounter"
        :rows-per-page="rowsPerPage"
        :external-checkbox-value="externalCheckboxValue"
        @update:search-value="(value: string) => (searchAndSortState.searchValue = value)"
        @update:search-by="(value: string) => (searchAndSortState.searchBy = value)"
        @update:search-type="(value: string) => (searchAndSortState.searchType = value)"
        @update:sort-field="(value: string) => (searchAndSortState.sortField = value)"
        @update:sort-order="
          (value: string) => {
            searchAndSortState.sortOrder = value;
          }
        "
        @update:external-checkbox-value="
          (value: boolean | 'indeterminate') => (externalCheckboxValue = value)
        "
        @update:selected-rows="(value: number) => (selectedRows = value)"
        @update:loaded-rows-per-page="(value: number) => (loadedRowsPerPage = value)"
        @update:is-loading="(value: boolean) => (isLoading = value)"
        @disable-create-entity-submit="() => (createEntitySubmitRef = false)"
      />
    </div>
  </div>
</template>
