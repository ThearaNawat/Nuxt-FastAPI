export default defineEventHandler( async (event) => {
    const config = useRuntimeConfig()
    const cookie = getCookie(event, 'ACCESS_TOKEN')
    const { id } = getRouterParams(event)
    const body = await readBody(event)

    return await $fetch(`${config.URL_API}/user/update/${id}`, { method: 'POST', headers: { Authorization: `Bearer ${cookie}` }, body})
})