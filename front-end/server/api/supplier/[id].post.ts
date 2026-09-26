export default eventHandler(async (event) =>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const body = await readBody(event)
    const { id } = getRouterParams(event)
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/supplier/update/${id}`, { method: 'POST', headers: { Authorization: `Bearer ${token}`}, body})
})