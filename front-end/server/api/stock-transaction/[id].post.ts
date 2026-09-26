export default defineEventHandler(async(event)=>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const { id } = await getRouterParams(event)
    const body = await readBody(event)
    const baseURL = config.URL_API_INTERNAL || config.public.URL_API
    return await $fetch(`${baseURL}/stock-transaction/update/${id}`, { headers: { Authorization: `Bearer ${token}`}, method:'POST', body})
})