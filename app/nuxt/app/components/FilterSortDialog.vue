<script setup lang="ts">
import type { UseProgramCodesResponse } from '~/types';
import type { FormSubmitEvent, SelectMenuItem } from '@nuxt/ui';

type EntityPropertiesOptions = Record<string, string[]>;

type BasicSelectMenuItem = string | { label?: string; type?: 'label' | 'separator' };

const props = defineProps<{
  entityType: string;
  dialogType: string;
  searchAndSortState: {
    searchBy: string;
    searchType: string;
    filterByGender: string;
    filterByYearLevel: string;
    filterByProgramCode: string;
    sortField: string;
    sortOrder: string;
  };
}>();

const emit = defineEmits<{
  (
    e: 'onProceed',
    localState: {
      searchBy: string;
      searchType: string;
      filterByGender: string;
      filterByYearLevel: string;
      filterByProgramCode: string;
      sortField: string;
      sortOrder: string;
    },
  ): void;
}>();

const isOpen = ref(false);

const localState = reactive({ ...props.searchAndSortState });

const entityPropertiesOptions: EntityPropertiesOptions = {
  students: ['ID Number', 'First Name', 'Last Name', 'Year Level', 'Gender', 'Program Code'],
  programs: ['Program Code', 'Program Name', 'College Code'],
  colleges: ['College Code', 'College Name'],
};

const searchFilterTypes = ['Starts With', 'Ends With', 'Contains'];

const sortTypes = ['Ascending', 'Descending'];

const getTextForTooltip = (): string => {
  if (props.dialogType === 'searchFilter') {
    return `Search By: ${localState.searchBy} | Search Type: ${localState.searchType}`;
  } else if (props.dialogType === 'sort') {
    return `Sort Field: ${localState.sortField} | Sort Order: ${localState.sortOrder}`;
  } else {
    return 'Filter entries';
  }
};

const programCodeOptions = ref<SelectMenuItem[]>([]);
let programCodesDetailsData: UseProgramCodesResponse[];

const isDropdownOpen = ref(false);

const searchValue: Ref<string> = ref<string>('');
const effectiveSearchValue = ref('');

const localGender = ref<{ label: string }>({ label: 'All' });
const localYearLevel = ref<{ label: string }>({ label: 'All' });
const localProgramCode = ref<{ label: string }>({ label: 'All' });

const yearLevelOptions = ref([
  {
    label: 'All',
  },
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
    label: 'All',
  },
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

const getTextFromSelectMenuItem = (item: BasicSelectMenuItem): string => {
  if (typeof item === 'string') return item;
  if (item.type === 'label' || !item.type) return item.label ?? '';
  return '';
};

// Watcher for searchAndSortState changes
watch(
  () => props.searchAndSortState,
  (newVal) => {
    Object.assign(localState, newVal);
  },
  { deep: true, immediate: true },
);

onMounted(async () => {
  programCodesDetailsData = (await useEntityIds('programs')) as UseProgramCodesResponse[];

  programCodeOptions.value = formatProgramCodesForSelectMenu(programCodesDetailsData);
});
</script>

<template>
  <div>
    <UModal v-model:open="isOpen">
      <UTooltip
        :content="{
          align: 'center',
          side: 'top',
          sideOffset: 8,
        }"
        arrow
        :ui="{ content: 'data-[state=delayed-open]:animate-none data-[state=closed]:animate-none' }"
      >
        <template #content>
          {{ getTextForTooltip() }}
        </template>
        <UButton
          :icon="
            props.dialogType === 'filter'
              ? 'solar:filter-linear'
              : props.dialogType === 'searchFilter'
                ? 'solar:magnifer-linear'
                : 'solar:sort-linear'
          "
          size="md"
          color="primary"
          variant="solid"
          class="cursor-pointer"
          @click="isOpen = true"
          >{{
            props.dialogType === 'filter'
              ? 'Filters'
              : props.dialogType === 'searchFilter'
                ? 'Search Filters'
                : 'Sort Options'
          }}
        </UButton>
      </UTooltip>

      <template #header>
        <h2 v-if="props.dialogType === 'filter'" class="text-3xl font-semibold">Filters</h2>

        <h2 v-else-if="props.dialogType === 'searchFilter'" class="text-3xl font-semibold">
          Search Filters
        </h2>

        <h2 v-else class="text-3xl font-semibold">Sort Options</h2>
      </template>

      <template #body>
        <div>
          <div
            class="flex-col"
            :class="
              props.dialogType === 'searchFilter' || props.dialogType === 'sort' ? 'mb-12' : 'mb-5'
            "
          >
            <div v-if="props.dialogType === 'searchFilter'" class="w-full flex gap-4 mb-2">
              <h3 class="flex-1 text-lg font-medium">Search By</h3>
              <h3 class="flex-1 text-lg font-medium">Search Type</h3>
            </div>
            <div v-else-if="props.dialogType === 'filter'" class="w-full flex gap-4 mb-2">
              <h3 class="flex-1 text-lg font-medium">Filter By</h3>
              <!-- <h3 class="flex-1 text-lg font-medium">Search Type</h3> -->
            </div>
            <div v-else class="w-full flex gap-4 mb-2">
              <h3 class="flex-1 text-lg font-medium">Sort Field</h3>
              <h3 class="flex-1 text-lg font-medium">Sort Order</h3>
            </div>
            <div
              v-if="props.dialogType === 'searchFilter' || props.dialogType === 'sort'"
              class="w-full flex gap-4 mb-2"
            >
              <div class="flex-1 h-[2px] bg-primary" />
              <div class="flex-1 h-[2px] bg-primary" />
            </div>
            <div v-else class="w-full grid grid-cols-2 gap-4 mb-2">
              <div class="flex-1 h-[2px] bg-primary" />
              <!-- <div class="flex-1 h-[2px] bg-primary" /> -->
            </div>
            <div
              v-if="props.dialogType === 'searchFilter' || props.dialogType === 'sort'"
              class="w-full flex gap-4 mb-4"
            >
              <RadioSelectButtons
                :options="entityPropertiesOptions[props.entityType] ?? []"
                :dialog-type="props.dialogType"
                :column-position="'first'"
                :search-and-sort-state="localState"
                @update:search-by="(value: string) => (localState.searchBy = value)"
                @update:search-type="(value: string) => (localState.searchType = value)"
                @update:sort-field="(value: string) => (localState.sortField = value)"
                @update:sort-order="(value: string) => (localState.sortOrder = value)"
              />
              <RadioSelectButtons
                :options="props.dialogType === 'searchFilter' ? searchFilterTypes : sortTypes"
                :dialog-type="props.dialogType"
                :column-position="'second'"
                :search-and-sort-state="localState"
                @update:search-by="(value: string) => (localState.searchBy = value)"
                @update:search-type="(value: string) => (localState.searchType = value)"
                @update:sort-field="(value: string) => (localState.sortField = value)"
                @update:sort-order="(value: string) => (localState.sortOrder = value)"
              />
            </div>

            <div v-else class="flex flex-col gap-3 pt-5">
              <div class="flex gap-15">
                <p class="flex-1 font-semibold">By gender</p>

                <USelectMenu v-model="localGender" :items="genderOptions" class="flex-1" />
              </div>

              <div class="flex gap-15">
                <p class="flex-1 font-semibold">By year level</p>
                <USelectMenu v-model="localYearLevel" :items="yearLevelOptions" class="flex-1" />
              </div>

              <div class="flex gap-15">
                <p class="flex-1 font-semibold">By program code</p>
                <USelectMenu
                  v-model="localProgramCode"
                  v-model:search-term="searchValue"
                  :items="filteredItems"
                  ignore-filter
                  class="w-full h-8 flex-1"
                  :ui="{
                    trailingIcon:
                      'group-data-[state=open]:rotate-180 transition-transform duration-200',
                    label: 'text-primary',
                  }"
                  @update:open="isDropdownOpen = $event"
                />
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex justify-end gap-2 w-full">
          <UButton
            size="md"
            color="error"
            variant="solid"
            class="cursor-pointer"
            @click="isOpen = false"
            >Close</UButton
          >
          <UButton
            size="md"
            color="primary"
            variant="solid"
            class="cursor-pointer"
            @click="
              localState.filterByGender = localGender.label !== 'All' ? localGender.label : '';
              localState.filterByYearLevel =
                localYearLevel.label !== 'All' ? localYearLevel.label : '';
              localState.filterByProgramCode =
                localProgramCode.label !== 'All' ? localProgramCode.label : '';
              isOpen = false;
              emit('onProceed', localState);
            "
            >Proceed</UButton
          >
        </div>
      </template>
    </UModal>
  </div>
</template>
