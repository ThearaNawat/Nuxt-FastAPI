export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'ACCESS_TOKEN')

  return await $fetch(`${config.URL_API}/purchase-order/next-number`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` }
  })
})