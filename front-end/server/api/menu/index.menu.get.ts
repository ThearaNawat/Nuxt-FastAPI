export default defineEventHandler(async (event) => {
    const token = getCookie(event,"ACCESS_TOKEN")
    const config = useRuntimeConfig()
    return await $fetch(`${config.URL_API}/menu`, { method: 'GET', headers: { Authorization: `Bearer ${token}`}})
})