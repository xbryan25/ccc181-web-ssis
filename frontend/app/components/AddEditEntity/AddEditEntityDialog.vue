<script setup lang="ts">
import type { Student, Program, College } from '~/types';

const props = defineProps<{
  entityType: string;
  dialogType: string;
  isOpen: boolean;
  selectedEntity?: string;
}>();

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void;
  (e: 'onSubmit'): void;
}>();

const isOpen = computed({
  get: () => props.isOpen,
  set: (val: boolean) => {
    emit('update:isOpen', val);
  },
});

const toast = useToast();

async function onSubmit(newEntity: Student | Program | College) {
  isOpen.value = false;

  try {
    let data: { message: string };

    if (props.dialogType === 'add') {
      data = await useCreateEntity(props.entityType, newEntity);
    } else {
      data = await useEditEntityDetails(
        props.entityType,
        newEntity,
        props.selectedEntity as string,
      );
    }

    toast.add({
      title: 'Success',
      description: data.message,
      color: 'success',
    });
  } catch {
    toast.add({
      title: 'Error',
      description: 'Something went wrong!',
      color: 'error',
    });
  }

  emit('onSubmit');
}

async function onSubmitError() {
  toast.add({
    title: 'Error with inputs',
    description: `Resolve issues to ${props.dialogType} ${props.entityType.slice(0, -1)}.`,
    color: 'error',
  });
}
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
          {{ 'Add ' + capitalizeWords(props.entityType).slice(0, -1) }}
        </h2>

        <div v-else>
          <h2 class="text-3xl font-semibold">
            {{ 'Edit ' + capitalizeWords(props.entityType).slice(0, -1) }}
          </h2>
          <h3 class="text-md font-semibold text-stone-500">
            {{ `${capitalizeWords(props.entityType.slice(0, -1))}: ${props.selectedEntity}` }}
          </h3>
        </div>
      </template>

      <template #body>
        <AddEditEntityFormStudent
          v-if="entityType === 'students'"
          :dialog-type="props.dialogType"
          :selected-entity="props.selectedEntity"
          @on-submit="(newEntity) => onSubmit(newEntity)"
          @on-close="isOpen = false"
          @on-submit-error="onSubmitError"
        />
        <AddEditEntityFormProgram
          v-if="entityType === 'programs'"
          :dialog-type="props.dialogType"
          :selected-entity="props.selectedEntity"
          @on-submit="(newEntity) => onSubmit(newEntity)"
          @on-close="isOpen = false"
          @on-submit-error="onSubmitError"
        />
        <AddEditEntityFormCollege
          v-if="entityType === 'colleges'"
          :dialog-type="props.dialogType"
          :selected-entity="props.selectedEntity"
          @on-submit="(newEntity) => onSubmit(newEntity)"
          @on-close="isOpen = false"
          @on-submit-error="onSubmitError"
        />
      </template>

      <!-- <template #footer>
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
            @click="
              isOpen = false;
              clickProceed();
            "
            >Proceed</UButton
          >
        </div>
      </template> -->
    </UModal>
  </div>
</template>
