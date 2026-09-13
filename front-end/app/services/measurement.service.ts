import type { Measurement, MeasureError } from '~~/shared/types/measurement'
import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
export const MeasurementService = {

    measurementError(): MeasureError {
        return{ code: '', name: ''}
    },
    applyMeasurementValidationErrors(detail: any, errors: MeasureError): MeasureError {
        const nextErrors = { ...errors }
        
        if (typeof detail === 'string' || !Array.isArray(detail)) {
            return nextErrors
        }
        
        detail.forEach((item: any) => {
            const fieldName = item?.loc?.[1]
            if (fieldName === 'code') {
                nextErrors.code = item.msg
            }
            if (fieldName === 'name') {
                nextErrors.name = item.msg
            }
        })
        
        return nextErrors
    },

    createForm(): Measurement{
        return {
            id: 0,
            code: '',
            name: '',
            description: '',
            status: true
        }
    },

    filters(){
        return {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
            code: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
            description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
            status: { value: null, matchMode: FilterMatchMode.EQUALS },
        }
    },

    async getAll() { return await $fetch<Measurement[]>(`/api/measurement`) },
    async create(payload: Measurement) { return await $fetch(`/api/measurement`, { method: 'POST', body: payload}) },
    async update(id: number, payload: Measurement) { return await $fetch(`/api/measurement/${id}`, { method: 'POST', body: payload}) },
    async delete(ids: number[]) { return await $fetch(`/api/measurement`, { method: 'DELETE', body: ids}) }
}