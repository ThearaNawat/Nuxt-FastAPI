export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const cookie = getHeader(event, 'cookie')
    const { id } = getRouterParams(event)
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/user/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${cookie}` }})
})