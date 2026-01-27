<template>
    <div id="login" class="flex items-center justify-center h-screen">
        <i class="pi pi-spin pi-microchip-ai" style="font-size: 5rem; color: slateblue; position: absolute; left: 20%;"></i>
        <Button icon="pi pi-spin pi-microchip-ai" size="large" style="position: absolute; right: 0;" variant="link"></Button>
        
        <Card class="shadow-sm shadow-cyan-500/50 w-[600px]">
            <template #content>
                <!-- <div class="w-full"> -->
                    <form class="w-full" @submit.prevent="login">
                        <div class="flex items-center justify-between flex-column">
                            <div>
                                <!-- <i class="pi pi-spin pi-globe mr-2" style="font-size: 2rem; color: green; cursor: pointer;" @click="toggler"></i> -->
                                <Button icon="pi pi-spin pi-globe" variant="link" size="large" @click="toggler"></Button>
                                <Button :icon="theme !== 'dark' ? 'pi pi-spin pi-sun' : 'pi pi-spin pi-moon'" variant="link" size="large" @click="toggle"></Button>
                                <!-- <i :class="theme !== 'dark' ? 'pi pi-spin pi-sun' : 'pi pi-spin pi-moon'" style="font-size: 2rem;color: green; cursor: pointer;" @click="toggle"/> -->
                            </div>

                            <div>
                                <h1 class="text-blue-800 text-shadow-2xs text-xl text-shadow-sky-900 font-bold">{{ t('lblLogin') }}</h1>
                            </div>
                            <div>
                                <ComponentColorPicker/>
                            </div>
                        </div>
                        
                        <Divider></Divider>
                        <div class="">
                            <InputGroup>
                                <InputGroupAddon>
                                    <!-- <i class="pi pi-envelope" style="font-weight: bold; color: slateblue;"></i> -->
                                    <Button icon="pi pi-envelope" variant="link"></Button>
                                </InputGroupAddon>
                                <FloatLabel variant="on">
                                    <InputText
                                        id="email"
                                        class="w-full"
                                        size="large"
                                        v-model="email"
                                        
                                    />
                                    <label for="email">{{ t('email') }}</label>
                                </FloatLabel>
                                
                            </InputGroup>
                            <Message severity="error" variant="simple" size="small" v-if="errors.isEmail">{{ errors.email }}</Message>
                        </div>

                        <div class="my-4">
                            <InputGroup>
                                <InputGroupAddon>
                                    <!-- <i class="pi pi-key" style="font-weight: bold; color: slateblue;"></i> -->
                                    <Button icon="pi pi-key" variant="link"></Button>
                                </InputGroupAddon>
                                <FloatLabel variant="on">
                                    <Password
                                        size="large"
                                        v-model="password"
                                        toggleMask
                                        name="password"
                                    >
                                        
                                    </Password>
                                    <label>{{ t('password') }}</label>
                                </FloatLabel>
                            </InputGroup>
                            <Message severity="error" variant="simple" size="small" v-if="errors.isPassword">{{ errors.password }}</Message>
                        </div>

                        <Button
                            type="submit"
                            :label="t('btnLogin')"
                            icon="pi pi-sign-in"
                            class="w-full"
                            :loading="btnLoading"
                        />
                    </form>
                    <Divider></Divider>
                    <NuxtLink to="register" class="text-blue-800 font-bold">{{t('lblRegister')}}</NuxtLink>
                    <NuxtLink to="forgot-password" class="text-blue-800 font-bold float-right">{{ t('lblForgot') }}</NuxtLink>
                <!-- </div> -->
            </template>
            
        </Card>
         <Popover ref="op" :dismissable="true">
            <div class="flex flex-col gap-4">
                <Button @click="hideButton('en')" label="English" size="small" variant="text"></Button>
                <Button @click="hideButton('kh')" label="Khmer" size="small" variant="text"></Button>
            </div>
        </Popover>
    </div>
</template>
<script setup lang="ts">
    import  { useAuthStore }  from '../../../store/state'
    import type Popover from 'primevue/popover'
    const { t } = useI18n()
    const $i18n = useI18n()
    const { theme, toggle } = useTheme()
    const router = useRouter()
    const password = ref('')
    const email = ref('')
    const errors = ref({ email: '', password: '', isEmail: false, isPassword: false})
    const btnLoading = ref(false)
    const state = useAuthStore()
    const message = MessageBox()
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
    async function login(){
        await state.login(email.value, password.value)
        .then((res) => {
            router.push('/')
            btnLoading.value = false
            message.success('You login success')
        })
        .catch((error: any) => {
            const errorText = error.response.data.detail
            for(var x=0; x < errorText.length; x++){
                var textField = errorText[x].loc[1]
                var msgText = errorText[x]
                if(textField === 'email'){
                    errors.value.isEmail = true
                    errors.value.email = msgText.msg
                }

                if(textField === 'password'){
                    errors.value.isPassword = true
                    errors.value.password = msgText.msg
                }
            }
            btnLoading.value = false
        })
    }
</script>