export type user = {id: number; username: string; email: string; password: string, confirm_password: string,status: boolean}

export const useUsers = () => {
    const userList = async () => await $fetch<user[]>(`/api/user`)

    const create = async (payload: user) => await $fetch(`/api/user`, { method: 'POST', body: payload })

    const update = async (id: number, payload: user) => await $fetch(`/api/user/${id}`, { method: 'POST', body: payload})

    const remove = async (id: number) => await $fetch(`/api/user/${id}`, { method: 'DELETE'})

    const removeMany = async (ids: number[]) => await $fetch(`/api/user`, { method: 'DELETE', body: ids })
    
    return { userList, create, update, remove, removeMany}
    
}