export default defineEventHandler(async(event)=>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const { id } = await getRouterParams(event)
    const body = await readBody(event)
    return await $fetch(`${config.URL_API}/stock-transaction/update/${id}`, { headers: { Authorization: `Bearer ${token}`}, method:'POST', body})
})