export default defineEventHandler( async (event) => {
    const config = useRuntimeConfig()
    // const cookie = getCookie(event, 'ACCESS_TOKEN')
    const body = await readBody(event)
    
    return await $fetch(`${config.URL_API}/user/create`, { method: 'POST', body })
})