export default defineEventHandler(async (event)=>{
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const body = await readBody(event)
    const { id } = getRouterParams(event)
    return await $fetch(`${config.URL_API}/measurement/update/${id}`, { method: 'POST', headers: { Authorization: `Bearer ${token}`}, body})
})