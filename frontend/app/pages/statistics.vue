<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div>
    <div class="flex flex-col gap-10 h-full">
      <h1 class="font-bold text-5xl">Statistics</h1>

      <GeneralStatistics />

      <StudentsStatistics />

      <ProgramsStatistics />

      <CollegesStatistics />
    </div>

    <div class="flex justify-center h-20 pt-10">
      <p class="text-primary">
        Made with love by
        <a
          href="https://github.com/xbryan25"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-block underline transition-transform duration-300 hover:scale-105"
        >
          @xbryan25
        </a>
      </p>
    </div>
  </div>
</template>
