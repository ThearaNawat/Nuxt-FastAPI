export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const { id } = getRouterParams(event)

    return await $fetch(`${config.URL_API}/role/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
    })
})
