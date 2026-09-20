export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'ACCESS_TOKEN')

  return await $fetch(`${config.URL_API}/income/`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
  })
})
