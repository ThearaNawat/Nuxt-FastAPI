import type { InvoiceForm, InvoiceErrors, Invoice } from '~~/shared/types/invoice'
import { FilterMatchMode, FilterOperator } from '@primevue/core/api'

export const createInvoiceFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  invoice_number: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  customer_id: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
  status: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
})

export const InvoiceService = {
  async getAllInvoices(query?: Record<string, any>) {
    // const url = query ? `/api/invoice?${query}` : '/api/invoice'
    return await $fetch(`/api/invoice`, {query}) as any
  },

  async createInvoice(payload: InvoiceForm) {
    return await $fetch('/api/invoice', { method: 'POST', body: payload })
  },

  async updateInvoice(id: number, payload: InvoiceForm) {
    return await $fetch(`/api/invoice/${id}`, { method: 'POST', body: payload })
  },

  async deleteInvoices(ids: number[]) {
    return await $fetch('/api/invoice', { method: 'DELETE', body: ids })
  },

  invoiceError(): InvoiceErrors {
    return { invoice_number: '', customer_id: '', amount: '' }
  },

  applyInvoiceValidationErrors(detail: any, errors: InvoiceErrors): InvoiceErrors {
    const nextErrors = { ...errors }
    if (typeof detail === 'string' || !Array.isArray(detail)) return nextErrors

    detail.forEach((item: any) => {
      const fieldName = item?.loc?.[1]
      if (fieldName === 'invoice_number') nextErrors.invoice_number = item.msg
      if (fieldName === 'customer_id') nextErrors.customer_id = item.msg
      if (fieldName === 'amount') nextErrors.amount = item.msg
    })

    return nextErrors
  },
}
