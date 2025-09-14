<script setup lang="ts">
import SearchAndSortHeader from '~/components/SearchAndSortHeader.vue';
import { capitalizeWords } from '~/utils/stringUtils';

// definePageMeta validate only decides whether the page is valid to be shown
definePageMeta({
  validate: (route) => {
    const entity = route.params.entity;
    // Ensure id is a string
    if (typeof entity !== 'string') return false;

    console.log(entity);
    return ['students', 'programs', 'colleges'].includes(entity);
  },
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
</script>

<template>
  <div class="flex flex-col gap-10 h-full">
    <h1 class="font-bold text-5xl">{{ capitalizeWords(entity) }}</h1>

    <SearchAndSortHeader
      :entity-type="entity"
      :search-and-sort-state="searchAndSortState"
      @update:search-value="(value: string) => (searchAndSortState.searchValue = value)"
      @update:search-by="(value: string) => (searchAndSortState.searchBy = value)"
      @update:search-type="(value: string) => (searchAndSortState.searchType = value)"
      @update:sort-field="(value: string) => (searchAndSortState.sortField = value)"
      @update:sort-order="(value: string) => (searchAndSortState.sortOrder = value)"
    />

    <EntityTable
      :entity-type="entity"
      :search-value="searchAndSortState.searchValue"
      :search-by="searchAndSortState.searchBy"
      :search-type="searchAndSortState.searchType"
      :sort-field="searchAndSortState.sortField"
      :sort-order="searchAndSortState.sortOrder"
      @update:search-value="(value: string) => (searchAndSortState.searchValue = value)"
      @update:search-by="(value: string) => (searchAndSortState.searchBy = value)"
      @update:search-type="(value: string) => (searchAndSortState.searchType = value)"
      @update:sort-field="(value: string) => (searchAndSortState.sortField = value)"
      @update:sort-order="(value: string) => (searchAndSortState.sortOrder = value)"
    />
  </div>
</template>
