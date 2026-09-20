import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import type { FinancialRecord, FinancialRecordForm, FinancialRecordType } from '~~/shared/types/financial-record'

export const createFinancialRecordFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  category: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  counterparty: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  reference_number: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
})

export const FinancialRecordService = {
  list: async (recordType: FinancialRecordType) =>
    await $fetch<FinancialRecord[]>(`/api/${recordType}`),

  create: async (recordType: FinancialRecordType, payload: FinancialRecordForm) =>
    await $fetch(`/api/${recordType}`, { method: 'POST', body: payload }),

  update: async (recordType: FinancialRecordType, id: number, payload: FinancialRecordForm) =>
    await $fetch(`/api/${recordType}/${id}`, { method: 'POST', body: payload }),

  remove: async (recordType: FinancialRecordType, ids: number[]) =>
    await $fetch(`/api/${recordType}`, { method: 'DELETE', body: ids }),
}
