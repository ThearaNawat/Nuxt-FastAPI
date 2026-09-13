import type { Currency } from '~~/shared/types/currency'
export const useCurrency = () => {
    const getAllCurrency = async () => await $fetch<Currency[]>('/api/currency')

    return {
        getAllCurrency
    }
}