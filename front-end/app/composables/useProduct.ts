export type product = {id: number; code: string; name: string; package: string; expire_date: Date | null; stock: number; description: string; category_id: number | null; review: number, images: [] | ''}
import type { category } from "~/composables/useCategory";
export const useProduct = ()=>{
    const category = async () => await $fetch<category[]>(`/api/category`);
    const getAllProduct = async () => await $fetch<product[]>(`/api/product`);
    const create = async (payload: product) => await $fetch(`/api/product`, { method: 'POST', body: payload })
    const update = async (id: number, payload: product) => await $fetch(`/api/product/${id}`,{method: 'POST', body: payload})
    const remove = async (id: number[]) => await $fetch(`/api/product`, { method: 'DELETE', body: id})
    return { category, getAllProduct, create, update, remove }
}