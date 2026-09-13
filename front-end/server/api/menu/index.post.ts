export default defineEventHandler(async (event) => {
    const token = getCookie(event, 'ACCESS_TOKEN')
    const config = useRuntimeConfig()
    const body = await readBody(event)
    return await $fetch(`${config.URL_API}/menu/create`, { method: 'POST', headers: { Authorization: `Bearer ${token}`}, body})
})