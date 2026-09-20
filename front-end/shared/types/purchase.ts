export type PurchaseSupplier = {
  id: number
  code?: string
  name: string
}

export type PurchaseProduct = {
  id: number
  code: string
  name: string
  package?: string | null
  measurement_id?: number | null
  measurement_code?: string | null
}

export type PurchaseOrderItem = {
  id?: number
  product_id: number | null
  quantity: number
  unit_cost: number
  measurement_id: number | 0
  total_cost?: number
  product?: PurchaseProduct | null
}

export type PurchaseOrder = {
  id?: number
  order_number?: string
  supplier_id: number | null
  supplier?: PurchaseSupplier | null
  order_date?: string | null
  required_date?: string | null
  received_date?: string | null
  status: string
  payment_status?: number | 1
  currency_id: number | null
  notes?: string | null
  sub_total: number | 0
  discount_amount: number | 0
  tax_amount: number | 0
  total_amount: number | 0
  items?: PurchaseOrderItem[]
  created_at?: string | null
  updated_at?: string | null
}
