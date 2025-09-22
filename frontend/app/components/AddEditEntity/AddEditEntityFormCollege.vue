<script setup lang="ts">
import type { College, CollegeFormState } from '~/types';

import { validateForm } from '#imports';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
  toSubmit: boolean;
}>();

const state = reactive<CollegeFormState>({
  collegeCode: '',
  collegeName: '',
});

const transformCollegeState = () => {
  return {
    collegeCode: state.collegeCode,
    collegeName: state.collegeName,
  };
};

const emit = defineEmits<{
  (e: 'onSubmit', newEntity: College): void;
}>();

let hasCalled = false;

onMounted(async () => {
  if (props.dialogType === 'edit') {
    const entityData = await useEntityDetails('colleges', props.selectedEntity as string);

    state.collegeCode = entityData.collegeCode;
    state.collegeName = entityData.collegeName;
  }

  hasCalled = true;
});

watch(
  () => props.toSubmit,
  (val) => {
    if (val) {
      emit('onSubmit', transformCollegeState());
    }
  },
);
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'college', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
  >
    <UFormField label="College Code" name="collegeCode" class="flex-1">
      <UInput v-model="state.collegeCode" class="w-full" />
    </UFormField>

    <UFormField label="College Name" name="collegeName" class="flex-1">
      <UInput v-model="state.collegeName" class="w-full" />
    </UFormField>
  </UForm>
</template>
