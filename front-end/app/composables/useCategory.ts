export type category = { id: number, code: string, name: string, description: string }
export const useCategory = () => {
    const getAllCategory = async () => await $fetch<category[]>(`/api/category`)
    const create = async (payload: category) => await $fetch(`/api/category`, { method: 'POST', body: payload})
    const update = async (id: number, payload: category) => await $fetch(`/api/category/${id}`, { method: 'POST', body: payload})
    const remove = async (payload: number[]) => await $fetch(`/api/category`, { method: 'DELETE', body: payload})
    return { getAllCategory, create, update, remove}
}