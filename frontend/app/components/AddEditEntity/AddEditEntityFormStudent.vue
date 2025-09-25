<script setup lang="ts">
import type { Gender, Student, StudentFormState, UseProgramCodesResponse } from '~/types';

import { validateForm, capitalizeFirstWord, formatProgramCodesForSelectMenu } from '#imports';
import type { SelectMenuItem } from '@nuxt/ui';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
  toSubmit: boolean;
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
    label: '',
  },
});

const transformStudentState = () => {
  return {
    idNumber: state.idNumber,
    firstName: state.firstName,
    lastName: state.lastName,
    yearLevel: state.yearLevel.label,
    gender: state.gender.label,
    programCode: state.programCode.label,
  };
};

const emit = defineEmits<{
  (e: 'onSubmit', newEntity: Student): void;
}>();

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

const programCodeOptions = ref<SelectMenuItem[]>([]);

let hasCalled = false;

onMounted(async () => {
  if (props.dialogType === 'edit') {
    const entityData = await useEntityDetails('students', props.selectedEntity as string);

    state.idNumber = entityData.idNumber;
    state.firstName = entityData.firstName;
    state.lastName = entityData.lastName;
    state.yearLevel.label = entityData.yearLevel;
    state.gender.label = capitalizeFirstWord(entityData.gender) as Gender;
    state.programCode.label = entityData.programCode ? entityData.programCode : '';
  }

  const programCodesDetailsData: UseProgramCodesResponse[] = (await useEntityIds(
    'programs',
  )) as UseProgramCodesResponse[];

  programCodeOptions.value = formatProgramCodesForSelectMenu(programCodesDetailsData);

  if (state.programCode.label === '') {
    state.programCode.label = programCodesDetailsData[0]?.programCodes[0] as string;
  }

  hasCalled = true;
});

watch(
  () => props.toSubmit,
  (val) => {
    if (val) {
      emit('onSubmit', transformStudentState());
    }
  },
);
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'student', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
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
