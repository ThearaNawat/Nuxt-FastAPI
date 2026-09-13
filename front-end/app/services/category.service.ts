import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import type { category } from '~/composables/useCategory'

export type CategoryForm = category
export type CategoryErrors = { code: string; name: string }

export const createCategoryFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  code: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] }
})

export const createEmptyCategoryForm = (): CategoryForm => ({
  id: 0,
  name: '',
  code: '',
  description: ''
})

export const createCategoryErrors = (): CategoryErrors => ({ code: '', name: '' })

export const applyCategoryValidationErrors = (detail: any, errors: CategoryErrors): CategoryErrors => {
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
  })

  return nextErrors
}
