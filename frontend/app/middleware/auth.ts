import { useAuthStore } from "~/stores/useAuthStore"

// This redirects users to login page if not logged in

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()
  const now = Date.now()

  try {
    // Refresh access token only if missing or near expiry (less than 1 min remaining)

    if (!auth.accessTokenExpiresAt || now > auth.accessTokenExpiresAt - 60_000) {
      let data;

      const event = useRequestEvent()    
      const cookie = event ? event.node.req.headers.cookie : ''   

      if (import.meta.server) {
        // SSR: forward incoming cookies
        data = await useRefreshAccessToken('server', cookie)
      } else {
        // Client: normal fetch with credentials
        data = await useRefreshAccessToken('client')
      }

      if (!auth.username) {
        const response = import.meta.server
          ? await useCurrentUser('server', cookie)
          : await useCurrentUser('client')
        auth.username = response.username
        auth.isAuthenticated = true
      }

      auth.accessTokenExpiresAt = data.accessTokenExpiresAt
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
