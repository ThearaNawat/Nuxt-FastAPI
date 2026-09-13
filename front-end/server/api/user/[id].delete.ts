export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const cookie = getHeader(event, 'cookie')
    const { id } = getRouterParams(event)
    return await $fetch(`${config.URL_API}/user/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${cookie}` }})
})