export type SaleOrder = {
  id?: number
  order_number: string
  customer_id: number | null
  order_date?: string | null
  required_date?: string | null
  shipped_date?: string | null
  status: string
  notes?: string | null
  created_at?: string | null
  updated_at?: string | null
}

export const useOrder = () => {
  const list = async () => await $fetch<SaleOrder[]>('/api/order')

  const nextNumber = async () => await $fetch<{ order_number: string }>('/api/order/next-number')

  const create = async (payload: Partial<SaleOrder>) =>
    await $fetch('/api/order', { method: 'POST', body: payload })

  const update = async (id: number, payload: Partial<SaleOrder>) =>
    await $fetch(`/api/order/${id}`, { method: 'POST', body: payload })

  const remove = async (ids: number[]) =>
    await $fetch('/api/order', { method: 'DELETE', body: ids })

  return { list, nextNumber, create, update, remove }
}
