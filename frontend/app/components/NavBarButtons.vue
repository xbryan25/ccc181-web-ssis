<script setup lang="ts">
defineProps<{
  url: string;
  buttonName: string;
  iconName: string;
}>();
</script>

<template>
  <NuxtLink
    :to="url"
    class="flex items-center h-12 rounded-lg hover:bg-zinc-700 cursor-pointer"
  >
    <Icon :name="iconName" class="flex-1 w-8 h-8 text-green-400" />
    <p class="flex-[3] font-bold text-green-400 text-xl">{{ buttonName }}</p>
  </NuxtLink>
</template>
