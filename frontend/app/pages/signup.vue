<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuthStore';

definePageMeta({
  layout: 'auth',
});

const toast = useToast();
const auth = useAuthStore();

// const onSubmit = async (event: FormSubmitEvent<typeof state>) => {
//   console.log(event.data);

//   try {
//     const userLoginMessage = await auth.login(event.data.email, event.data.password);

//     toast.add({
//       title: 'Login successful.',
//       description: userLoginMessage,
//       color: 'success',
//     });
//   } catch (error) {
//     toast.add({
//       title: 'Login failed.',
//       description: error.data.error,
//       color: 'error',
//     });
//   }
// };
</script>

<template>
  <AuthForm auth-type="signup" />
</template>
