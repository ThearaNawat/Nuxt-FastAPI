import { useAuthStore } from "~~/store/state"

export default defineNuxtRouteMiddleware((to) =>{
    const auth = useAuthStore()
    const token = auth.getToken
    const publicPages = [
        "/login",
        "/register",
        "/forgot-password",
        "/error"
    ]

    if (publicPages.includes(to.path)) return
    if (!token && to.path !== "/login") return navigateTo('/login')

    const allowedRoutes = hasRoutePermission(auth.getMenu, to.path)
    if(!allowedRoutes) return navigateTo('/error')
})