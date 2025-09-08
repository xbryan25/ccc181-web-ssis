<script setup lang="ts">
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
  <div>
    <h1>Welcome to the {{ entity }} page</h1>
    <NuxtLink to="/about" class="font-bold">Link</NuxtLink>
  </div>
</template>
