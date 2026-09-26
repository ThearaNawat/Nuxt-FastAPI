export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'ACCESS_TOKEN')
  const query = getQuery(event)
  const baseURL = config.URL_API_INTERNAL || config.public.URL_API
  return await $fetch(`${baseURL}/stock`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
    query
  })
})
