<script setup lang="ts">
const props = defineProps<{
  options: string[];
}>();

// const emit = defineEmits<{
//   (e: "update:modelValue", value: boolean): void;
// }>();

// const visible = computed({
//   get: () => props.modelValue,
//   set: (value: boolean) => emit("update:modelValue", value),
// });

const currentOption = ref(props.options[0]);
</script>

<template>
  <div class="flex-1 flex flex-col gap-2">
    <button
      v-for="(option, index) in options"
      :key="index"
      :class="[
        'w-full h-10 rounded-lg transition-colors duration-100',
        currentOption === option
          ? 'bg-zinc-700 text-white'
          : 'text-white hover:bg-zinc-700',
      ]"
      @click="currentOption = option"
    >
      <p class="font-medium">{{ option }}</p>
    </button>
  </div>
</template>
