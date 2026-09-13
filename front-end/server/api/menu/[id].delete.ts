export default defineEventHandler(async (event) => {
    const token = getCookie(event, 'ACCESS_TOKEN')
    const config = useRuntimeConfig()
    const { id } = getRouterParams(event)
    return await $fetch(`${config.URL_API}/menu/delete/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${token}`}})
})