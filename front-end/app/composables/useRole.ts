export type role = {
    id: number
    role_name: string
    description?: string | null
    status: boolean,
    menu: number[]
    created_at?: string | null
    updated_at?: string | null
}

export const useRole = () => {
    const roleList = async () => await $fetch<role[]>(`/api/role`)

    const create = async (payload: role) => await $fetch(`/api/role`, { method: 'POST', body: payload })

    const update = async (id: number, payload: role) => await $fetch(`/api/role/${id}`, { method: 'POST', body: payload })

    const remove = async (id: number) => await $fetch(`/api/role/${id}`, { method: 'DELETE' })

    const removeMany = async (ids: number[]) => {
        await Promise.all(ids.map((id) => remove(id)))
    }

    return { roleList, create, update, remove, removeMany }
}
