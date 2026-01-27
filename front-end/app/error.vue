<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps<{
  error: NuxtError
}>()

const is404 = computed(() => props.error?.statusCode === 404)

function goHome() {
  clearError({ redirect: '/' })
}

function goBack() {
  
  clearError()
  if (import.meta.client) window.history.back()
}
</script>

<template>
  <div
    class="min-h-screen w-full flex items-center justify-center px-4 py-10
           bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100"
  >
    <div class="w-full max-w-2xl">
      <Card class="rounded-2xl shadow-2xl overflow-hidden">
        <template #content>
          <div class="p-8 sm:p-10">
            <!-- Header -->
            <div class="flex items-start gap-4">
              <div
                class="flex h-12 w-12 items-center justify-center rounded-xl
                       bg-slate-900 border border-slate-800"
              >
                <i class="pi pi-exclamation-triangle text-xl text-yellow-400"></i>
              </div>

              <div class="flex-1">
                <div class="flex items-baseline gap-3">
                  <h1 class="text-3xl sm:text-4xl font-semibold">
                    {{ is404 ? 'Page not found' : 'Something went wrong' }}
                  </h1>
                  <span
                    class="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium
                           bg-slate-900 border border-slate-800 text-slate-300"
                  >
                    {{ props.error?.statusCode || 500 }}
                  </span>
                </div>

                <p class="mt-2 text-slate-300 leading-relaxed">
                  <span v-if="is404">
                    The page you’re looking for doesn’t exist, or the link is broken.
                  </span>
                  <span v-else>
                    {{ props.error?.message || 'An unexpected error occurred.' }}
                  </span>
                </p>
              </div>
            </div>

            <Divider class="my-7" />

            <!-- Helpful actions -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <Button
                label="Go to Home"
                icon="pi pi-home"
                class="w-full"
                severity="help"
                @click="goHome"
              />
              <Button
                label="Go Back"
                icon="pi pi-arrow-left"
                class="w-full"
                severity="secondary"
                outlined
                @click="goBack"
              />
            </div>

            
            <div class="mt-6 flex flex-wrap items-center gap-3 text-sm text-slate-400">
              <span class="inline-flex items-center gap-2">
                <i class="pi pi-info-circle"></i>
                Tip:
              </span>
              <span>Check the URL or return to a safe page.</span>
            </div>

            <div class="mt-6">
              <span class="p-input-icon-left w-full">
                <i class="pi pi-search" />
                <InputText
                  class="w-full"
                  placeholder="Search (optional) …"
                  disabled
                />
              </span>
              <p class="mt-2 text-xs text-slate-500">
                (Wire this to your search page later)
              </p>
            </div>
          </div>
        </template>
      </Card>

      <!-- Footer -->
      <div class="mt-6 text-center text-xs text-slate-500">
        {{ new Date().getFullYear() }} • Your App Name
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Make PrimeVue Card match dark background nicely */
:deep(.p-card) {
  background: rgba(15, 23, 42, 0.9); /* slate-900-ish */
  border: 1px solid rgba(51, 65, 85, 0.5); /* slate-700-ish */
}
:deep(.p-divider.p-divider-horizontal:before) {
  border-top-color: rgba(51, 65, 85, 0.6);
}
</style>
