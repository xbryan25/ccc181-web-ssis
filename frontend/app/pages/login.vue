<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  layout: 'auth',
});

const state = reactive({
  email: '',
  password: '',
});

const toast = useToast();
const auth = useAuthStore();

const onSubmit = async (event: FormSubmitEvent<typeof state>) => {
  console.log(event.data);

  try {
    const userLoginMessage = await auth.login(event.data.email, event.data.password);

    toast.add({
      title: 'Login successful.',
      description: userLoginMessage,
      color: 'success',
    });
  } catch (error) {
    toast.add({
      title: 'Login failed.',
      description: error.data.error,
      color: 'error',
    });
  }
};
</script>

<template>
  <div class="flex flex-col bg-zinc-800 w-96 h-96 rounded-xl py-5 gap-4">
    <!-- Header -->
    <div class="flex justify-center items-center gap-2 text-primary">
      <Icon name="simple-icons:progress" class="w-7 h-7" />
      <h3 class="font-bold text-xl">Sequence</h3>
    </div>

    <!-- Text -->
    <div class="flex flex-col justify-center items-center gap-1">
      <h2 class="font-bold text-2xl">Login with your credentials</h2>
      <p class="text-base">Glad to have you back!</p>
    </div>

    <!-- Form -->
    <UForm :state="state" class="flex flex-col gap-4 px-6" @submit="onSubmit">
      <UFormField label="Email" name="email">
        <UInput v-model="state.email" class="w-full" icon="tabler:mail" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput v-model="state.password" type="password" class="w-full" icon="tabler:lock" />
      </UFormField>

      <UButton type="submit" class="justify-center cursor-pointer bg-primary-500">Sign in</UButton>
    </UForm>

    <div class="flex justify-center items-center gap-2">
      <p class="text-base">Don't have an account?</p>
      <p class="text-base font-bold text-primary cursor-pointer">Sign Up</p>
    </div>
  </div>
</template>
