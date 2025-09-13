<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '@nuxt/ui';

import { useEntityDetails, useEditEntityDetails } from '~/composables';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

interface CollegeFormState {
  collegeCode: string;
  collegeName: string;
}

const state = reactive<CollegeFormState>({
  collegeCode: '',
  collegeName: '',
});

const collegeCodeRegex = /^[A-Z-]+$/;
const collegeNameRegex = /^[A-Za-z- ]+$/;

const validate = (state: CollegeFormState): FormError[] => {
  if (!hasCalled) return [];

  console.log(isMounted);

  const errors = [];
  if (!state.collegeCode) {
    errors.push({ name: 'collegeCode', message: 'Required.' });
  } else if (state.collegeCode && !collegeCodeRegex.test(state.collegeCode)) {
    errors.push({
      name: 'collegeCode',
      message: 'Uppercase letters & dashes only.',
    });
  }

  if (!state.collegeName) {
    errors.push({ name: 'collegeName', message: 'Required.' });
  } else if (state.collegeName && !collegeNameRegex.test(state.collegeName)) {
    errors.push({
      name: 'collegeName',
      message: 'Letters, spaces, and dashes only.',
    });
  }

  return errors;
};

const toast = useToast();

async function onSubmit(event: FormSubmitEvent<typeof state>) {
  const newEntity = {
    collegeCode: event.data.collegeCode,
    collegeName: event.data.collegeName,
  };

  const { data: messageData, error } = await useEditEntityDetails(props.dialogType, newEntity);

  if (error.value) {
    toast.add({
      title: 'Error',
      description: 'Something went wrong!',
      color: 'error',
    });
    return;
  } else if (!error.value && messageData.value) {
    toast.add({
      title: 'Success',
      description: messageData.value.message,
      color: 'success',
    });
  }
}

let hasCalled = false;
let isMounted = false;

onMounted(() => {
  if (props.dialogType === 'edit') {
    const { data: collegeData } = useEntityDetails(
      props.dialogType,
      props.selectedEntity as string,
    );

    Object.assign(state, collegeData);
    console.log('Data loaded', state);
  }

  hasCalled = true;
  isMounted = true;
});
</script>

<template>
  <UForm :validate="validate" :state="state" class="flex flex-col space-y-4" @submit="onSubmit">
    <UFormField label="College Code" name="collegeCode" class="flex-1">
      <UInput v-model="state.collegeCode" class="w-full" />
    </UFormField>

    <UFormField label="College Name" name="collegeName" class="flex-1">
      <UInput v-model="state.collegeName" class="w-full" />
    </UFormField>
  </UForm>
</template>
