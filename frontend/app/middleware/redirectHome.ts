import { useAuthStore } from '~/stores/useAuthStore'

// This redirects users to /manage/students if already logged in, else, redirect to /login

export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()

  if (auth.isAuthenticated) {
    return navigateTo('/manage/students')
  } else {
    return navigateTo('/login')
  }
})