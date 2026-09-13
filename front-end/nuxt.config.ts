import Aura from '@primeuix/themes/aura';
export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: false,
  imports: {
    autoImport: true
  },
  modules: [
    '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/hints',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    '@pinia/nuxt',
    '@primevue/nuxt-module',
    '@nuxtjs/tailwindcss',
    '@nuxtjs/i18n'
  ],
  css: [
    "primeicons/primeicons.css",
    "@/assets/main.css"
  ],
  fonts:{
    families:[
      {
        name: "Battambang",
        provider: "google",
        weights: [400, 500, 600],
        subsets:["khmer"]
      },
    ]
  },
  i18n: {
    defaultLocale: 'en',
    locales:[
      { code: 'en', name: 'English', file: 'en.ts'},
      { code: 'kh', name: 'Khmer', file: 'kh.ts'}
    ],
    langDir: 'locales/',
    strategy: 'no_prefix',
  },
  primevue:{
    autoImport: true,
    options: {
        ripple: true,
        inputVariant: 'filled',
        theme: {
            preset: Aura,
            options: {
                prefix: 'p',
                darkModeSelector: '.dark',
            }
        }
    }
  },
  plugins:[
    
  ],
  runtimeConfig:{
    URL_API: import.meta.env.BASE_URL
  }
})