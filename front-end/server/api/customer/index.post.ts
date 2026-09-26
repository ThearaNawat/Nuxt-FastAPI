export default defineEventHandler( async (event) => {
    const token = getCookie(event, 'ACCESS_TOKEN')
    const config = useRuntimeConfig()
    const body = await readBody(event)
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/customer/create`, { method: 'POST', headers: { Authorization: `Bearer ${token}`}, body})
})