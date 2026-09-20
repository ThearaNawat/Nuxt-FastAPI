export type FinancialRecordType = 'income' | 'expense'

export type FinancialRecord = {
  id: number
  transaction_date: string | null
  amount: number | string
  category: string
  counterparty: string | null
  reference_number: string | null
  description: string | null
}

export type FinancialRecordForm = {
  id?: number
  transaction_date: Date | null
  amount: number
  category: string
  counterparty: string
  reference_number: string
  description: string
}

export type FinancialRecordErrors = {
  transaction_date: string
  amount: string
  category: string
}

export const createEmptyFinancialRecordForm = (): FinancialRecordForm => ({
  transaction_date: new Date(),
  amount: 0,
  category: '',
  counterparty: '',
  reference_number: '',
  description: '',
})

export const createFinancialRecordErrors = (): FinancialRecordErrors => ({
  transaction_date: '',
  amount: '',
  category: '',
})
