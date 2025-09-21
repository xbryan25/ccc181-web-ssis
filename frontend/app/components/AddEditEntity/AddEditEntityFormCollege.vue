<script setup lang="ts">
import type { CollegeFormState } from '~/types';

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

const transformCollegeState = (input: CollegeFormState) => {
  return {
    collegeCode: input.collegeCode,
    collegeName: input.collegeName,
  };
};

const emit = defineEmits<{
  (e: 'onSubmit', newEntity: CollegeFormState): void;
}>();

let hasCalled = false;

onMounted(async () => {
  if (props.dialogType === 'edit') {
    const data = await useEntityDetails('colleges', props.selectedEntity as string);

    Object.assign(state, data.entityDetails);
    console.log('Data loaded', state);
  }

  hasCalled = true;
});

watch(
  () => props.toSubmit,
  (val) => {
    if (val) {
      emit('onSubmit', transformCollegeState(state));
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
