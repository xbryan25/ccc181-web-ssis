<script setup lang="ts">
const props = defineProps<{
  entityType: string;
  dialogType: string;
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: "update:isOpen", value: boolean): void;
}>();

const isOpen = computed({
  get: () => props.isOpen,
  set: (val: boolean) => {
    console.log("close dialog");
    emit("update:isOpen", val);
  },
});
</script>

<template>
  <div>
    <UModal
      v-model:open="isOpen"
      :ui="{
        content: entityType === 'students' ? 'w-[50%]' : 'w-[25%]',
      }"
    >
      <template #header>
        <h2 v-if="props.dialogType === 'add'" class="text-3xl font-semibold">
          {{ "Add " + capitalizeWords(props.entityType).slice(0, -1) }}
        </h2>

        <h2 v-else class="text-3xl font-semibold">
          {{ "Edit " + capitalizeWords(props.entityType).slice(0, -1) }}
        </h2>
      </template>

      <template #body>
        <AddEditEntityFormStudent
          v-if="entityType === 'students'"
          :dialog-type="props.dialogType"
        />
        <AddEditEntityFormProgram
          v-if="entityType === 'programs'"
          :dialog-type="props.dialogType"
        />
        <AddEditEntityFormCollege
          v-if="entityType === 'colleges'"
          :dialog-type="props.dialogType"
        />
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
