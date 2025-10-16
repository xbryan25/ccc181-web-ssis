<script setup lang="ts">
import { onMounted } from 'vue';

const toaster = { position: 'top-right' } as const;

onMounted(() => {
  window.dispatchEvent(new Event('nuxt-ready'));
});
</script>

<template>
  <UApp :toaster="toaster">
    <NuxtLayout />
  </UApp>
</template>
