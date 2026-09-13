export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'ACCESS_TOKEN')
  const body = await readBody(event)
  const id = getRouterParam(event, 'id')

  return await $fetch(`${config.URL_API}/sales-order/${id}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body
  })
})
