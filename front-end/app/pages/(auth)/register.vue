<template>
  <AuthShell>
    <template #left>
      <div
        class="relative overflow-hidden rounded-[2rem] border border-white/15 bg-slate-950/70 p-6 shadow-[0_30px_100px_rgba(15,23,42,0.45)] backdrop-blur-xl sm:p-8"
      >
        <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(34,211,238,0.16),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(99,102,241,0.18),transparent_32%)]"
        ></div>
        <div class="relative">
          <div
            class="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-1 text-xs font-semibold uppercase tracking-[0.3em] text-cyan-100"
          >
            <i class="pi pi-user-plus"></i>
            <span>{{ t('lblRegister') }}</span>
          </div>

          <h2 class="mt-6 max-w-xl text-4xl font-semibold leading-tight text-white sm:text-5xl">
            {{ t('lblRegisterTitle') }}
          </h2>
          <p class="mt-4 max-w-xl text-base leading-8 text-slate-300">
            {{ t('lblRegisterSubtitle') }}
          </p>

          <div class="mt-8 grid gap-4 sm:grid-cols-3">
            <div
              class="rounded-2xl border border-white/10 bg-white/5 p-4 transition duration-300 hover:-translate-y-1 hover:bg-white/10"
            >
              <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-300">
                <i class="pi pi-box text-lg"></i>
              </div>
              <p class="mt-3 text-sm font-medium text-white">
                {{ t('lblRegisterBenefit1') }}
              </p>
            </div>
            <div
              class="rounded-2xl border border-white/10 bg-white/5 p-4 transition duration-300 hover:-translate-y-1 hover:bg-white/10"
            >
              <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-indigo-400/15 text-indigo-300">
                <i class="pi pi-shield text-lg"></i>
              </div>
              <p class="mt-3 text-sm font-medium text-white">
                {{ t('lblRegisterBenefit2') }}
              </p>
            </div>
            <div
              class="rounded-2xl border border-white/10 bg-white/5 p-4 transition duration-300 hover:-translate-y-1 hover:bg-white/10"
            >
              <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-400/15 text-emerald-300">
                <i class="pi pi-lock text-lg"></i>
              </div>
              <p class="mt-3 text-sm font-medium text-white">
                {{ t('lblRegisterBenefit3') }}
              </p>
            </div>
          </div>

          <div class="mt-8 rounded-2xl border border-white/10 bg-white/5 p-5">
            <div class="flex items-start gap-4">
              <div
                class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-cyan-400/10 text-cyan-200"
              >
                <i class="pi pi-key text-xl"></i>
              </div>
              <div>
                <p class="text-sm font-medium text-white">
                  {{ t('lblRegisterNote') }}
                </p>
                <p class="mt-1 text-sm leading-6 text-slate-400">
                  {{ t('lblRegisterHint') }}
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
            <p class="text-xs font-semibold uppercase tracking-[0.32em] text-cyan-600 dark:text-cyan-300">
              {{ t('lblRegister') }}
            </p>
            <h1 class="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
              {{ t('lblRegisterTitle') }}
            </h1>
            <p class="mt-2 max-w-xl text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ t('lblRegisterSubtitle') }}
            </p>
          </div>

          <div class="hidden shrink-0 rounded-2xl border border-cyan-500/15 bg-cyan-500/10 p-4 text-cyan-600 dark:text-cyan-300 sm:flex">
            <i class="pi pi-user-plus text-2xl"></i>
          </div>
        </div>

        <Message v-if="apiError" class="mt-5" severity="error" variant="simple" size="small">
          {{ apiError }}
        </Message>

        <form class="mt-6 space-y-5" @submit.prevent="createAccount">
          <div>
            <label
              for="register-username"
              class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300"
            >
              {{ t('username') }}
            </label>
            <InputText
              id="register-username"
              v-model="form.username"
              class="w-full"
              size="large"
              autocomplete="username"
              :invalid="Boolean(errors.username)"
            />
            <Message v-if="errors.username" severity="error" variant="simple" size="small">
              {{ errors.username }}
            </Message>
          </div>

          <div>
            <label
              for="register-email"
              class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300"
            >
              {{ t('email') }}
            </label>
            <InputText
              id="register-email"
              v-model="form.email"
              type="email"
              class="w-full"
              size="large"
              autocomplete="email"
              :invalid="Boolean(errors.email)"
            />
            <Message v-if="errors.email" severity="error" variant="simple" size="small">
              {{ errors.email }}
            </Message>
          </div>

          <div>
            <label
              for="register-password"
              class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300"
            >
              {{ t('password') }}
            </label>
            <Password
              id="register-password"
              v-model="form.password"
              class="w-full"
              :feedback="false"
              toggleMask
              size="large"
              autocomplete="new-password"
              :invalid="Boolean(errors.password)"
            />
            <p class="mt-2 text-xs text-slate-500 dark:text-slate-400">
              {{ t('lblRegisterHint') }}
            </p>
            <Message v-if="errors.password" severity="error" variant="simple" size="small">
              {{ errors.password }}
            </Message>
          </div>

          <div>
            <label
              for="register-confirm-password"
              class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300"
            >
              {{ t('confirmPassword') }}
            </label>
            <Password
              id="register-confirm-password"
              v-model="form.confirm_password"
              class="w-full"
              :feedback="false"
              toggleMask
              size="large"
              autocomplete="new-password"
              :invalid="Boolean(errors.confirm_password)"
            />
            <Message
              v-if="errors.confirm_password"
              severity="error"
              variant="simple"
              size="small"
            >
              {{ errors.confirm_password }}
            </Message>
          </div>

          <Button
            type="submit"
            class="w-full justify-center !rounded-2xl"
            :label="t('btnCreateAccount')"
            icon="pi pi-user-plus"
            size="large"
            :loading="btnLoading"
          />
        </form>

        <div
          class="mt-6 flex flex-col gap-3 border-t border-slate-200 pt-5 text-sm text-slate-500 dark:border-slate-800 dark:text-slate-400 sm:flex-row sm:items-center sm:justify-between"
        >
          <span>{{ t('lblAlreadyHaveAccount') }}</span>
          <NuxtLink
            to="/login"
            class="inline-flex items-center gap-2 font-semibold text-cyan-600 transition hover:-translate-y-0.5 hover:text-cyan-500 dark:text-cyan-300 dark:hover:text-cyan-200"
          >
            {{ t('lblBackToLogin') }}
            <i class="pi pi-arrow-right text-xs"></i>
          </NuxtLink>
        </div>
      </div>
    </div>
  </AuthShell>
</template>

<script setup lang="ts">
import type { user } from '~/composables/useUsers'

const { t } = useI18n()
const router = useRouter()
const message = MessageBox()
const userAction = useUsers()

const form = reactive<user>({
  id: 0,
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  status: true,
  role_id: 0
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
})

const apiError = ref('')
const btnLoading = ref(false)

const resetErrors = () => {
  errors.username = ''
  errors.email = ''
  errors.password = ''
  errors.confirm_password = ''
  apiError.value = ''
}

const mapValidationErrors = (error: any) => {
  const detail =
    error?.data?.data?.detail ??
    error?.data?.detail ??
    error?.response?.data?.detail ??
    error?.response?.data?.data?.detail

  if (Array.isArray(detail)) {
    detail.forEach((item: any) => {
      const field = item?.loc?.[1]
      if (field && field in errors) {
        ;(errors as Record<string, string>)[field] = item.msg
      }
    })
    return
  }

  if (typeof detail === 'string') {
    apiError.value = detail
    return
  }

  apiError.value =
    error?.data?.data?.message ??
    error?.data?.message ??
    error?.response?.data?.message ??
    error?.message ??
    'Unable to create account.'
}

const createAccount = async () => {
  resetErrors()

  if (form.password !== form.confirm_password) {
    errors.confirm_password = t('lblPasswordMismatch')
    return
  }

  btnLoading.value = true

  try {
    await userAction.create({ ...form })
    message.success(t('lblRegisterSuccess'))
    await router.push({ path: '/login', query: { email: form.email } })
  } catch (error: any) {
    mapValidationErrors(error)
  } finally {
    btnLoading.value = false
  }
}
</script>
