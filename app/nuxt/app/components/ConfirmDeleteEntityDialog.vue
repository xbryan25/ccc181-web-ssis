<script setup lang="ts">
import { capitalizeWords } from '#imports';

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
    emit('update:isOpen', val);
  },
});

const toast = useToast();

const isDeleting = ref(false);

async function onDelete() {
  try {
    isDeleting.value = true;

    const data: { message: string } = await useDeleteEntity(props.entityType, props.selectedEntity);

    toast.add({
      title: 'Success',
      description: data.message,
      color: 'success',
    });

    isOpen.value = false;
    emit('onDelete');
  } catch {
    toast.add({
      title: 'Error',
      description: 'Something went wrong!',
      color: 'error',
    });
  }
}

watch(
  () => props.isOpen,
  async (newValue) => {
    if (!newValue) {
      // e.g. delay reset after modal closes
      setTimeout(() => {
        isDeleting.value = false;
      }, 300); // delay in ms
    }
  },
);
</script>

<template>
  <div>
    <UModal
      v-model:open="isOpen"
      :ui="{
        content: ['max-w-lg', isDeleting ? 'h-[30%]' : ''],
        body: isDeleting ? 'flex items-center justify-center' : '',
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
        <div v-if="!isDeleting" class="flex flex-col items-center">
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

        <div v-if="isDeleting" class="flex justify-center items-center">
          <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
          <span class="ml-2 text-primary">Deleting {{ props.entityType.slice(0, -1) }}...</span>
        </div>
      </template>

      <template v-if="!isDeleting" #footer>
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
