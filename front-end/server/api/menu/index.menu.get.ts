export default defineEventHandler(async (event) => {
    const token = getCookie(event,"ACCESS_TOKEN")
    const config = useRuntimeConfig()
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/menu`, { method: 'GET', headers: { Authorization: `Bearer ${token}`}})
})