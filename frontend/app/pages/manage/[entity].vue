<script setup lang="ts">
import SearchAndSortHeader from "~/components/SearchAndSortHeader.vue";
import { capitalizeWords } from "~/utils/stringUtils";

// definePageMeta validate only decides whether the page is valid to be shown
definePageMeta({
  validate: (route) => {
    const entity = route.params.entity;
    // Ensure id is a string
    if (typeof entity !== "string") return false;

    console.log(entity);
    return ["students", "programs", "colleges"].includes(entity);
  },
});

const route = useRoute();
const entity = route.params.entity;
</script>

<template>
  <div class="flex flex-col gap-10">
    <h1 class="font-bold text-5xl">{{ capitalizeWords(entity) }}</h1>
    <SearchAndSortHeader :entity-type="entity" />
  </div>
</template>
