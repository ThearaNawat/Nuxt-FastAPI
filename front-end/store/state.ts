import { defineStore } from "pinia";

export const useAuthStore = defineStore('user',{
    state: () => {
        return{
            user: {
                token: useCookie('ACCESS_TOKEN').value,
                user: JSON.parse(localStorage.getItem("USER") || "null") || null,
            }
        }
    },
    getters: {
        getToken: (state) => state.user.token
    },
    actions: {
        
        retreiveItem(data: any){
            this.user.user = data.user
            localStorage.setItem('USER', JSON.stringify(data.user))
            const token = useCookie<string | null>('ACCESS_TOKEN',{
                maxAge: 60 * 60 * 24, sameSite: "lax", httpOnly: false
            })
            token.value = data.token
            this.user.token = token.value
        },
        removeItem(){
            this.user.token = null
            this.user.user = null
            localStorage.removeItem('USER')
            const token = useCookie('ACCESS_TOKEN')
            token.value = null
        },
        async login(email: string, password: string){
            await new Promise((resolve, reject) => {
                const { $axios } = useNuxtApp()
                $axios.post(`/user/login`, { email, password })
                    .then((res: any) => {
                        this.retreiveItem(res.data)
                        resolve(res)
                    })
                    .catch((error: any) =>{
                        reject(error)
                    })
            })
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