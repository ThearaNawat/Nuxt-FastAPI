import type { PurchaseOrder } from '~~/shared/types/purchase'

export const usePurchase = () => {
  const list = async () => await $fetch<PurchaseOrder[]>('/api/purchase-order')

  const create = async (payload: Partial<PurchaseOrder>) =>
    await $fetch('/api/purchase-order', { method: 'POST', body: payload })

  const update = async (id: number, payload: Partial<PurchaseOrder>) =>
    await $fetch(`/api/purchase-order/${id}`, { method: 'POST', body: payload })

  const remove = async (ids: number[]) =>
    await $fetch('/api/purchase-order', { method: 'DELETE', body: ids })

  const nextNumber = async () =>
    await $fetch<{ order_number: string }>('/api/purchase-order/next-number')

  return { list, create, update, remove, nextNumber }
}
