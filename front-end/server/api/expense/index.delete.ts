export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'ACCESS_TOKEN')
  const body = await readBody(event)

  return await $fetch(`${config.URL_API}/expense/delete`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
    body,
  })
})
