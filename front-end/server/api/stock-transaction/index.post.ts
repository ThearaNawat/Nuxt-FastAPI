export default defineEventHandler(async (event)=>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const body = await readBody(event)
    return await $fetch(`${config.URL_API}/stock-transaction/create`, { headers: { Authorization: `Bearer ${token}`}, method: 'POST', body})
})