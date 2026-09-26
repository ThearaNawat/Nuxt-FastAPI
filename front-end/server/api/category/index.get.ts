export default defineEventHandler(async (event) =>{
    const config = useRuntimeConfig(event)
    const token = getCookie(event, 'ACCESS_TOKEN')
    const baseURL = `${config.URL_API_INTERNAL}/api` || config.public.URL_API
    return await $fetch(`${baseURL}/category/`, { method: 'GET', headers: { Authorization: `Bearer ${token}`}})
})