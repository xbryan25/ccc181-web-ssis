<script setup lang="ts">
import type { Program, ProgramFormState, UseCollegeCodesResponse } from '~/types';

import { validateForm, formatCollegeCodesForSelectMenu } from '#imports';
import type { SelectMenuItem } from '@nuxt/ui';

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

const state = reactive<ProgramFormState>({
  programCode: '',
  programName: '',
  collegeCode: {
    label: '',
  },
});

const emit = defineEmits<{
  (e: 'onSubmit', newEntity: Program): void;
  (e: 'onClose' | 'onSubmitError'): void;
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
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'program', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
    @submit="(event) => emit('onSubmit', event.data)"
    @error="emit('onSubmitError')"
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
