export type product = {id: number; code: string; name: string; package: string; expire_date: string | Date | null; stock: number; description: string; category_id: number | null; review: number; images?: File[], measurement_id: number | null}
import type { category } from "~/composables/useCategory";
export const useProduct = ()=>{
    const nuxtApp = useNuxtApp()
    const axios = nuxtApp.$axios as any
    const category = async () => await $fetch<category[]>(`/api/category`);
    const getAllProduct = async () => (await axios.get('/product')).data as product[];
    const create = async (payload: FormData) => (await axios.post('/product/create', payload)).data
    const update = async (id: number, payload: FormData) => (await axios.post(`/product/update/${id}`, payload)).data
    const remove = async (id: number[]) => (await axios.delete('/product/delete', { data: id })).data
    return { category, getAllProduct, create, update, remove }
}