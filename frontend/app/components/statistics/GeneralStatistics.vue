<script setup lang="ts"></script>

<template>
  <div class="flex flex-col items-center gap-4 px-[10%] w-300">
    <USeparator color="primary" type="solid">
      <h2 class="font-bold text-4xl">General</h2>
    </USeparator>

    <UPageGrid class="flex flex-col xl:flex-row gap-10 w-full items-center">
      <UPageCard
        v-for="n in 3"
        :key="n"
        icon="i-lucide-users"
        title="Test"
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
          <span class="text-2xl font-semibold text-highlighted"> 12 </span>
        </div>
      </UPageCard>
    </UPageGrid>
  </div>
</template>
