export type StockTransactionForm = {
    id: number | null
    warehouse_id: number | null
    measurement_id: number | null
    to_warehouse_id: number | null
    transaction_number?: string
    reference_number?: string
    product_id: number | null
    quantity: number
    reason: string
    transaction_type: string | null
}

export interface StockTransactionDetailCreate {
  product_id: number | null
  measurement_id: number | null
  quantity: number
  unit_price: number
  currency_id: number | null
  total_price: number
  exchange_rate: number
}


export interface StockTransactionCreate {
  id?: number
  warehouse_id: number | null
  to_warehouse_id: number | null
  transaction_type: TransactionType
  // transaction_date: string
  reference_number: string
  transaction_number: string
  reason: string

  details: StockTransactionDetailCreate[]
}

export type TransactionType =
  | 'STOCK_IN'
  | 'STOCK_OUT'
  | 'ADJUSTMENT'
  | 'RETURN'
  | 'DAMAGE'
  | 'QUARANTINE'
  | 'INTERNAL_TRANSFER'

export type Errors = {
    warehouse_id: string | null | undefined,
    measurement_id: string | null | undefined
    product_id: string | null | undefined
    quantity: string | null | undefined
    transaction_type: string | null | undefined
}


export type ValidationDetailItem = {
  loc?: Array<string | number>
  msg?: string
}
