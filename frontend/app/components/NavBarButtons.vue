<script setup lang="ts">
import type { RouteLocationNormalizedGeneric } from 'vue-router';

const props = defineProps<{
  url: string;
  buttonName: string;
  iconName: string;
}>();

const route: RouteLocationNormalizedGeneric = useRoute();

console.log(props.url);

const isActive = () => {
  if (props.url.endsWith(route.path)) {
    console.log(true);
    return true;
  } else {
    return false;
  }
};
</script>

<template>
  <NuxtLink
    :to="url"
    :class="[
      'flex items-center h-12 rounded-lg cursor-pointer transition-transform duration-300 hover:scale-105',
      isActive() ? 'bg-accented text-primary' : 'text-muted hover:bg-accented hover:text-primary',
    ]"
  >
    <Icon :name="iconName" class="flex-1 w-8 h-8" />
    <p class="flex-[3] font-bold text-xl">{{ buttonName }}</p>
  </NuxtLink>
</template>
