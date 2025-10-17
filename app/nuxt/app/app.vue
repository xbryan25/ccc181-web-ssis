<script setup lang="ts">
import { onMounted } from 'vue';

useHead({
  title: 'Sequence',
  meta: [{ name: 'description', content: 'This is my awesome Nuxt app' }],
  link: [{ rel: 'icon', type: 'image/png', href: '/favicon.svg' }],
});

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
