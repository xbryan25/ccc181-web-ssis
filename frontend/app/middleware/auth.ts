import { useAuthStore } from "~/stores/useAuthStore"

// This redirects users to login page if not logged in

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()

  try {
    const response = await useCurrentUser('client')
    auth.username = response.username
    auth.isAuthenticated = true
  } catch {
    auth.username = null
    auth.isAuthenticated = false
    if (to.path !== '/login') {
      return navigateTo('/login')
    }
  }
})
