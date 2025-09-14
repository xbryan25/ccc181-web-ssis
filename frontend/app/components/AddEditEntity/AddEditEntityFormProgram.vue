<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

import { validateForm } from '#imports';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

interface ProgramFormState {
  programCode: string;
  programName: string;
  collegeCode: { label: string };
}

const state = reactive<ProgramFormState>({
  programCode: '',
  programName: '',
  collegeCode: {
    label: 'CCS',
  },
});

const toast = useToast();

async function onSubmit(event: FormSubmitEvent<typeof state>) {
  const newEntity = {
    programCode: event.data.programCode,
    programName: event.data.programName,
    collegeCode: event.data.collegeCode.label,
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

const collegeCodeOptions = ref([
  {
    label: 'CCS',
  },
  {
    label: 'COE',
  },
  {
    label: 'CHS',
  },
  {
    label: 'CEBA',
  },
  {
    label: 'CSM',
  },
]);

let hasCalled = false;

onMounted(async () => {
  if (props.dialogType === 'edit') {
    const { data: programData } = await useEntityDetails(
      props.dialogType,
      props.selectedEntity as string,
    );

    Object.assign(state, programData);
    console.log('Data loaded', state);
  }

  hasCalled = true;
});
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'program', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
    @submit="onSubmit"
  >
    <UFormField label="Program Code" name="programCode" class="flex-1">
      <UInput v-model="state.programCode" class="w-full" />
    </UFormField>

    <UFormField label="Program Name" name="programName" class="flex-1">
      <UInput v-model="state.programName" class="w-full" />
    </UFormField>

    <UFormField label="College Code" name="collegeCode" class="flex-1">
      <USelectMenu v-model="state.collegeCode" :items="collegeCodeOptions" class="w-full" />
    </UFormField>
  </UForm>
</template>
