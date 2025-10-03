<script setup lang="ts">
import { VisSingleContainer, VisTooltip, VisDonut, VisBulletLegend } from '@unovis/vue';
import { Donut } from '@unovis/ts';
import type { SelectMenuItem } from '@nuxt/ui';
import type { UseCollegeCodesResponse } from '~/types';

const triggers = {
  [Donut.selectors.segment]: (d: { data: { label: string; value: number } }) =>
    `${d.data.label}: ${d.data.value}`,
};

const value = (d: { label: string; value: number }) => d.value;

const yearLevelLegendItems = [
  { name: '1st' },
  { name: '2nd' },
  { name: '3rd' },
  { name: '4th' },
  { name: '4th+' },
];
const genderLegendItems = [
  { name: 'Male' },
  { name: 'Female' },
  { name: 'Others' },
  { name: 'Prefer not to say' },
];

const collegeCodeOptions = ref<SelectMenuItem[]>([]);
const selectedCollegeCode = ref({
  label: '',
});

const studentsTotalCount: Ref<number> = ref(0);
const programsTotalCount: Ref<number> = ref(0);

const yearLevelData = ref<{ label: string | undefined; value: number | undefined }[]>([]);

const genderData = ref<{ label: string | undefined; value: number | undefined }[]>([]);

onMounted(async () => {
  const collegeCodesDetailsData: UseCollegeCodesResponse[] = (await useEntityIds(
    'colleges',
  )) as UseCollegeCodesResponse[];

  collegeCodeOptions.value = formatCollegeCodesForSelectMenu(collegeCodesDetailsData);

  selectedCollegeCode.value.label = collegeCodesDetailsData[0]?.collegeCode as string;

  ({ totalCount: studentsTotalCount.value } = await useEntitiesCount('students', {
    filterBy: { collegeCode: selectedCollegeCode.value.label },
  }));

  ({ totalCount: programsTotalCount.value } = await useEntitiesCount('programs', {
    filterBy: { collegeCode: selectedCollegeCode.value.label },
  }));

  yearLevelData.value = formatForYearLevelDonutChart(
    await useYearLevelDemographics({ collegeCode: selectedCollegeCode.value.label }),
  );

  genderData.value = formatForGenderDonutChart(
    await useGenderDemographics({ programCode: selectedCollegeCode.value.label }),
  );
});

watch(
  () => selectedCollegeCode.value.label,
  async (newSelectedCollegeCode) => {
    ({ totalCount: studentsTotalCount.value } = await useEntitiesCount('students', {
      filterBy: { collegeCode: newSelectedCollegeCode },
    }));

    ({ totalCount: programsTotalCount.value } = await useEntitiesCount('programs', {
      filterBy: { collegeCode: selectedCollegeCode.value.label },
    }));

    yearLevelData.value = formatForYearLevelDonutChart(
      await useYearLevelDemographics({ collegeCode: newSelectedCollegeCode }),
    );

    genderData.value = formatForGenderDonutChart(
      await useGenderDemographics({ collegeCode: newSelectedCollegeCode }),
    );
  },
);
</script>

<template>
  <div class="flex flex-col items-center gap-4 px-[10%] w-300">
    <USeparator color="primary" type="solid">
      <h2 class="font-bold text-4xl">Colleges</h2>
    </USeparator>

    <USelectMenu
      v-model="selectedCollegeCode"
      :items="collegeCodeOptions"
      class="w-75"
      :ui="{
        trailingIcon: 'group-data-[state=open]:rotate-180 transition-transform duration-200',
        label: 'text-green-400 ',
      }"
    />

    <div class="flex gap-10 flex-col lg:flex-row">
      <UPageCard
        icon="solar:square-academic-cap-2-bold"
        title="Students"
        variant="subtle"
        :ui="{
          container: 'gap-y-1.5',
          wrapper: 'items-start',
          leading: 'p-2.5 rounded-full bg-primary/10 ring ring-inset ring-primary/25 flex-col',
          title: 'font-bold text-md',
        }"
        class="flex-1 w-75 transition-transform duration-300 hover:scale-105"
      >
        <div class="flex items-center gap-2">
          <span class="text-2xl font-semibold text-highlighted"> {{ studentsTotalCount }}</span>
        </div>
      </UPageCard>

      <UPageCard
        icon="solar:book-2-bold-duotone"
        title="Programs"
        variant="subtle"
        :ui="{
          container: 'gap-y-1.5',
          wrapper: 'items-start',
          leading: 'p-2.5 rounded-full bg-primary/10 ring ring-inset ring-primary/25 flex-col',
          title: 'font-bold text-md',
        }"
        class="flex-1 w-75 transition-transform duration-300 hover:scale-105"
      >
        <div class="flex items-center gap-2">
          <span class="text-2xl font-semibold text-highlighted"> {{ programsTotalCount }} </span>
        </div>
      </UPageCard>
    </div>

    <div class="flex flex-col xl:flex-row gap-10 w-full pt-5">
      <div class="flex-1 flex flex-col items-center gap-3">
        <VisBulletLegend :items="yearLevelLegendItems" />
        <VisSingleContainer :data="yearLevelData" class="h-50 max-w-100">
          <VisTooltip :triggers="triggers" />
          <VisDonut :value="value" />
        </VisSingleContainer>
      </div>

      <div class="flex-1 flex flex-col items-center gap-3">
        <VisBulletLegend :items="genderLegendItems" />
        <VisSingleContainer :data="genderData" class="h-50 max-w-100">
          <VisTooltip :triggers="triggers" />
          <VisDonut :value="value" />
        </VisSingleContainer>
      </div>
    </div>
  </div>
</template>

<style scoped>
.unovis-single-container {
  --vis-tooltip-background-color: var(--ui-bg);
  --vis-tooltip-border-color: var(--ui-border);
  --vis-tooltip-text-color: var(--ui-text-highlighted);
}
</style>
