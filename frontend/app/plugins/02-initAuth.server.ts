import { useAuthStore } from '~/stores/useAuthStore'
import { useCurrentUser } from '#imports'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()

  const event = useRequestEvent()
  const cookie = event ? event.node.req.headers.cookie : '' 

  try {
    const response = await useCurrentUser('server', cookie)
    auth.username = response.username
    auth.isAuthenticated = true
  } catch {
    auth.username = null
    auth.isAuthenticated = false
  }
})

