<script setup lang="ts">
import NavBarButtons from '~/components/NavBarButtons.vue';
import { useAuthStore } from '~/stores/useAuthStore';

interface NavBarDetails {
  url: string;
  buttonName: string;
  iconName: string;
}

const colorMode = useColorMode();

const auth = useAuthStore();

const navBarButtonDetails: NavBarDetails[] = [
  {
    url: '/manage/students',
    buttonName: 'Students',
    iconName: 'solar:square-academic-cap-2-bold',
  },
  {
    url: '/manage/programs',
    buttonName: 'Programs',
    iconName: 'solar:book-2-bold-duotone',
  },
  {
    url: '/manage/colleges',
    buttonName: 'Colleges',
    iconName: 'solar:buildings-2-bold',
  },
  {
    url: '/statistics',
    buttonName: 'Statistics',
    iconName: 'solar:chart-2-bold',
  },
  {
    url: '/about',
    buttonName: 'About',
    iconName: 'solar:info-square-bold',
  },
];

const items = ref([
  [
    {
      label: 'Appearance',
      icon: 'i-lucide-sun-moon',
      children: [
        {
          label: 'Light',
          icon: 'i-lucide-sun',
          type: 'checkbox',
          checked: colorMode.value === 'light',
          onSelect(e: Event) {
            e.preventDefault();

            colorMode.preference = 'light';
          },
        },
        {
          label: 'Dark',
          icon: 'i-lucide-moon',
          type: 'checkbox',
          checked: colorMode.value === 'dark',
          onUpdateChecked(checked: boolean) {
            if (checked) {
              colorMode.preference = 'dark';
            }
          },
          onSelect(e: Event) {
            e.preventDefault();
          },
        },
      ],
    },
  ],

  [
    {
      label: 'Logout',
      icon: 'i-lucide-log-out',
    },
  ],
]);
</script>

<template>
  <div class="flex h-screen">
    <div class="flex flex-col w-64 bg-stone-800">
      <div class="flex justify-center items-center py-5 px-1">
        <Icon name="simple-icons:progress text-primary" class="flex-1 w-10 h-10" />
        <p class="flex-[3] font-bold text-4xl font-rethink text-primary">Sequence</p>
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

      <div class="px-3 py-5">
        <UDropdownMenu
          :items="items"
          class="w-full cursor-pointer"
          :content="{ align: 'center', collisionPadding: 12 }"
          :ui="{
            content: 'w-(--reka-dropdown-menu-trigger-width) bg-stone-900',
            item: 'cursor-pointer',
          }"
        >
          <UButton
            trailing-icon="i-lucide-menu"
            color="neutral"
            variant="ghost"
            class="flex w-full bg-stone-800 text-zinc-500 hover:bg-zinc-700 hover:text-zinc-300 active:bg-stone-900 active:text-zinc-500"
          >
            <div class="flex-1 justify-items-start px-2">
              <p class="text-lg font-bold">{{ auth.username }}</p>
            </div>
          </UButton>
        </UDropdownMenu>
      </div>
    </div>

    <div class="flex-1 px-6 py-4 overflow-auto">
      <NuxtPage />
    </div>
  </div>
</template>
