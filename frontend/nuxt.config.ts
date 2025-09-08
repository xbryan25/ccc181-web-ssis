import Aura from '@primeuix/themes/aura';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: [
    '@nuxt/devtools',
    '@nuxt/icon',
    '@nuxtjs/tailwindcss',
    '@nuxt/eslint',
    '@primevue/nuxt-module'
  ],
  primevue: {
      options: {
          theme: {
              preset: Aura
          }
      }
  },
  icon: {
    mode: 'css',
    cssLayer: 'base'
  }
})