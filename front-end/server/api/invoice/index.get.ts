export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const token = getCookie(event, 'ACCESS_TOKEN')
    const query = getQuery(event) 
    return await $fetch(`${config.URL_API}/invoice`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` },
        query
    })
})
