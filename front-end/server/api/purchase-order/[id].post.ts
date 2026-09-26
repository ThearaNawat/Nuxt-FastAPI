export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'ACCESS_TOKEN')
  const body = await readBody(event)
  const id = getRouterParam(event, 'id')
  const baseURL = config.URL_API_INTERNAL || config.public.URL_API
  return await $fetch(`${baseURL}/purchase-order/update/${id}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body
  })
})