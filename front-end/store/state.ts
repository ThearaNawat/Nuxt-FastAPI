import { defineStore } from "pinia";
import type { role } from '~/composables/useRole'

export type User = {
    id: number,
    username: string,
    email: string,
    is_active: boolean,
    role?: role | null,
    updated_at?: Date,
    created_at?: Date
}

export type MenuNode = {
    id?: number
    label: string
    path: string | ""
    icon?: string | null
    badge?: number | null
    key?: string | null
    parent_id?: number | null
    display_order?: number | null
    type?: string | null
    is_active?: boolean | null
    children?: MenuNode[]
}

const readStorageJSON = <T>(key: string, fallback: T): T => {
    if (typeof window === "undefined") {
        return fallback
    }

    try {
        const raw = localStorage.getItem(key)
        return raw ? JSON.parse(raw) as T : fallback
    } catch {
        return fallback
    }
}

const writeStorageJSON = (key: string, value: unknown) => {
    if (typeof window === "undefined") {
        return
    }

    localStorage.setItem(key, JSON.stringify(value))
}

export const useAuthStore = defineStore('user',{
    state: () => {
        return{
            user: {
                token: useCookie('ACCESS_TOKEN').value,
                user: readStorageJSON<User | null>("USER", null),
                menu: readStorageJSON<MenuNode[]>("MENU", []),
                menu_all: readStorageJSON<MenuNode[]>("MENU_ALL", []),
            }
        }
    },
    getters: {
        getToken: (state) => state.user.token,
        getMenu: (state) => state.user.menu,
        getUser: (state) => state.user.user,
        getMenuAll: (state) => state.user.menu_all,
    },
    actions: {
        
        retreiveItem(data: any){
            this.user.user = data.user
            writeStorageJSON('USER', data.user)
            const token = useCookie<string | null>('ACCESS_TOKEN',{
                maxAge: 60 * 60 * 24, sameSite: "lax", httpOnly: false
            })
            token.value = data.token
            this.user.token = token.value
            const menu = Array.isArray(data?.menu) ? data.menu : []
            const menuAll = Array.isArray(data?.menu_all) ? data.menu_all : []
            this.storeMenu(menu)
            this.storeMenuAll(menuAll)
        },
        storeMenu(menu: MenuNode[]){
            this.user.menu = menu
            writeStorageJSON('MENU', menu)
        },
        storeMenuAll(menu: MenuNode[]){
            this.user.menu_all = menu
            writeStorageJSON('MENU_ALL', menu)
        },
        clearMenu(){
            this.user.menu = []
            this.user.menu_all = []
            if (typeof window !== "undefined") {
                localStorage.removeItem('MENU')
                localStorage.removeItem('MENU_ALL')
            }
        },
        removeItem(){
            this.user.token = null
            this.user.user = null
            this.clearMenu()
            if (typeof window !== "undefined") {
                localStorage.removeItem('USER')
            }
            const token = useCookie('ACCESS_TOKEN')
            token.value = null
        },
        
        async login(email: string, password: string){
            const { $axios } = useNuxtApp()
            const response = await $axios.post(`/user/login`, { email, password })
            this.retreiveItem(response.data)
            
            return response
        },
        async logout(){
            const { $axios } = useNuxtApp()
            await new Promise((resolve, reject) => {
                $axios.post('/user/logout')
                .then((res: any) => {
                    this.removeItem()
                    resolve(res)
                })
                .catch((error: any) => {
                    reject(error)
                })
            })
        }
    }
})
