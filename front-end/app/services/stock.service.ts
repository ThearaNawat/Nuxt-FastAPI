import { FilterMatchMode, FilterOperator } from '@primevue/core/api'

export type StockForm = {
  id?: number
  product_id: number | null
  warehouse_id: number | null
  measurement_id: number | null
  measurement_reserved_id: number |  null
  transaction_type: string | null
  quantity: number | 0
  reserved_qty: number | 0
  reason: string
  reference_number?: string | null
}

export type StockErrors = {
  product_id: string
  warehouse_id: string
  measurement_id: string
  transaction_type: string
  quantity: string
}

type ValidationDetailItem = {
  loc?: Array<string | number>
  msg?: string
}

export const createStockFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  'product.code': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
  'product.name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  'warehouse.warehouse_name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  'measurement.code': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  transaction_type: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
  quantity: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
  reference_number: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  reason: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
})

export const createEmptyStockForm = (): StockForm => ({
  product_id: null,
  warehouse_id: null,
  measurement_id: null,
  transaction_type: null,
  quantity: 0,
  reason: '',
  measurement_reserved_id: null,
  reserved_qty: 0,
  reference_number: null
})

export const createStockErrors = (): StockErrors => ({
  product_id: '',
  warehouse_id: '',
  measurement_id: '',
  transaction_type: '',
  quantity: '',
})

export const applyStockValidationErrors = (detail: unknown, errors: StockErrors): StockErrors => {
  const nextErrors = { ...errors }
  if (typeof detail === 'string' || !Array.isArray(detail)) return nextErrors

  detail.forEach((item: ValidationDetailItem) => {
    const fieldName = item?.loc?.[1]
    const message = item?.msg ?? ''
    if (fieldName === 'product_id') nextErrors.product_id = message
    if (fieldName === 'warehouse_id') nextErrors.warehouse_id = message
    if (fieldName === 'measurement_id') nextErrors.measurement_id = message
    if (fieldName === 'transaction_type') nextErrors.transaction_type = message
    if (fieldName === 'quantity') nextErrors.quantity = message
  })

  return nextErrors
}
