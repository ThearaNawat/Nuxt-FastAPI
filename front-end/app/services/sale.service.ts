import { FilterMatchMode, FilterOperator } from '@primevue/core/api'

export type SaleForm = {
  id?: number
  order_number: string
  customer_id: number | null
  order_date: Date | null 
  required_date: Date | null 
  shipped_date: Date | null
  status: string
  notes: string
}

export type SaleErrors = {
  order_number: string
  customer_id: string
}

export const createSaleFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  order_number: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  customer_id: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
  status: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] }
})

export const createEmptySaleForm = (): SaleForm => ({
  order_number: '',
  customer_id: null,
  order_date: new Date(),
  required_date: null,
  shipped_date: null,
  status: 'pending',
  notes: ''
})

export const createSaleErrors = (): SaleErrors => ({
  order_number: '',
  customer_id: ''
})

export const applySaleValidationErrors = (detail: any, errors: SaleErrors): SaleErrors => {
  const nextErrors = { ...errors }
  if (typeof detail === 'string' || !Array.isArray(detail)) return nextErrors

  detail.forEach((item: any) => {
    const fieldName = item?.loc?.[1]
    if (fieldName === 'order_number') nextErrors.order_number = item.msg
    if (fieldName === 'customer_id') nextErrors.customer_id = item.msg
  })

  return nextErrors
}
