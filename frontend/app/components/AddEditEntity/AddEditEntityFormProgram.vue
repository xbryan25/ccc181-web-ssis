<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '@nuxt/ui';

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

const programCodeRegex = /^[A-Z-]+$/;
const programNameRegex = /^[A-Za-z- ]+$/;

const validate = (state: ProgramFormState): FormError[] => {
  if (!hasCalled) return [];

  const errors = [];
  if (!state.programCode) {
    errors.push({ name: 'programCode', message: 'Required.' });
  } else if (state.programCode && !programCodeRegex.test(state.programCode)) {
    errors.push({
      name: 'programCode',
      message: 'Uppercase letters & dashes only.',
    });
  }

  if (!state.programName) {
    errors.push({ name: 'programName', message: 'Required.' });
  } else if (state.programName && !programNameRegex.test(state.programName)) {
    console.log('reach here');
    errors.push({
      name: 'programName',
      message: 'Letters, spaces, and dashes only.',
    });
  }

  return errors;
};

const toast = useToast();
async function onSubmit(event: FormSubmitEvent<typeof state>) {
  toast.add({
    title: 'Success',
    description: 'The form has been submitted.',
    color: 'success',
  });
  console.log(event.data);
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

const apiUrl = import.meta.env.VITE_API_URL;

const getProgramDetails = () => {
  return useFetch(`${apiUrl}/api/college/`, {
    method: 'GET',
    params: {
      programCode: props.selectedEntity,
    },
  });
};

onMounted(() => {
  if (props.dialogType === 'edit') {
    // const { data: collegeData, pending, error } = getProgramDetails();
    // Object.assign(state, collegeData);
    console.log('Data loaded', state);
  }

  hasCalled = true;
});
</script>

<template>
  <UForm :validate="validate" :state="state" class="flex flex-col space-y-4" @submit="onSubmit">
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
