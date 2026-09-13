export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const query = getQuery(event)
    return await $fetch(`${config.URL_API}/stock-transaction`, { headers: { Authorization: `Bearer ${token}`}, method: 'GET', query})
})