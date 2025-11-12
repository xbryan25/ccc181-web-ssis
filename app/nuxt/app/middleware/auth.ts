
import { useAuthStore } from '~/stores/useAuthStore'

// Works client-only

export default defineNuxtRouteMiddleware(async (to) => {
    const auth = useAuthStore()

    try {
        // Wait 10 seconds to refresh token again, if access token is removed while still in cooldown, redirect to login
        await safeRefresh()
        // await useRefreshAccessToken()
        const response = await useCurrentUser()
        auth.username = response.username
        auth.isAuthenticated = true

    } catch {
        auth.username = null
        auth.isAuthenticated = false

        if (to.path !== '/login') return navigateTo('/login')
    }
})