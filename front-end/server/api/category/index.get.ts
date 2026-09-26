export default defineEventHandler(async (event) =>{
    const config = useRuntimeConfig(event)
    const token = getCookie(event, 'ACCESS_TOKEN')
    // const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${config.URL_API_INTERNAL}/category/`, { method: 'GET', headers: { Authorization: `Bearer ${token}`}})
})