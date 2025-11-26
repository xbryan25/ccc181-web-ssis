<script setup lang="ts">
import type { StudentFormState, ProgramFormState, CollegeFormState } from '~/types';

import { capitalizeWords } from '#imports';

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

const isSubmitting = ref(false);

const isStudentFormState = (
  entity: StudentFormState | ProgramFormState | CollegeFormState,
): entity is StudentFormState => {
  return (
    entity &&
    typeof entity === 'object' &&
    'idNumber' in entity &&
    'firstName' in entity &&
    'lastName' in entity &&
    'yearLevel' in entity &&
    'gender' in entity &&
    'programCode' in entity &&
    'avatar' in entity
  );
};

async function onSubmit(newEntity: StudentFormState | ProgramFormState | CollegeFormState) {
  try {
    isSubmitting.value = true;

    let data: { message: string } = { message: '' };

    if (props.dialogType === 'add') {
      if (props.entityType === 'students' && isStudentFormState(newEntity)) {
        const studentFormData = new FormData();
        studentFormData.append('idNumber', newEntity.idNumber);
        studentFormData.append('firstName', newEntity.firstName);
        studentFormData.append('lastName', newEntity.lastName);
        studentFormData.append('yearLevel', newEntity.yearLevel.label);
        studentFormData.append('gender', newEntity.gender.label);
        studentFormData.append('programCode', newEntity.programCode.label);

        if (newEntity.avatar) {
          studentFormData.append('avatar', newEntity.avatar);
        }

        data = await useCreateEntity(props.entityType, { studentFormData });
      } else if (!isStudentFormState(newEntity)) {
        data = await useCreateEntity(props.entityType, { entityDetails: newEntity });
      }
    } else {
      if (props.entityType === 'students' && isStudentFormState(newEntity)) {
        const studentFormData = new FormData();

        studentFormData.append('idNumber', newEntity.idNumber);
        studentFormData.append('firstName', newEntity.firstName);
        studentFormData.append('lastName', newEntity.lastName);
        studentFormData.append('yearLevel', newEntity.yearLevel.label);
        studentFormData.append('gender', newEntity.gender.label);
        studentFormData.append('programCode', newEntity.programCode.label);

        if (newEntity.avatar) {
          studentFormData.append('avatar', newEntity.avatar);
        }

        if (newEntity.existingAvatarUrl) {
          studentFormData.append('existingAvatarUrl', newEntity.existingAvatarUrl);
        }

        data = await useEditEntityDetails(
          props.entityType,
          { studentFormData },
          props.selectedEntity as string,
        );
      } else if (!isStudentFormState(newEntity)) {
        data = await useEditEntityDetails(
          props.entityType,
          { entityDetails: newEntity },
          props.selectedEntity as string,
        );
      }
    }

    toast.add({
      title: 'Success',
      description: data.message,
      color: 'success',
    });

    isOpen.value = false;
    emit('onSubmit');
  } catch (error) {
    let errorMessage;

    if (error instanceof Error) {
      errorMessage = error.message; // fetch error reason
    }

    if (typeof error === 'object' && error !== null && 'data' in error) {
      errorMessage = (error as any).data.error;
    }

    toast.add({
      title: 'Error',
      description: errorMessage,
      color: 'error',
    });

    isSubmitting.value = false;
  }
}

async function onSubmitError() {
  toast.add({
    title: 'Error with inputs',
    description: `Resolve issues to ${props.dialogType} ${props.entityType.slice(0, -1)}.`,
    color: 'error',
  });
}

watch(
  () => props.isOpen,
  async (newValue) => {
    if (!newValue) {
      // e.g. delay reset after modal closes
      setTimeout(() => {
        isSubmitting.value = false;
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
        content: isSubmitting
          ? 'max-w-lg h-[30%]'
          : props.entityType === 'students'
            ? 'max-w-2xl'
            : 'max-w-lg',
        body: isSubmitting ? 'flex items-center justify-center' : '',
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
          v-if="entityType === 'students' && !isSubmitting"
          :dialog-type="props.dialogType"
          :selected-entity="props.selectedEntity"
          @on-submit="(newEntity) => onSubmit(newEntity)"
          @on-close="isOpen = false"
          @on-submit-error="onSubmitError"
        />
        <AddEditEntityFormProgram
          v-if="entityType === 'programs' && !isSubmitting"
          :dialog-type="props.dialogType"
          :selected-entity="props.selectedEntity"
          @on-submit="(newEntity) => onSubmit(newEntity)"
          @on-close="isOpen = false"
          @on-submit-error="onSubmitError"
        />
        <AddEditEntityFormCollege
          v-if="entityType === 'colleges' && !isSubmitting"
          :dialog-type="props.dialogType"
          :selected-entity="props.selectedEntity"
          @on-submit="(newEntity) => onSubmit(newEntity)"
          @on-close="isOpen = false"
          @on-submit-error="onSubmitError"
        />

        <div v-if="isSubmitting" class="flex justify-center items-center">
          <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-accent" />
          <span class="ml-2 text-primary"
            >{{ capitalizeWords(props.dialogType) + 'ing' }}
            {{ props.entityType.slice(0, -1) }}...</span
          >
        </div>
      </template>
    </UModal>
  </div>
</template>
