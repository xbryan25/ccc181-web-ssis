<script setup lang="ts">
import { navigateTo } from '#app';

import type { FormSubmitEvent } from '@nuxt/ui';

const props = defineProps<{
  authType: string;
}>();

const emit = defineEmits<{
  (e: 'onSubmitLogin', email: string, password: string): void;
  (e: 'onSubmitSignup', username: string, email: string, password: string): void;
}>();

const state = reactive({
  username: '',
  email: '',
  password: '',
});

const onSubmit = async (event: FormSubmitEvent<typeof state>) => {
  if (props.authType === 'login') {
    emit('onSubmitLogin', event.data.email, event.data.password);
  } else {
    emit('onSubmitSignup', event.data.username, event.data.email, event.data.password);
  }
};
</script>

<template>
  <div
    :class="[
      'flex flex-col bg-zinc-800 rounded-xl py-5 gap-4 w-96 ',
      props.authType === 'login' ? 'h-96 ' : 'h-115',
    ]"
  >
    <!-- Header -->
    <div class="flex justify-center items-center gap-2 text-primary">
      <Icon name="simple-icons:progress" class="w-7 h-7" />
      <h3 class="font-bold text-xl">Sequence</h3>
    </div>

    <!-- Text -->
    <div v-if="props.authType === 'signup'" class="flex flex-col justify-center items-center gap-1">
      <h2 class="font-bold text-2xl">Sign up to create an account</h2>
      <p class="text-base">Glad to have you onboard!</p>
    </div>

    <div v-else class="flex flex-col justify-center items-center gap-1">
      <h2 class="font-bold text-2xl">Login with your credentials</h2>
      <p class="text-base">Glad to have you back!</p>
    </div>

    <!-- Form -->
    <UForm :state="state" class="flex flex-col gap-4 px-6" @submit="onSubmit">
      <UFormField v-if="props.authType === 'signup'" label="Username" name="username">
        <UInput v-model="state.username" class="w-full" icon="tabler:user" />
      </UFormField>

      <UFormField label="Email" name="email">
        <UInput v-model="state.email" class="w-full" icon="tabler:mail" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput v-model="state.password" type="password" class="w-full" icon="tabler:lock" />
      </UFormField>

      <UButton type="submit" class="justify-center cursor-pointer bg-primary-500">{{
        props.authType === 'signup' ? 'Sign up' : 'Sign in'
      }}</UButton>
    </UForm>

    <!-- Signup/Sign in redirect -->
    <div class="flex justify-center items-center gap-2">
      <p v-if="props.authType === 'signup'" class="text-base">Already have an account?</p>
      <p v-else class="text-base">Don't have an account?</p>

      <p
        v-if="props.authType === 'signup'"
        class="text-base font-bold text-primary cursor-pointer"
        @click="navigateTo('/login')"
      >
        Sign Up
      </p>
      <p
        v-else
        class="text-base font-bold text-primary cursor-pointer"
        @click="navigateTo('/signup')"
      >
        Sign In
      </p>
    </div>
  </div>
</template>
