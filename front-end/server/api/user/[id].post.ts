export default defineEventHandler( async (event) => {
    const config = useRuntimeConfig()
    const cookie = getCookie(event, 'ACCESS_TOKEN')
    const { id } = getRouterParams(event)
    const body = await readBody(event)
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/user/update/${id}`, { method: 'POST', headers: { Authorization: `Bearer ${cookie}` }, body})
})