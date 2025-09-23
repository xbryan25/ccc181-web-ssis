// stores/auth.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserLogin } from '~/composables/useUserLogin'

export const useAuthStore = defineStore('auth', () => {
  const username = ref<string | null>(null)
  const isAuthenticated = ref(false)

  const login = async (email: string, password: string): Promise<string> => {
    const response = await useUserLogin(email, password)

    username.value = response.username
    isAuthenticated.value = true

    return response.message
  }

  const logout = () => {
    username.value = null
    isAuthenticated.value = false
  }

  return { username, isAuthenticated, login, logout }
})