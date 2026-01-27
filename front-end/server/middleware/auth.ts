export default defineEventHandler((event) => {
    const token = getCookie(event, "TOKEN") || null
    
    if(!token) return
})