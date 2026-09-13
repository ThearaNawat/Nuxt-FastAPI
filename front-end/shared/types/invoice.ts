export type Invoice = {
  id?: number
  invoice_number: string
  order_id: number | null
  customer_id: number | null
  invoice_date?: string | null
  due_date?: string | null
  amount: number
  paid_amount: number
  status: string
  customer?: {
    id: number
    customer_name: string
  }
  order?: {
    id: number
    order_number: string
  }
}

export type InvoiceForm = {
  id?: number
  invoice_number: string
  order_id: number | null
  customer_id: number | null
  invoice_date: Date | null
  due_date: Date | null
  amount: number
  paid_amount: number
  status: string
}

export type InvoiceErrors = {
  invoice_number: string
  customer_id: string
  amount: string
}

export const createEmptyInvoiceForm = (): InvoiceForm => ({
  invoice_number: '',
  order_id: null,
  customer_id: null,
  invoice_date: new Date(),
  due_date: null,
  amount: 0,
  paid_amount: 0,
  status: 'draft',
})

export const createInvoiceErrors = (): InvoiceErrors => ({
  invoice_number: '',
  customer_id: '',
  amount: '',
})
