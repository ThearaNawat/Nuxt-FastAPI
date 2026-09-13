<template>
  <div class="auth-shell relative isolate min-h-screen overflow-hidden bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div class="auth-orb auth-orb-a"></div>
      <div class="auth-orb auth-orb-b"></div>
      <div class="auth-orb auth-orb-c"></div>
      <div class="absolute inset-0 bg-[linear-gradient(120deg,rgba(255,255,255,0.82),rgba(255,255,255,0.4)_45%,rgba(255,255,255,0.14)_70%,transparent)] dark:bg-[linear-gradient(120deg,rgba(2,6,23,0.86),rgba(2,6,23,0.6)_45%,rgba(2,6,23,0.34)_70%,transparent)]"></div>
      <div class="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-white/80 to-transparent dark:from-slate-950"></div>
    </div>

    <div class="absolute right-4 top-4 z-20 flex items-center gap-2 sm:right-6 sm:top-6">
      <Button
        :label="locale === 'kh' ? 'KH' : 'EN'"
        icon="pi pi-globe"
        severity="secondary"
        outlined
        rounded
        size="small"
        class="!px-4"
        @click="openLocaleMenu"
      />
      <Button
        :icon="theme !== 'dark' ? 'pi pi-moon' : 'pi pi-sun'"
        severity="secondary"
        outlined
        rounded
        size="small"
        class="!h-10 !w-10"
        @click="toggleTheme"
      />

      <Popover ref="localeMenu" :dismissable="true">
        <div class="flex min-w-44 flex-col gap-2 p-2">
          <Button
            label="English"
            size="small"
            variant="text"
            class="w-full !justify-start"
            :icon="locale === 'en' ? 'pi pi-check' : 'pi pi-globe'"
            :severity="locale === 'en' ? 'primary' : 'secondary'"
            @click="setAppLocale('en')"
          />
          <Button
            label="Khmer"
            size="small"
            variant="text"
            class="w-full !justify-start"
            :icon="locale === 'kh' ? 'pi pi-check' : 'pi pi-globe'"
            :severity="locale === 'kh' ? 'primary' : 'secondary'"
            @click="setAppLocale('kh')"
          />
        </div>
      </Popover>
    </div>

    <div class="relative mx-auto grid min-h-screen w-full max-w-7xl items-center gap-6 px-4 py-16 sm:px-6 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)] lg:gap-12 lg:px-8 lg:py-10">
      <section class="order-2 lg:order-1">
        <slot name="left" />
      </section>
      <section class="order-1 flex items-center lg:order-2">
        <slot />
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import type Popover from 'primevue/popover'
import { useTheme } from '../composables/useTheme'
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'
const { theme, toggle } = useTheme()
const i18n = useI18n()
const locale = i18n.locale
const localeMenu = ref<InstanceType<typeof Popover> | null>(null)

const toggleTheme = () => toggle()
const openLocaleMenu = (event: Event) => localeMenu.value?.toggle(event)
const setAppLocale = async (code: 'en' | 'kh') => {
  await i18n.setLocale(code)
  localeMenu.value?.hide()
}

</script>

<style scoped>
.auth-orb {
  position: absolute;
  border-radius: 9999px;
  filter: blur(72px);
  opacity: 0.65;
}

.auth-orb-a {
  top: -7rem;
  left: -7rem;
  width: 26rem;
  height: 26rem;
  background: rgba(34, 211, 238, 0.28);
  animation: drift-a 18s ease-in-out infinite;
}

.auth-orb-b {
  top: 5rem;
  right: -8rem;
  width: 28rem;
  height: 28rem;
  background: rgba(99, 102, 241, 0.25);
  animation: drift-b 22s ease-in-out infinite;
}

.auth-orb-c {
  bottom: -8rem;
  left: 36%;
  width: 20rem;
  height: 20rem;
  background: rgba(16, 185, 129, 0.18);
  animation: drift-c 20s ease-in-out infinite;
}

@keyframes drift-a {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
  }

  50% {
    transform: translate3d(2rem, 1rem, 0) scale(1.08);
  }
}

@keyframes drift-b {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
  }

  50% {
    transform: translate3d(-1.5rem, 1.5rem, 0) scale(1.05);
  }
}

@keyframes drift-c {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
  }

  50% {
    transform: translate3d(1rem, -1.5rem, 0) scale(1.04);
  }
}
</style>
