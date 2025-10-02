<script setup lang="ts">
import { VisSingleContainer, VisTooltip, VisDonut, VisBulletLegend } from '@unovis/vue';
import { Donut } from '@unovis/ts';

const data = [
  { label: 'Male', value: 5 },
  { label: 'Female', value: 7 },
  { label: 'Other', value: 3 },
];

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
</script>

<template>
  <div class="flex flex-col items-center gap-4 px-[10%] w-300">
    <USeparator color="primary" type="solid">
      <h2 class="font-bold text-4xl">Students</h2>
    </USeparator>

    <UPageCard
      icon="i-lucide-users"
      title="Test"
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
        <span class="text-2xl font-semibold text-highlighted"> 12 </span>
      </div>
    </UPageCard>

    <div class="flex flex-col xl:flex-row gap-10 w-full pt-5">
      <div class="flex-1 flex flex-col items-center gap-3 max-w-full">
        <VisBulletLegend :items="yearLevelLegendItems" />
        <VisSingleContainer :data="data" class="h-50 max-w-100">
          <VisTooltip :triggers="triggers" />
          <VisDonut :value="value" />
        </VisSingleContainer>
      </div>

      <div class="flex-1 flex flex-col items-center gap-3">
        <VisBulletLegend :items="genderLegendItems" />
        <VisSingleContainer :data="data" class="h-50 max-w-100">
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
