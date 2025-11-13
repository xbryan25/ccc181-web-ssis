<script setup lang="ts">
import type { Gender, StudentFormState, UseProgramCodesResponse } from '~/types';

import { validateForm, capitalizeFirstWord, formatProgramCodesForSelectMenu } from '#imports';
import type { FormSubmitEvent, SelectMenuItem } from '@nuxt/ui';

type BasicSelectMenuItem = string | { label?: string; type?: 'label' | 'separator' };

const props = defineProps<{
  dialogType: string;
  selectedEntity?: string;
}>();

const state = reactive<StudentFormState>({
  avatar: null,
  existingAvatarUrl: null,
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

const isDropdownOpen = ref(false);

const searchValue: Ref<string> = ref<string>('');
const effectiveSearchValue = ref('');

const maxFileSize = 2 * 1024 * 1024; // 2MB

const toast = useToast();

const emit = defineEmits<{
  (e: 'onSubmit', newEntity: StudentFormState): void;
  (e: 'onClose' | 'onSubmitError'): void;
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
let programCodesDetailsData: UseProgramCodesResponse[];

let hasCalled = false;

const transformStudentState = (event: FormSubmitEvent<StudentFormState>) => {
  emit('onSubmit', {
    avatar: event.data.avatar,
    existingAvatarUrl: event.data.existingAvatarUrl,
    idNumber: event.data.idNumber,
    firstName: event.data.firstName,
    lastName: event.data.lastName,
    yearLevel: event.data.yearLevel,
    gender: event.data.gender,
    programCode: event.data.programCode,
  });
};

const getTextFromSelectMenuItem = (item: BasicSelectMenuItem): string => {
  if (typeof item === 'string') return item;
  if (item.type === 'label' || !item.type) return item.label ?? '';
  return '';
};

const filteredItems = computed(() => {
  if (!searchValue.value.trim()) return programCodeOptions.value;

  const lower = searchValue.value.toLowerCase();
  const result: BasicSelectMenuItem[] = [];
  let currentGroupHasMatch = false;
  let currentGroupLabel: BasicSelectMenuItem | null = null;

  for (const item of programCodeOptions.value as BasicSelectMenuItem[]) {
    if (typeof item === 'object' && item?.type === 'label') {
      currentGroupLabel = item;
      currentGroupHasMatch = false;
      continue;
    }

    if (typeof item === 'object' && item?.type === 'separator') {
      if (currentGroupHasMatch) result.push(item);
      currentGroupHasMatch = false;
      continue;
    }

    const text = getTextFromSelectMenuItem(item);

    if (text.toLowerCase().includes(lower)) {
      if (currentGroupLabel && !result.includes(currentGroupLabel)) {
        result.push(currentGroupLabel);
      }
      result.push(item);
      currentGroupHasMatch = true;
    }
  }

  result.pop();
  return result;
});

watch(
  () => state.avatar,
  (newAvatar: File | null) => {
    if (!newAvatar) return;

    if (newAvatar.size > maxFileSize) {
      state.avatar = null;

      toast.add({
        title: 'File Size Limit Exceeded',
        description: `Image was skipped because it exceed the 2 MB size limit.`,
        color: 'error',
      });
    }
  },
);

watch(searchValue, (newVal) => {
  if (newVal === '') {
    searchValue.value = effectiveSearchValue.value;
  } else {
    effectiveSearchValue.value = newVal;
  }
});

watch(
  () => isDropdownOpen.value,
  (newVal) => {
    if (newVal) {
      searchValue.value = '';
      effectiveSearchValue.value = '';
    }
  },
);

onMounted(async () => {
  if (props.dialogType === 'edit') {
    const entityData = await useEntityDetails('students', props.selectedEntity as string);

    state.existingAvatarUrl = entityData.avatarUrl;
    state.idNumber = entityData.idNumber;
    state.firstName = entityData.firstName;
    state.lastName = entityData.lastName;
    state.yearLevel.label = entityData.yearLevel;
    state.gender.label = capitalizeFirstWord(entityData.gender) as Gender;
    state.programCode.label = entityData.programCode ? entityData.programCode : '';
  }

  programCodesDetailsData = (await useEntityIds('programs')) as UseProgramCodesResponse[];

  programCodeOptions.value = formatProgramCodesForSelectMenu(programCodesDetailsData);

  if (state.programCode.label === '') {
    state.programCode.label = programCodesDetailsData[0]?.programCodes[0] as string;
  }

  hasCalled = true;
});
</script>

<template>
  <UForm
    :validate="(state) => validateForm(state, 'student', hasCalled)"
    :state="state"
    class="flex flex-col space-y-4"
    @submit="(event) => transformStudentState(event)"
    @error="emit('onSubmitError')"
  >
    <UFormField
      v-if="props.dialogType === 'edit' && state.existingAvatarUrl"
      label="Existing Avatar"
      name="existingAvatar"
      class="w-full min-h-48"
    >
      <div class="flex items-center justify-center w-full">
        <NuxtImg :src="`${state.existingAvatarUrl}`" class="rounded-full w-45 h-45 object-cover" />
        <UButton
          class="absolute -top-1.5 -right-1.5 w-5 h-5 p-0 flex items-center justify-center rounded-full bg-inverted text-xs cursor-pointer"
          type="button"
          @click="state.existingAvatarUrl = null"
        >
          <Icon name="i-lucide:x" class="w-4 h-4" />
        </UButton>
      </div>
    </UFormField>

    <UFormField
      :label="`${props.dialogType === 'edit' ? 'New Avatar' : 'Avatar (not required)'}`"
      name="avatar"
      class="flex-1"
    >
      <UFileUpload
        v-model="state.avatar"
        accept="image/*"
        label="Drop your image here"
        description="SVG, PNG, JPG or GIF (max. 2MB)"
        icon="i-lucide-image"
        position="inside"
        layout="list"
        class="w-full min-h-36"
      />
    </UFormField>

    <div class="flex gap-4 w-full">
      <UFormField label="ID Number" name="idNumber" class="flex-1">
        <UInput v-model="state.idNumber" class="w-full" />
      </UFormField>

      <UFormField label="Year Level" name="yearLevel" class="flex-1">
        <USelectMenu v-model="state.yearLevel" :items="yearLevelOptions" class="w-full" />
      </UFormField>
    </div>

    <div class="flex gap-4">
      <UFormField label="First Name" name="firstName" class="flex-1">
        <UInput v-model="state.firstName" class="w-full" />
      </UFormField>

      <UFormField label="Last Name" name="lastName" class="flex-1">
        <UInput v-model="state.lastName" class="w-full" />
      </UFormField>
    </div>

    <div class="flex gap-4">
      <UFormField label="Gender" name="gender" class="flex-1">
        <USelectMenu v-model="state.gender" :items="genderOptions" class="w-full" />
      </UFormField>

      <UFormField label="Program Code" name="programCode" class="flex-1">
        <USelectMenu
          v-model="state.programCode"
          v-model:search-term="searchValue"
          :items="filteredItems"
          ignore-filter
          class="w-full"
          :ui="{
            trailingIcon: 'group-data-[state=open]:rotate-180 transition-transform duration-200',
            label: 'text-primary',
          }"
          @update:open="isDropdownOpen = $event"
        />
      </UFormField>
    </div>

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
