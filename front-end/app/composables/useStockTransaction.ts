import { FilterMatchMode, FilterOperator } from "@primevue/core/api"
import type { StockTransactionForm, Errors, ValidationDetailItem, StockTransactionCreate, StockTransactionDetailCreate, TransactionType } from '~~/shared/types/stocktransaction'

export const useStockTransaction = () => {
    const createStockTransactionFilters = () => ({
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        'product.code': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        'product.name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
        'warehouse.warehouse_name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
        'measurement.code': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
        transaction_type: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        quantity: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        reference_number: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
        transfer_number: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
        reason: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
    })
    
    const createEmptyStockTransactionForm = (): StockTransactionForm => ({
        id: 0,
        product_id: null,
        warehouse_id: null,
        measurement_id: null,
        transaction_type: null,
        quantity: 0,
        reason: '',
        reference_number: '',
        to_warehouse_id: null,
        transaction_number: ''
    })

    const createEmptyStockTransactionDetail = (): StockTransactionDetailCreate[] => [{
        product_id: null,
        measurement_id: null,
        quantity: 0,
        unit_price: 0,
        currency_id: null,
        total_price: 0,
        exchange_rate: 0
    }]
    const transactionType: TransactionType = 'STOCK_IN'
    const createEmptyStockTransaction = (): StockTransactionCreate => ({
        id: 0,
        warehouse_id: null,
        transaction_type: transactionType,
        reason: '',
        reference_number: '',
        to_warehouse_id: null,
        transaction_number: '',
        details: createEmptyStockTransactionDetail()
    })
    
    const createStockTransactionErrors = (): Errors => ({
        product_id: null,
        warehouse_id: null,
        measurement_id: null,
        transaction_type: '',
        quantity: '',
    })
    
    const applyStockTransactionValidationErrors = (detail: unknown, errors: Errors): Errors => {
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
    
    const getAll = async (query: string = '') => query ? await $fetch(`/api/stock-transaction?${query}`) : await $fetch(`/api/stock-transaction`)
    const create = async (payload: StockTransactionCreate) => await $fetch(`/api/stock-transaction`, { method: 'POST', body: payload}) 
    const update = async (id: number, payload: StockTransactionCreate) => await $fetch(`/api/stock-transaction/${id}`, { method: 'POST', body: payload}) 
    const remove = async (id: number[]) => await $fetch(`/api/stock-transaction`, { method: 'DELETE', body: id}) 
    const createStockTransaction = async (data: StockTransactionCreate) => await $fetch(`/api/stock-transaction`, { method: 'POST', body: data })
    return {
        createStockTransaction,
        applyStockTransactionValidationErrors,
        createEmptyStockTransactionForm,
        createStockTransactionErrors,
        createStockTransactionFilters,
        getAll,
        create,
        update,
        remove,
        createEmptyStockTransaction
    }
}