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
    iconName: "solar:square-academic-cap-2-bold",
  },
  {
    url: "/manage/programs",
    buttonName: "Programs",
    iconName: "solar:book-2-bold-duotone",
  },
  {
    url: "/manage/colleges",
    buttonName: "Colleges",
    iconName: "solar:buildings-2-bold",
  },
  {
    url: "/statistics",
    buttonName: "Statistics",
    iconName: "solar:chart-2-bold",
  },
  {
    url: "/about",
    buttonName: "About",
    iconName: "solar:info-square-bold",
  },
];
</script>

<template>
  <div class="flex h-screen">
    <div class="flex flex-col w-64 bg-stone-800">
      <div class="flex justify-center items-center bg-green-700 py-5 px-1">
        <Icon name="simple-icons:progress" class="flex-1 w-10 h-10" />
        <p class="flex-[3] font-bold text-4xl font-rethink">Sequence</p>
      </div>

      <nav class="flex flex-col gap-3 px-3 py-5 h-full">
        <NavBarButtons
          v-for="(buttonDetails, index) in navBarButtonDetails"
          :key="index"
          :url="buttonDetails.url"
          :button-name="buttonDetails.buttonName"
          :icon-name="buttonDetails.iconName"
        />
      </nav>
    </div>

    <div class="flex-1 px-6 py-4 overflow-auto">
      <NuxtPage />
    </div>
  </div>
</template>
