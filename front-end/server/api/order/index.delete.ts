export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'ACCESS_TOKEN')
  const body = await readBody(event)
  const baseURL = config.URL_API_INTERNAL || config.public.URL_API
  return await $fetch(`${baseURL}/sales-order`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
    body
  })
})
