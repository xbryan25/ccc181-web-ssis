<script setup lang="ts">
import guest from '~/middleware/guest';
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  layout: 'auth',
  middleware: guest,
});

const toast = useToast();
const auth = useAuthStore();

const onSubmitSignup = async (username: string, email: string, password: string) => {
  try {
    const userSignupResponse = await useUserSignup(username, email, password);

    toast.add({
      title: userSignupResponse.messageTitle,
      description: userSignupResponse.message,
      color: 'success',
    });
  } catch (error) {
    toast.add({
      title: 'Signup failed.',
      description: error.data.error,
      color: 'error',
    });
  }
};
</script>

<template>
  <AuthForm
    auth-type="signup"
    @on-submit-signup="(username, email, password) => onSubmitSignup(username, email, password)"
  />
</template>
