export default defineEventHandler((event) => {
    const token = getCookie(event, "ACCESS_TOKEN") || getCookie(event, "TOKEN") || null
    
    if(!token) return
})
