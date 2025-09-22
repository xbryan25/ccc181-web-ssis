<script setup lang="ts">
const props = defineProps<{
  entityType: string;
  isOpen: boolean;
  selectedEntity: string;
}>();

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void;
  (e: 'onDelete'): void;
}>();

const isOpen = computed({
  get: () => props.isOpen,
  set: (val: boolean) => {
    console.log('close dialog');
    emit('update:isOpen', val);
  },
});

const toast = useToast();

async function onDelete() {
  try {
    isOpen.value = false;

    const data: { message: string } = await useDeleteEntity(props.entityType, props.selectedEntity);

    toast.add({
      title: 'Success',
      description: data.message,
      color: 'success',
    });

    emit('onDelete');
  } catch {
    toast.add({
      title: 'Error',
      description: 'Something went wrong!',
      color: 'error',
    });
  }
}
</script>

<template>
  <div>
    <UModal
      v-model:open="isOpen"
      :ui="{
        content: 'w-[30%]',
      }"
    >
      <template #header>
        <div class="flex flex-col">
          <h2 class="text-3xl font-semibold">Confirm delete</h2>
          <h3 class="text-md font-semibold text-stone-500">
            {{ `${capitalizeWords(props.entityType.slice(0, -1))}: ${props.selectedEntity}` }}
          </h3>
        </div>
      </template>

      <template #body>
        <div class="flex flex-col items-center">
          <UIcon
            name="material-symbols:warning-rounded"
            class="size-20 text-red-500 animate-bounce"
          />
          <div>
            <p>
              {{ `Are you sure you want to delete this ${props.entityType.slice(0, -1)}?` }}
            </p>
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex justify-end gap-2 w-full">
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
            @click="onDelete"
            >Proceed</UButton
          >
        </div>
      </template>
    </UModal>
  </div>
</template>
