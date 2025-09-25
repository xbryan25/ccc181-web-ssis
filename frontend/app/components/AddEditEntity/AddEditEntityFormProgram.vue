<script setup lang="ts">
import type { Program, ProgramFormState, UseCollegeCodesResponse } from '~/types';

import { validateForm, formatCollegeCodesForSelectMenu } from '#imports';
import type { SelectMenuItem } from '@nuxt/ui';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
  toSubmit: boolean;
}>();

const state = reactive<ProgramFormState>({
  programCode: '',
  programName: '',
  collegeCode: {
    label: '',
  },
});

const transformProgramState = () => {
  return {
    programCode: state.programCode,
    programName: state.programName,
    collegeCode: state.collegeCode.label,
  };
};

const emit = defineEmits<{
  (e: 'onSubmit', newEntity: Program): void;
}>();

const collegeCodeOptions = ref<SelectMenuItem[]>([]);

let hasCalled = false;

onMounted(async () => {
  if (props.dialogType === 'edit') {
    const entityData = await useEntityDetails('programs', props.selectedEntity as string);

    state.programCode = entityData.programCode;
    state.programName = entityData.programName;
    state.collegeCode.label = entityData.collegeCode ? entityData.collegeCode : '';
  }

  const collegeCodesDetailsData: UseCollegeCodesResponse[] = (await useEntityIds(
    'colleges',
  )) as UseCollegeCodesResponse[];

  collegeCodeOptions.value = formatCollegeCodesForSelectMenu(collegeCodesDetailsData);

  if (state.collegeCode.label === '') {
    state.collegeCode.label = collegeCodesDetailsData[0]?.collegeCode as string;
  }

  hasCalled = true;
});

watch(
  () => props.toSubmit,
  (val) => {
    if (val) {
      emit('onSubmit', transformProgramState());
    }
  },
);
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'program', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
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
