<script setup lang="ts">
const studentTotalCount = ref<number | string>('-');

const programTotalCount = ref<number | string>('-');

const collegeTotalCount = ref<number | string>('-');

const entitiesTotalCounts = [
  {
    entityTitle: 'Students',
    entityIcon: 'solar:square-academic-cap-2-bold',
    totalCount: studentTotalCount,
  },
  {
    entityTitle: 'Programs',
    entityIcon: 'solar:book-2-bold-duotone',
    totalCount: programTotalCount,
  },
  { entityTitle: 'Colleges', entityIcon: 'solar:buildings-2-bold', totalCount: collegeTotalCount },
];

onMounted(async () => {
  const [students, programs, colleges] = await Promise.all([
    useEntitiesCount('students'),
    useEntitiesCount('programs'),
    useEntitiesCount('colleges'),
  ]);

  studentTotalCount.value = students.totalCount;
  programTotalCount.value = programs.totalCount;
  collegeTotalCount.value = colleges.totalCount;
});
</script>

<template>
  <div class="flex flex-col items-center gap-4 px-[10%] w-300">
    <USeparator color="primary" type="solid">
      <h2 class="font-bold text-4xl">General</h2>
    </USeparator>

    <UPageGrid class="flex flex-col xl:flex-row gap-10 w-full items-center">
      <UPageCard
        v-for="(entity, index) in entitiesTotalCounts"
        :key="index"
        :icon="entity.entityIcon"
        :title="entity.entityTitle"
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
          <span class="text-2xl font-semibold text-highlighted"> {{ entity.totalCount }} </span>
        </div>
      </UPageCard>
    </UPageGrid>
  </div>
</template>
