export interface Menu {id: number, label: string, path: string, icon: string, display_order: number, type: string, is_active: boolean, parent_id: number | null }
export const useMenu = () => {
    const getMenuTree = async () => await $fetch(`/api/menu/index.menu`)
    const getAllMenu = async () => await $fetch(`/api/menu`)
    const create = async (payload: Menu) => await $fetch(`/api/menu`, { method: 'POST', body: payload })
    const update = async (id: number, payload: Menu) => await $fetch(`/api/menu/${id}`, { method: 'PUT', body: payload})
    const remove = async (id: number) => await $fetch(`/api/menu/${id}`, { method: 'DELETE'})

    return { getAllMenu, create, update, remove, getMenuTree }
}