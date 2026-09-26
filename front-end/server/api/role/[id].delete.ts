export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const { id } = getRouterParams(event)
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/role/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
    })
})
