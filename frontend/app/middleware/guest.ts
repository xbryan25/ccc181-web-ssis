import { useAuthStore } from '~/stores/useAuthStore'

// This redirects users to /manage/students if already logged in

export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()

  if (auth.isAuthenticated) {
    return navigateTo('/manage/students')
  }
})