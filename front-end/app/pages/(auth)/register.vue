<template>
  <Card id="register-page" class="flex items-center justify-center h-screen">
      <template #content>
          <Card class="w-[600px] shadow-sm shadow-cyan-500/50">
          <template #content>
              <form class="w-full" @submit.prevent="createAccount">
                  <div class="flex items-center justify-between flex-column">
                      <div>
                          <Button icon="pi pi-spin pi-globe" variant="link" size="large" @click="toggler"></Button>
                          <Button :icon="theme !== 'dark' ? 'pi pi-spin pi-sun' : 'pi pi-spin pi-moon'" variant="link" size="large" @click="toggle"></Button>
                      </div>

                      <div>
                          <h1 class="text-blue-800 text-shadow-2xs text-xl text-shadow-sky-900 font-bold">{{ t('lblRegister') }}</h1>
                      </div>
                      <div>
                          <ComponentColorPicker/>
                      </div>
                  </div>
                  
                  <Divider></Divider>
                  <div class="">
                      <InputGroup>
                          <InputGroupAddon>
                              <Button icon="pi pi-user" variant="link"></Button>
                          </InputGroupAddon>
                          <FloatLabel variant="on">
                              <InputText
                                  class="w-full"
                                  size="large"
                                  v-model="form.username"
                                  
                              />
                              <label for="email">{{ t('username') }}</label>
                          </FloatLabel>
                          
                      </InputGroup>
                      <Message severity="error" variant="simple" size="small" v-if="errors.username">{{ errors.username }}</Message>
                  </div>

                  <div class="mt-4">
                      <InputGroup>
                          <InputGroupAddon>
                              <Button icon="pi pi-envelope" variant="link"></Button>
                          </InputGroupAddon>
                          <FloatLabel variant="on">
                              <InputText
                                  id="email"
                                  class="w-full"
                                  size="large"
                                  v-model="form.email"
                                  
                              />
                              <label for="email">{{ t('email') }}</label>
                          </FloatLabel>
                          
                      </InputGroup>
                      <Message severity="error" variant="simple" size="small" v-if="errors.email">{{ errors.email }}</Message>
                  </div>

                  <div class="my-4">
                      <InputGroup>
                          <InputGroupAddon>
                              <Button icon="pi pi-key" variant="link"></Button>
                          </InputGroupAddon>
                          <FloatLabel variant="on">
                              <Password
                                  size="large"
                                  v-model="form.password"
                                  toggleMask
                                  name="password"
                              >
                                  
                              </Password>
                              <label>{{ t('password') }}</label>
                          </FloatLabel>
                      </InputGroup>
                      <Message severity="error" variant="simple" size="small" v-if="errors.password">{{ errors.password }}</Message>
                  </div>

                  <div class="my-4">
                      <InputGroup>
                          <InputGroupAddon>
                              <Button icon="pi pi-key" variant="link"></Button>
                          </InputGroupAddon>
                          <FloatLabel variant="on">
                              <Password
                                  size="large"
                                  v-model="form.confirm_password"
                                  toggleMask
                                  name="password"
                              >
                                  
                              </Password>
                              <label>{{ t('confirmPassword') }}</label>
                          </FloatLabel>
                      </InputGroup>
                      <Message severity="error" variant="simple" size="small" v-if="errors.confirm_password">{{ errors.confirm_password }}</Message>
                  </div>

                  <Button
                      type="submit"
                      :label="t('btnSave')"
                      icon="pi pi-sign-in"
                      class="w-full"
                      :loading="btnLoading"
                  />
              </form>
              <Divider></Divider>
              <NuxtLink to="/login" class="text-blue-800 font-bold">{{t('lblLogin')}}</NuxtLink>
              
              <Popover ref="op" :dismissable="true">
                <div class="flex flex-col gap-4">
                    <Button @click="hideButton('en')" label="English" size="small" variant="text"></Button>
                    <Button @click="hideButton('kh')" label="Khmer" size="small" variant="text"></Button>
                </div>
            </Popover>
          </template>
            
        </Card>
      </template>
  </Card>
</template>

<script setup lang="ts">
import type { user } from '~/composables/useUsers'
import type Popover from 'primevue/popover'
const { theme, toggle } = useTheme()
const { t } = useI18n()
const $i18n = useI18n()
const router = useRouter()
const message = MessageBox()
const userAction = useUsers()
const op = ref<InstanceType<typeof Popover> | null>(null)
    //================Method====================
const hideButton = (lang: string) => {
  op.value?.hide()
  if(lang === 'en') 
    $i18n.setLocale('en')
  else
    $i18n.setLocale('kh') 
}
const toggler = (event: Event) => {
  op.value?.toggle(event);
}
    

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
