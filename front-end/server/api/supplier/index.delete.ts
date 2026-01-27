export default eventHandler(async (event) =>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const body = await readBody(event)

    return await $fetch(`${config.URL_API}/supplier/delete`, { method: 'DELETE', headers: { Authorization: `Bearer ${token}`}, body})
})