<script setup lang="ts">
import NavBarButtons from '~/components/NavBarButtons.vue';
import { useAuthStore } from '~/stores/useAuthStore';

import type { DropdownMenuItem } from '@nuxt/ui';

interface NavBarDetails {
  url: string;
  buttonName: string;
  iconName: string;
}

const colorMode = useColorMode();
const appConfig = useAppConfig();

const colors = [
  'red',
  'orange',
  'amber',
  'yellow',
  'lime',
  'green',
  'emerald',
  'teal',
  'cyan',
  'sky',
  'blue',
  'indigo',
  'violet',
  'purple',
  'fuchsia',
  'pink',
  'rose',
];
const neutrals = ['slate', 'gray', 'zinc', 'neutral', 'stone'];

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

const items = computed<DropdownMenuItem[][]>(() => [
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
          onSelect(e: Event) {
            e.preventDefault();
            colorMode.preference = 'dark';
          },
        },
      ],
    },
  ],
  [
    {
      label: 'Theme',
      icon: 'i-lucide-palette',
      children: [
        {
          label: 'Primary',
          slot: 'chip',
          chip: appConfig.ui.colors.primary,
          content: {
            align: 'center',
            collisionPadding: 16,
          },
          children: colors.map((color: string) => ({
            label: color.charAt(0).toUpperCase() + color.slice(1),
            chip: color,
            slot: 'chip',
            checked: appConfig.ui.colors.primary === color,
            type: 'checkbox',
            onSelect: (e: Event) => {
              e.preventDefault();

              appConfig.ui.colors.primary = color;
            },
          })),
        },
        {
          label: 'Neutral',
          slot: 'chip',
          chip:
            appConfig.ui.colors.neutral === 'neutral' ? 'old-neutral' : appConfig.ui.colors.neutral,
          content: {
            align: 'end',
            collisionPadding: 16,
          },
          children: neutrals.map((color) => ({
            label: color,
            chip: color === 'neutral' ? 'old-neutral' : color,
            slot: 'chip',
            type: 'checkbox',
            checked: appConfig.ui.colors.neutral === color,
            onSelect: (e) => {
              e.preventDefault();

              appConfig.ui.colors.neutral = color;
            },
          })),
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
    <div class="flex flex-col w-64 bg-elevated">
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
            content: 'w-(--reka-dropdown-menu-trigger-width) bg-default',
            item: 'cursor-pointer',
          }"
        >
          <UButton
            trailing-icon="i-lucide-menu"
            color="neutral"
            variant="ghost"
            class="flex w-full text-muted hover:bg-accented hover:text-primary active:bg-default active:text-primary"
          >
            <div class="flex-1 justify-items-start px-2">
              <p class="text-lg font-bold">{{ auth.username }}</p>
            </div>
          </UButton>

          <template #chip-leading="{ item }">
            <span
              :style="{
                '--chip-light': `var(--color-${(item as any).chip}-500)`,
                '--chip-dark': `var(--color-${(item as any).chip}-400)`,
              }"
              class="ms-0.5 size-2 rounded-full bg-(--chip-light) dark:bg-(--chip-dark)"
            />
          </template>
        </UDropdownMenu>
      </div>
    </div>

    <div class="flex-1 px-6 py-4 overflow-auto">
      <NuxtPage />
    </div>
  </div>
</template>
