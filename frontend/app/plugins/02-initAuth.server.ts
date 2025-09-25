import { useAuthStore } from '~/stores/useAuthStore'
import { useCurrentUser } from '#imports'

import type { H3Event } from 'h3'

export default defineNuxtPlugin(async (nuxtApp) => {
  const auth = useAuthStore()

  const event: H3Event | undefined = nuxtApp.ssrContext?.event

  try {
    const response = await useCurrentUser('server', event)
    auth.username = response.username
    auth.isAuthenticated = true
  } catch {
    auth.username = null
    auth.isAuthenticated = false
  }
})

