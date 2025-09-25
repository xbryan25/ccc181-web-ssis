<script setup lang="ts">
import guest from '~/middleware/guest';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  layout: 'auth',
  middleware: guest,
});

const toast = useToast();
const auth = useAuthStore();

const onSubmitLogin = async (email: string, password: string) => {
  try {
    const { messageTitle, message } = await auth.login(email, password);

    toast.add({
      title: messageTitle,
      description: message,
      color: 'success',
    });

    navigateTo('/manage/students');
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
  <AuthForm
    auth-type="login"
    @on-submit-login="(email, password) => onSubmitLogin(email, password)"
  />
</template>
