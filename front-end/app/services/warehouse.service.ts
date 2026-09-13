import type { Warehouse } from "~~/shared/types/warehouse";
export const WarehouseService = {
    async getAllWarehouse() { return await $fetch<Warehouse[]>(`/api/warehouse`) },
    async createWarehouse(payload: Warehouse) { return await $fetch(`/api/warehouse`, { method: 'POST', body: payload}) },
    async updateWarehouse(id: number, payload: Warehouse) { return await $fetch(`/api/warehouse/${id}`, { method: 'POST', body: payload}) },
    async deleteWarehouse(id: number[]) { return await $fetch(`/api/warehouse/delete/${id}`, {method: 'DELETE', body: id}) },
    async deleteManyWarehouse(ids: number[]) { return await $fetch(`/api/warehouse`, { method: 'DELETE', body: ids}) },
    warehouseError() {
        return {
            warehouse_name: '',
        }
    },
    applyWarehouseValidationErrors(detail: any, errors: WarehouseError): WarehouseError {
        const nextErrors = { ...errors }
        
        if (typeof detail === 'string' || !Array.isArray(detail)) {
            return nextErrors
        }
        
        detail.forEach((item: any) => {
            const fieldName = item?.loc?.[1]
            if (fieldName === 'warehouse_name') {
                nextErrors.warehouse_name = item.msg
            }
        })
        
        return nextErrors
    } 

}