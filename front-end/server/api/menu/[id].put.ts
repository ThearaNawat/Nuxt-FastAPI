export default defineEventHandler(async (event) => {
    const token = getCookie(event, 'ACCESS_TOKEN')
    const config = useRuntimeConfig()
    const body = await readBody(event)
    const { id } = getRouterParams(event)

    return await $fetch(`${config.URL_API}/menu/update/${id}`, { method: 'PUT', headers: { Authorization: `Bearer ${token}`}, body})
})