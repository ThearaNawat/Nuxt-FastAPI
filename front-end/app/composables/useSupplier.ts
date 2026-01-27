export type supplier = { id: number; code: string; name: string; email: string; phone: string; address: string; description: string}
export const useSuppliers = () => {
    const getAllSupplier = async () => await $fetch<supplier[]>(`/api/supplier`)
    const create = async (payload: supplier) => await $fetch(`/api/supplier`, { method: 'POST', body: payload})
    const update = async (id: number, payload: supplier) => await $fetch(`/api/supplier/${id}`, { method: 'POST', body: payload})
    const remove = async (id: number[]) => await $fetch(`/api/supplier`, { method: 'DELETE', body: id})
    return { getAllSupplier, create, update, remove }
}