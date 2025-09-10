<script setup lang="ts">
const props = defineProps<{
  entityType: string;
}>();

// const emit = defineEmits<{
//   (
//     e:
//       | "update:searchBy"
//       | "update:searchType"
//       | "update:sortField"
//       | "update:sortOrder",
//     value: string
//   ): void;
// }>();

const isOpen = ref(false);
</script>

<template>
  <div>
    <UModal
      v-model:open="isOpen"
      :ui="{
        content: [entityType === 'students' ? 'w-[50%]' : 'w-[25%]'],
      }"
    >
      <UButton
        icon="solar:add-circle-linear"
        size="md"
        color="primary"
        variant="solid"
        class="cursor-pointer justify-center w-36"
        @click="isOpen = true"
        >{{ "Add " + capitalizeWords(props.entityType).slice(0, -1) }}</UButton
      >

      <template #header>
        <h2 class="text-3xl font-semibold">
          {{ "Add " + capitalizeWords(props.entityType).slice(0, -1) }}
        </h2>
      </template>

      <template #body>
        <AddEditEntityFormStudent v-if="entityType === 'students'" />
        <AddEditEntityFormProgram v-if="entityType === 'programs'" />
        <AddEditEntityFormCollege v-if="entityType === 'colleges'" />
      </template>

      <template #footer>
        <div class="flex justify-end gap-2">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="isOpen = false"
            >Close</UButton
          >
          <UButton
            size="md"
            color="primary"
            variant="solid"
            class="cursor-pointer"
            @click="isOpen = false"
            >Proceed</UButton
          >
        </div>
      </template>
    </UModal>

    <!-- <Dialog v-model:visible="visible" modal class="w-[30rem]">
      <template #header>
        <h2 v-if="props.dialogType === 'filter'" class="text-3xl font-semibold">
          Search Filters
        </h2>

        <h2 v-else class="text-3xl font-semibold">Sort Options</h2>
      </template>
      
    </Dialog> -->
  </div>
</template>
