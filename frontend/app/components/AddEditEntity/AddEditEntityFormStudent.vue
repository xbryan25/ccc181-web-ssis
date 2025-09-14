<script setup lang="ts">
import type { FormSubmitEvent, SelectMenuItem } from '@nuxt/ui';
import type { StudentFormState } from '~/types';

import { validateForm } from '#imports';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

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

const toast = useToast();

async function onSubmit(event: FormSubmitEvent<typeof state>) {
  const newEntity = {
    idNumber: event.data.idNumber,
    firstName: event.data.firstName,
    lastName: event.data.lastName,
    yearLevel: event.data.yearLevel.label,
    gender: event.data.gender.label,
    programCode: event.data.programCode.label,
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

onMounted(() => {
  if (props.dialogType === 'edit') {
    const { data: studentData } = useEntityDetails(
      props.dialogType,
      props.selectedEntity as string,
    );
    Object.assign(state, studentData);
    console.log('Data loaded', state);
  }

  hasCalled = true;
});
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'student', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
    @submit="onSubmit"
  >
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
