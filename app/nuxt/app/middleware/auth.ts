
import { useAuthStore } from '~/stores/useAuthStore'
import { useRefreshAccessToken, useCurrentUser } from '#imports'

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()
  const now = Date.now()

  // Skip during SSR
  if (import.meta.server) return

  try {
    // If accessToken had already exipired or it will expire in 30 seconds, create another accessToken

    if (!auth.accessTokenExpiresAt || now > auth.accessTokenExpiresAt - 30_000) {
      const data = await useRefreshAccessToken('client')
      auth.accessTokenExpiresAt = data.accessTokenExpiresAt

      if (!auth.username) {
        const response = await useCurrentUser('client')
        auth.username = response.username
        auth.isAuthenticated = true
      }
    }
  } catch {
    auth.username = null
    auth.isAuthenticated = false
    auth.accessTokenExpiresAt = null

    if (to.path !== '/login') {
      return navigateTo('/login')
    }
  }
})