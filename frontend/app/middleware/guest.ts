import { useAuthStore } from '~/stores/useAuthStore'

// This redirects users to /manage/students if already logged in

export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()

  console.log(`${auth.isAuthenticated ? 'Logged in' : 'Not logged in'}`)

  if (auth.isAuthenticated) {
    return navigateTo('/manage/students')
  }
})