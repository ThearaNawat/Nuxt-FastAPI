export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const { id } = getRouterParams(event)
    const body = await readBody(event)
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/role/${id}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` },
        body,
    })
})
