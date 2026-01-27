import { useAuthStore } from "~~/store/state"

export default defineNuxtRouteMiddleware((event) =>{
    const auth = useAuthStore()
    const token = auth.getToken
    if (!token) return navigateTo('/login')
})