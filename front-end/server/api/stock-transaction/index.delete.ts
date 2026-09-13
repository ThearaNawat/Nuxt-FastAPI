export default defineEventHandler(async(event)=>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const body = await readBody(event)
    return await $fetch(`${config.URL_API}/stock-transaction/delete`, { headers: { Authorization: `Bearer ${token}`}, method:'DELETE', body})
})