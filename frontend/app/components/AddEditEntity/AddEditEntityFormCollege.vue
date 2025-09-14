<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

import type { CollegeFormState } from '~/types';

import { validateForm } from '#imports';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

const state = reactive<CollegeFormState>({
  collegeCode: '',
  collegeName: '',
});

const toast = useToast();

async function onSubmit(event: FormSubmitEvent<typeof state>) {
  const newEntity = {
    collegeCode: event.data.collegeCode,
    collegeName: event.data.collegeName,
  };

  const fn = props.dialogType === 'add' ? useCreateEntity : useEditEntityDetails;

  const { data: messageData, error } = await fn(props.dialogType, newEntity);

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
  <UForm
    :validate="(state) => validateForm(state, 'college', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
    @submit="onSubmit"
  >
    <UFormField label="College Code" name="collegeCode" class="flex-1">
      <UInput v-model="state.collegeCode" class="w-full" />
    </UFormField>

    <UFormField label="College Name" name="collegeName" class="flex-1">
      <UInput v-model="state.collegeName" class="w-full" />
    </UFormField>
  </UForm>
</template>
