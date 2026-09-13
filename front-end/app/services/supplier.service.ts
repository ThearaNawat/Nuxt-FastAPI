import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import type { supplier } from '~/composables/useSupplier'

export type SupplierForm = supplier
export type SupplierErrors = { code: string; name: string; email: string; phone: string }

export const createSupplierFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  code: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  email: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  phone: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  address: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] }
})

export const createEmptySupplierForm = (): SupplierForm => ({
  id: 0,
  name: '',
  code: '',
  description: '',
  phone: '',
  email: '',
  address: ''
})

export const createSupplierErrors = (): SupplierErrors => ({ code: '', name: '', email: '', phone: '' })

export const applySupplierValidationErrors = (detail: any, errors: SupplierErrors): SupplierErrors => {
  const nextErrors = { ...errors }

  if (typeof detail === 'string' || !Array.isArray(detail)) {
    return nextErrors
  }

  detail.forEach((item: any) => {
    const fieldName = item?.loc?.[1]
    if (fieldName === 'name') {
      nextErrors.name = item.msg
    }
    if (fieldName === 'code') {
      nextErrors.code = item.msg
    }
    if (fieldName === 'email') {
      nextErrors.email = item.msg
    }
    if (fieldName === 'phone') {
      nextErrors.phone = item.msg
    }
  })

  return nextErrors
}
