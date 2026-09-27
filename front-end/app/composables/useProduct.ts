export type product = {id: number; code: string; name: string; package: string; expire_date: string | Date | null; stock: number; description: string; category_id: number | null; review: number; images?: File[], measurement_id: number | null}
import type { category } from "~/composables/useCategory";
export const useProduct = ()=>{
    const nuxtApp = useNuxtApp()
    const axios = nuxtApp.$axios as any
    const category = async () => await $fetch<category[]>("/api/category");
    const getAllProduct = async () => await $fetch<product>(`/api/product`)
    const create = async (payload: FormData) => await $fetch('/product/create', { method: "POST", body: payload})
    const update = async (id: number, payload: FormData) => await $fetch(`/product/create/${id}`, { method: "POST", body: payload})
    const remove = async (id: number[]) => await $fetch(`/product/delete`, { method: "DELETE", id: id})
    return { category, getAllProduct, create, update, remove }
}