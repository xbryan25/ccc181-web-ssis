<script setup lang="ts">
import type { College, CollegeFormState } from '~/types';

import { validateForm } from '#imports';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

const state = reactive<CollegeFormState>({
  collegeCode: '',
  collegeName: '',
});

const emit = defineEmits<{
  (e: 'onSubmit', newEntity: College): void;
  (e: 'onClose' | 'onSubmitError'): void;
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
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'college', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
    @submit="(event) => emit('onSubmit', event.data)"
    @error="emit('onSubmitError')"
  >
    <UFormField label="College Code" name="collegeCode" class="flex-1">
      <UInput v-model="state.collegeCode" class="w-full" />
    </UFormField>

    <UFormField label="College Name" name="collegeName" class="flex-1">
      <UInput v-model="state.collegeName" class="w-full" />
    </UFormField>

    <div class="flex justify-end gap-2 w-full pt-5">
      <UButton
        size="md"
        color="error"
        variant="solid"
        class="cursor-pointer"
        @click="emit('onClose')"
        >Close</UButton
      >
      <UButton size="md" color="primary" variant="solid" type="submit" class="cursor-pointer"
        >Proceed</UButton
      >
    </div>
  </UForm>
</template>
