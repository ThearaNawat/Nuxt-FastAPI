import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import type { user } from '~/composables/useUsers'

export type UserForm = user
export type UserErrors = { username: string; email: string; password: string; confirm_password: string }

export const createUserFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  username: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
  status: { value: null, matchMode: FilterMatchMode.EQUALS },
  email: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
  created_at: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
  updated_at: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
  role_id: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] }
})

export const createEmptyUserForm = (): UserForm => ({
  id: 0,
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  status: true,
  role_id: null
})

export const createUserErrors = (): UserErrors => ({ username: '', email: '', password: '', confirm_password: '' })

export const applyUserValidationErrors = (detail: any, errors: UserErrors): UserErrors => {
  const nextErrors = { ...errors }

  if (typeof detail === 'string' || !Array.isArray(detail)) {
    return nextErrors
  }

  detail.forEach((item: any) => {
    const fieldName = item?.loc?.[1]
    if (fieldName === 'username') {
      nextErrors.username = item.msg
    }
    if (fieldName === 'email') {
      nextErrors.email = item.msg
    }
    if (fieldName === 'password') {
      nextErrors.password = item.msg
    }
    if (fieldName === 'confirm_password') {
      nextErrors.confirm_password = item.msg
    }
  })

  return nextErrors
}
