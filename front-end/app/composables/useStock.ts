export type StockMeasurement = {
  id: number
  code: string
  name: string
  description?: string | null
}

export type StockProduct = {
  id: number
  code: string
  name: string
  package?: string | null
  expire_date?: string | null
  measurement_id?: number | null
  measurement_code?: string | null
  measurement?: StockMeasurement | null
}

export type StockWarehouse = {
  id: number
  warehouse_name: string
  address?: string | null
  city?: string | null
  state?: string | null
  postal_code?: string | null
  country?: string | null
}

export type StockItem = {
  id: number
  product_id: number | null
  warehouse_id: number | null
  measurement_id?: number | null
  measurement_reserved_id?: number | null
  transaction_type: string | null
  current_quantity: number
  reserved_quantity?: number | 0
  reason?: string | null
  reference_number?: string | null
  status?: boolean
  created_at?: string | null
  updated_at?: string | null
  product?: StockProduct | null
  measurement?: StockMeasurement | null
  warehouse?: StockWarehouse | null
}

export type StockPagination = {
  page: number
  limit: number
  total_records: number
  total_pages: number
  offset: number
}

export type StockListResponse = {
  data: StockItem[]
  pagination: StockPagination
}

export const useStock = () => {
  const list = async (queryString: string = '') => {
    const url = queryString ? `/api/stock?${queryString}` : '/api/stock'
    return await $fetch<StockListResponse>(url)
  }

  const create = async (payload: Partial<StockItem>) =>
    await $fetch('/api/stock', { method: 'POST', body: payload })

  const update = async (id: number, payload: Partial<StockItem>) =>
    await $fetch(`/api/stock/${id}`, { method: 'POST', body: payload })

  const remove = async (ids: number[]) =>
    await $fetch('/api/stock', { method: 'DELETE', body: ids })

  return { list, create, update, remove }
}
