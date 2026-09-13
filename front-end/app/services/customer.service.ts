import type { Customer, CustomerErrors } from '~~/shared/types/customer'

export const CustomerService = {
    async getAllCustomer(): Promise<Customer[]> { return await $fetch<Customer[]>(`/api/customer`) },
    async createCustomer(payload: Customer) { return await $fetch(`/api/customer`, { method: 'POST', body: payload}) }, 
    async updateCustomer(id: number, payload: Customer) { return await $fetch(`/api/customer/${id}`, { method: 'POST', body: payload}) },
    async deleteCustomer(ids: number[]) { return await $fetch(`/api/customer`, {method: 'DELETE', body: ids}) },
    customerError(): CustomerErrors {
        return{ customer_code: '', customer_name: ''}
    },
    applyUserValidationErrors(detail: any, errors: CustomerErrors): CustomerErrors {
        const nextErrors = { ...errors }
        
        if (typeof detail === 'string' || !Array.isArray(detail)) {
            return nextErrors
        }
        
        detail.forEach((item: any) => {
            const fieldName = item?.loc?.[1]
            if (fieldName === 'customer_code') {
                nextErrors.customer_code = item.msg
            }
            if (fieldName === 'customer_name') {
                nextErrors.customer_name = item.msg
            }
        })
        
        return nextErrors
    } 
}   