import { useAuthStore } from "~/stores/useAuthStore"

// This redirects users to login page if not logged in

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()
  const now = Date.now()

  try {
    // Refresh access token only if missing or near expiry (less than 1 min remaining)
    
    if (!auth.accessTokenExpiresAt || now > auth.accessTokenExpiresAt - 60_000) {
      const data = await useRefreshAccessToken()
      auth.accessTokenExpiresAt = data.accessTokenExpiresAt
    }

    const response = await useCurrentUser('client')
    auth.username = response.username
    auth.isAuthenticated = true

  } catch {

    auth.username = null
    auth.isAuthenticated = false
    auth.accessTokenExpiresAt = null

    if (to.path !== '/login') {
      return navigateTo('/login')
    }
  }
})
