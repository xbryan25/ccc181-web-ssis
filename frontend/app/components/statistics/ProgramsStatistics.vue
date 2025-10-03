<script setup lang="ts">
import { VisSingleContainer, VisTooltip, VisDonut, VisBulletLegend } from '@unovis/vue';
import { Donut } from '@unovis/ts';
import type { SelectMenuItem } from '@nuxt/ui';
import type { UseProgramCodesResponse } from '~/types';

const triggers = {
  [Donut.selectors.segment]: (d: { data: { label: string; value: number } }) => {
    console.log(d);
    return `${d.data.label}: ${d.data.value}`;
  },
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

const programCodeOptions = ref<SelectMenuItem[]>([]);
const selectedProgramCode = ref({
  label: '',
});

const studentsTotalCount: Ref<number> = ref(0);

const yearLevelData = ref<{ label: string | undefined; value: number | undefined }[]>([]);

const genderData = ref<{ label: string | undefined; value: number | undefined }[]>([]);

onMounted(async () => {
  const programCodesDetailsData: UseProgramCodesResponse[] = (await useEntityIds(
    'programs',
  )) as UseProgramCodesResponse[];

  programCodeOptions.value = formatProgramCodesForSelectMenu(programCodesDetailsData);

  selectedProgramCode.value.label = programCodesDetailsData[0]?.programCodes[0] as string;

  ({ totalCount: studentsTotalCount.value } = await useEntitiesCount('students', {
    filterBy: { programCode: selectedProgramCode.value.label },
  }));

  yearLevelData.value = formatForYearLevelDonutChart(
    await useYearLevelDemographics({ programCode: selectedProgramCode.value.label }),
  );

  genderData.value = formatForGenderDonutChart(
    await useGenderDemographics({ programCode: selectedProgramCode.value.label }),
  );
});

watch(
  () => selectedProgramCode.value.label,
  async (newSelectedProgramCode) => {
    ({ totalCount: studentsTotalCount.value } = await useEntitiesCount('students', {
      filterBy: { programCode: newSelectedProgramCode },
    }));

    yearLevelData.value = formatForYearLevelDonutChart(
      await useYearLevelDemographics({ programCode: selectedProgramCode.value.label }),
    );

    genderData.value = formatForGenderDonutChart(
      await useGenderDemographics({ programCode: selectedProgramCode.value.label }),
    );
  },
);
</script>

<template>
  <div class="flex flex-col items-center gap-4 px-[10%] w-300">
    <USeparator color="primary" type="solid">
      <h2 class="font-bold text-4xl">Programs</h2>
    </USeparator>

    <USelectMenu
      v-model="selectedProgramCode"
      :items="programCodeOptions"
      class="w-75"
      :ui="{
        trailingIcon: 'group-data-[state=open]:rotate-180 transition-transform duration-200',
        label: 'text-green-400 ',
      }"
    />

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
      class="w-75 transition-transform duration-300 hover:scale-105"
    >
      <div class="flex items-center gap-2">
        <span class="text-2xl font-semibold text-highlighted"> {{ studentsTotalCount }} </span>
      </div>
    </UPageCard>

    <div class="flex flex-col xl:flex-row gap-10 w-full pt-5">
      <div class="flex-1 flex flex-col items-center gap-3 max-w-full">
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
