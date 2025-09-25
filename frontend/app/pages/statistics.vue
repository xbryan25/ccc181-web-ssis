<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div>
    <h1>Welcome to the statistics page</h1>
    <AppAlert class=""> This is an auto-imported component </AppAlert>
    <NuxtLink to="/about" class="font-bold">Link</NuxtLink>
  </div>
</template>
