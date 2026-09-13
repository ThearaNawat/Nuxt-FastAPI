export default defineEventHandler(async (event) => {
    const token = getCookie(event, 'ACCESS_TOKEN')
    const config = useRuntimeConfig()
    const body = await readBody(event)
    const { id } = getRouterParams(event)
    return await $fetch(`${config.URL_API}/customer/update/${id}`, { method: 'POST', headers: { Authorization: `Bearer ${token}`}, body})
})