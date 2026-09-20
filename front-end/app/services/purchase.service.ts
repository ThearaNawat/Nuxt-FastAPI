import { FilterMatchMode, FilterOperator } from '@primevue/core/api'

export type PurchaseItemForm = {
  product_id: number | null
  quantity: number
  unit_cost: number
  total_cost: number
  measurement_id: number
}

export type PurchaseForm = {
  id?: number
  order_number?: string
  supplier_id: number | null
  order_date: Date | null
  required_date: Date | null
  received_date: Date | null
  status: string
  payment_status: number
  notes: string
  sub_total: number
  discount_amount: number
  currency_id: number | null
  tax_amount: number
  total_amount: number
  items: PurchaseItemForm[]
}

export type PurchaseErrors = {
  supplier_id: string
  items: string
}

export const createPurchaseFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  order_number: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  supplier_id: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
  status: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] }
})

export const createEmptyPurchaseItem = (): PurchaseItemForm => ({
  product_id: null,
  quantity: 1,
  unit_cost: 0,
  total_cost: 0,
  measurement_id: 0
})

export const createEmptyPurchaseForm = (): PurchaseForm => ({
  order_number: undefined,
  supplier_id: null,
  order_date: new Date(),
  required_date: null,
  received_date: null,
  status: 'pending',
  payment_status: 1,
  notes: '',
  currency_id: null,
  sub_total: 0,
  discount_amount: 0,
  tax_amount: 0,
  total_amount: 0,
  items: [createEmptyPurchaseItem()],
})

export const createPurchaseErrors = (): PurchaseErrors => ({
  supplier_id: '',
  items: ''
})

type ValidationDetailItem = {
  loc?: Array<string | number>
  msg?: string
}

export const applyPurchaseValidationErrors = (detail: unknown, errors: PurchaseErrors): PurchaseErrors => {
  const nextErrors = { ...errors }
  if (typeof detail === 'string' || !Array.isArray(detail)) return nextErrors

  detail.forEach((item: ValidationDetailItem) => {
    const fieldName = item?.loc?.[1]
    const message = item?.msg ?? ''
    if (fieldName === 'supplier_id') nextErrors.supplier_id = message
    if (fieldName === 'items') nextErrors.items = message
  })

  return nextErrors
}
