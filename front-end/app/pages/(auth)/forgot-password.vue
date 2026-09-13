<template>
  <AuthShell>
    <template #left>
      <div
        class="relative overflow-hidden rounded-[2rem] border border-white/15 bg-slate-950/70 p-6 shadow-[0_30px_100px_rgba(15,23,42,0.45)] backdrop-blur-xl sm:p-8"
      >
        <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(16,185,129,0.16),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(99,102,241,0.18),transparent_32%)]"
        ></div>
        <div class="relative">
          <div
            class="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-1 text-xs font-semibold uppercase tracking-[0.3em] text-emerald-100"
          >
            <i class="pi pi-lock"></i>
            <span>{{ t('lblForgot') }}</span>
          </div>

          <h2 class="mt-6 max-w-xl text-4xl font-semibold leading-tight text-white sm:text-5xl">
            {{ t('lblForgotTitle') }}
          </h2>
          <p class="mt-4 max-w-xl text-base leading-8 text-slate-300">
            {{ t('lblForgotSubtitle') }}
          </p>

          <div class="mt-8 grid gap-4">
            <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div class="flex items-start gap-4">
                <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-400/15 text-emerald-300">
                  <span class="text-sm font-semibold">01</span>
                </div>
                <div>
                  <p class="text-sm font-medium text-white">{{ t('lblForgotStep1') }}</p>
                </div>
              </div>
            </div>

            <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div class="flex items-start gap-4">
                <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-300">
                  <span class="text-sm font-semibold">02</span>
                </div>
                <div>
                  <p class="text-sm font-medium text-white">{{ t('lblForgotStep2') }}</p>
                </div>
              </div>
            </div>

            <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div class="flex items-start gap-4">
                <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-indigo-400/15 text-indigo-300">
                  <span class="text-sm font-semibold">03</span>
                </div>
                <div>
                  <p class="text-sm font-medium text-white">{{ t('lblForgotStep3') }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-8 rounded-2xl border border-white/10 bg-white/5 p-5">
            <div class="flex items-start gap-4">
              <div
                class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-emerald-400/10 text-emerald-200"
              >
                <i class="pi pi-info-circle text-xl"></i>
              </div>
              <div>
                <p class="text-sm font-medium text-white">{{ t('lblResetEmailHint') }}</p>
                <p class="mt-1 text-sm leading-6 text-slate-400">
                  {{ t('lblForgotSubtitle') }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <div class="w-full max-w-xl lg:ml-auto">
      <div
        class="rounded-[2rem] border border-white/70 bg-white/90 p-6 shadow-[0_24px_100px_rgba(15,23,42,0.18)] backdrop-blur-xl dark:border-slate-800/80 dark:bg-slate-900/90 sm:p-8"
      >
        <div class="flex items-start justify-between gap-6">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.32em] text-emerald-600 dark:text-emerald-300">
              {{ t('lblForgot') }}
            </p>
            <h1 class="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
              {{ t('lblForgotTitle') }}
            </h1>
            <p class="mt-2 max-w-xl text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ t('lblForgotSubtitle') }}
            </p>
          </div>

          <div class="hidden shrink-0 rounded-2xl border border-emerald-500/15 bg-emerald-500/10 p-4 text-emerald-600 dark:text-emerald-300 sm:flex">
            <i class="pi pi-lock text-2xl"></i>
          </div>
        </div>

        <div
          v-if="sent"
          class="mt-6 rounded-[1.5rem] border border-emerald-500/20 bg-emerald-500/10 p-5 dark:border-emerald-500/20 dark:bg-emerald-500/10"
        >
          <div class="flex items-start gap-4">
            <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-emerald-500/15 text-emerald-500">
              <i class="pi pi-check-circle text-2xl"></i>
            </div>
            <div class="flex-1">
              <h2 class="text-2xl font-semibold text-slate-900 dark:text-white">
                {{ t('lblForgotSuccessTitle') }}
              </h2>
              <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
                {{ t('lblForgotSuccessBody') }}
              </p>
              <div class="mt-4 inline-flex rounded-full border border-emerald-500/20 bg-white/70 px-4 py-2 text-sm text-slate-700 dark:border-emerald-500/20 dark:bg-slate-950/60 dark:text-slate-200">
                {{ email }}
              </div>
            </div>
          </div>

          <div class="mt-6 flex flex-col gap-3 sm:flex-row">
            <NuxtLink
              to="/login"
              class="inline-flex items-center justify-center gap-2 rounded-2xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm font-semibold text-emerald-700 transition hover:-translate-y-0.5 hover:bg-emerald-500/15 dark:text-emerald-200"
            >
              {{ t('lblBackToLogin') }}
              <i class="pi pi-arrow-right text-xs"></i>
            </NuxtLink>
            <Button
              type="button"
              severity="secondary"
              outlined
              class="justify-center !rounded-2xl"
              :label="t('lblTryAnotherEmail')"
              @click="tryAnotherEmail"
            />
          </div>
        </div>

        <template v-else>
          <Message v-if="emailError" class="mt-5" severity="warn" variant="simple" size="small">
            {{ emailError }}
          </Message>

          <form class="mt-6 space-y-5" @submit.prevent="sendResetLink">
            <div>
              <label
                for="reset-email"
                class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300"
              >
                {{ t('email') }}
              </label>
              <InputText
                id="reset-email"
                v-model="email"
                type="email"
                class="w-full"
                size="large"
                autocomplete="email"
                :invalid="Boolean(emailError)"
              />
            </div>

            <Button
              type="submit"
              class="w-full justify-center !rounded-2xl"
              :label="t('btnSendReset')"
              icon="pi pi-envelope"
              size="large"
            />
          </form>

          <div
            class="mt-6 flex flex-col gap-3 border-t border-slate-200 pt-5 text-sm text-slate-500 dark:border-slate-800 dark:text-slate-400 sm:flex-row sm:items-center sm:justify-between"
          >
            <span>{{ t('lblResetEmailHint') }}</span>
            <NuxtLink
              to="/login"
              class="inline-flex items-center gap-2 font-semibold text-emerald-600 transition hover:-translate-y-0.5 hover:text-emerald-500 dark:text-emerald-300 dark:hover:text-emerald-200"
            >
              {{ t('lblBackToLogin') }}
              <i class="pi pi-arrow-right text-xs"></i>
            </NuxtLink>
          </div>
        </template>
      </div>
    </div>
  </AuthShell>
</template>

<script setup lang="ts">
const { t } = useI18n()

const email = ref('')
const emailError = ref('')
const sent = ref(false)

watch(email, () => {
  if (emailError.value) {
    emailError.value = ''
  }
})

const tryAnotherEmail = () => {
  sent.value = false
  emailError.value = ''
}

const sendResetLink = () => {
  if (!email.value.trim()) {
    emailError.value = t('lblResetEmailRequired')
    return
  }

  sent.value = true
}
</script>
