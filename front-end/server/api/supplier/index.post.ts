export default eventHandler(async (event) =>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const body = await readBody(event)
    return await $fetch(`${config.URL_API}/supplier/create`, { method: 'POST', headers: {Authorization: `Bearer ${token}`}, body})
})