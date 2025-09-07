<script setup lang="ts">
import NavBarButtons from "~/components/NavBarButtons.vue";

interface NavBarDetails {
  url: string;
  buttonName: string;
  iconName: string;
}

const navBarButtonDetails: NavBarDetails[] = [
  {
    url: "/manage/students",
    buttonName: "Students",
    iconName: "solar:book-2-bold-duotone",
  },
  {
    url: "/manage/programs",
    buttonName: "Programs",
    iconName: "solar:buildings-2-bold",
  },
  {
    url: "/manage/colleges",
    buttonName: "Colleges",
    iconName: "solar:chart-2-bold",
  },
  {
    url: "/",
    buttonName: "Statistics",
    iconName: "solar:square-academic-cap-2-bold",
  },
];
</script>

<template>
  <div class="flex h-screen">
    <div class="flex flex-col w-64 bg-stone-800">
      <div class="flex justify-center items-center bg-green-600 py-5">
        <p class="font-bold text-3xl">Sequence</p>
      </div>

      <nav class="flex flex-col gap-3 px-3 pt-5">
        <NavBarButtons
          v-for="(buttonDetails, index) in navBarButtonDetails"
          :key="index"
          :url="buttonDetails.url"
          :button-name="buttonDetails.buttonName"
          :icon-name="buttonDetails.iconName"
        />
      </nav>
    </div>

    <div class="flex-1 p-6 overflow-auto">
      <NuxtPage />
    </div>
  </div>
</template>
