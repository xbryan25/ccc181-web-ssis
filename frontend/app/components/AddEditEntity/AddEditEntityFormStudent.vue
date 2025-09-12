<script setup lang="ts">
import type { FormError, FormSubmitEvent, SelectMenuItem } from '@nuxt/ui';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

interface StudentFormState {
  idNumber: string;
  firstName: string;
  lastName: string;
  yearLevel: { label: string };
  gender: { label: string };
  programCode: { label: string };
}

const state = reactive<StudentFormState>({
  idNumber: '',
  firstName: '',
  lastName: '',
  yearLevel: {
    label: '1st',
  },
  gender: {
    label: 'Male',
  },
  programCode: {
    label: 'BSCS',
  },
});

const idNumberRegex = /^\d{4}-\d{4}$/;
const nameRegex = /^[A-Za-z- ]+$/;

const validate = (state: StudentFormState): FormError[] => {
  if (!hasCalled) return [];

  const errors = [];
  if (!state.idNumber) {
    errors.push({ name: 'idNumber', message: 'Required.' });
  } else if (state.idNumber && !idNumberRegex.test(state.idNumber)) {
    errors.push({
      name: 'idNumber',
      message: 'ID number format is XXXX-XXXX.',
    });
  }

  if (!state.firstName) {
    errors.push({ name: 'firstName', message: 'Required.' });
  } else if (state.firstName && !nameRegex.test(state.firstName)) {
    errors.push({
      name: 'firstName',
      message: 'Letters, spaces, and dashes only.',
    });
  }

  if (!state.lastName) {
    errors.push({ name: 'lastName', message: 'Required.' });
  } else if (state.lastName && !nameRegex.test(state.lastName)) {
    errors.push({
      name: 'lastName',
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

const yearLevelOptions = ref([
  {
    label: '1st',
  },
  {
    label: '2nd',
  },
  {
    label: '3rd',
  },
  {
    label: '4th',
  },
  {
    label: '4th+',
  },
]);

const genderOptions = ref([
  {
    label: 'Male',
  },
  {
    label: 'Female',
  },
  {
    label: 'Others',
  },
  {
    label: 'Prefer not to say',
  },
]);

const programCodeOptions = ref<SelectMenuItem[]>([
  {
    type: 'label',
    label: 'CCS',
  },
  {
    label: 'BSCS',
  },
  {
    label: 'BSCA',
  },
  {
    label: 'BSIS',
  },
  {
    label: 'BSIT',
  },
  {
    type: 'separator',
  },
  {
    type: 'label',
    label: 'COE',
  },
  {
    label: 'BSCE',
  },
]);

let hasCalled = false;

const apiUrl = import.meta.env.VITE_API_URL;

const getStudentDetails = () => {
  return useFetch(`${apiUrl}/api/college/`, {
    method: 'GET',
    params: {
      studentIdNumber: props.selectedEntity,
    },
  });
};

onMounted(() => {
  if (props.dialogType === 'edit') {
    // const { data: collegeData, pending, error } = getStudentDetails();
    // Object.assign(state, collegeData);
    console.log('Data loaded', state);
  }

  hasCalled = true;
});
</script>

<template>
  <UForm :validate="validate" :state="state" class="flex flex-col space-y-4" @submit="onSubmit">
    <div class="flex gap-4 w-full">
      <UFormField label="ID Number" name="idNumber" class="flex-1">
        <UInput v-model="state.idNumber" />
      </UFormField>

      <UFormField label="Year Level" name="yearLevel" class="flex-1">
        <USelectMenu v-model="state.yearLevel" :items="yearLevelOptions" class="w-full" />
      </UFormField>
    </div>

    <div class="flex gap-4">
      <UFormField label="First Name" name="firstName">
        <UInput v-model="state.firstName" />
      </UFormField>

      <UFormField label="Last Name" name="lastName">
        <UInput v-model="state.lastName" />
      </UFormField>
    </div>

    <div class="flex gap-4">
      <UFormField label="Gender" name="gender" class="flex-1">
        <USelectMenu v-model="state.gender" :items="genderOptions" class="w-full" />
      </UFormField>

      <UFormField label="Program Code" name="programCode" class="flex-1">
        <USelectMenu
          v-model="state.programCode"
          :items="programCodeOptions"
          class="w-full"
          :ui="{
            trailingIcon: 'group-data-[state=open]:rotate-180 transition-transform duration-200',
            label: 'text-green-400 ',
          }"
        />
      </UFormField>
    </div>
  </UForm>
</template>
