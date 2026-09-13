export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const { id } = getRouterParams(event)
    const body = await readBody(event)

    return await $fetch(`${config.URL_API}/role/${id}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` },
        body,
    })
})
