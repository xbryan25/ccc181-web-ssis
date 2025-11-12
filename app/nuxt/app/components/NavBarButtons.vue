<script setup lang="ts">
import type { RouteLocationNormalizedGeneric } from 'vue-router';

const props = defineProps<{
  url: string;
  buttonName: string;
  iconName: string;
  isCollapsed: boolean;
}>();

const route: RouteLocationNormalizedGeneric = useRoute();

const isActive = () => {
  if (props.url.endsWith(route.path)) {
    return true;
  } else {
    return false;
  }
};

// watch(
//   () => props.isCollapsed,
//   (newVal) => console.log(newVal),
// );
</script>

<template>
  <NuxtLink
    :to="url"
    :class="[
      'flex items-center h-12 rounded-lg cursor-pointer transition-all duration-300 hover:scale-105',
      isActive() ? 'bg-accented text-primary' : 'text-muted hover:bg-accented hover:text-primary',
      isCollapsed ? 'w-12' : 'w-full',
    ]"
  >
    <div class="flex items-center w-full px-2">
      <Icon :name="iconName" class="w-8 h-8 flex-shrink-0" />

      <Transition name="fade">
        <p
          v-if="!props.isCollapsed"
          class="ml-3 font-bold text-xl whitespace-nowrap overflow-hidden transition-opacity duration-300"
        >
          {{ buttonName }}
        </p>
      </Transition>
    </div>
  </NuxtLink>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateX(0);
}
</style>
