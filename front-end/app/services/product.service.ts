import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import type { product } from '~/composables/useProduct'

export type ProductForm = Omit<product, 'expire_date'> & { expire_date: Date | null; images: File[] }

export const createProductFilters = () => ({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  code: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  review: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  package: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
  expire_date: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
  category_id: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
  measurement_id: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] }
})

export const createEmptyProductForm = (): ProductForm => ({
  id: 0,
  code: '',
  name: '',
  expire_date: null,
  package: '',
  description: '',
  stock: Math.floor(Math.random() * 1000),
  review: Math.floor(Math.random() * 100),
  category_id: null,
  images: [],
  measurement_id: null
})

export const parseDate = (value: string | Date | null) => {
  if (!value) return null
  if (value instanceof Date) return value

  let normalized = value
  if (normalized.indexOf('-') > 0) {
    normalized = normalized.replaceAll('-', '/')
  }

  const [year, month, day] = normalized.split('/')
  if (year && month && day) {
    return new Date(Number(year), Number(month) - 1, Number(day.substring(0, 2)))
  }

  return new Date(normalized)
}

export const toLocalDateString = (value: Date): string => {
  const year = value.getFullYear()
  const month = String(value.getMonth() + 1).padStart(2, '0')
  const day = String(value.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export const formatDate = (value: string | Date | null) => {
  if (!value) return ''
  const date = value instanceof Date ? value : parseDate(value)
  if (!date || Number.isNaN(date.getTime())) return ''

  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

export const buildProductFormData = (product: ProductForm) => {
  const formData = new FormData()
  formData.append('code', product.code)
  formData.append('name', product.name)

  if (product.description) {
    formData.append('description', product.description)
  }
  if (product.expire_date) {
    const expireDateValue = toLocalDateString(product.expire_date as Date)
    formData.append('expire_date', expireDateValue)
  }
  if (product.package) {
    formData.append('package', product.package)
  }
  if (product.stock != null) {
    formData.append('stock', String(product.stock))
  }
  if (product.category_id != null) {
    formData.append('category_id', String(product.category_id))
  }
  if (product.measurement_id) {
    formData.append('measurement_id', String(product.measurement_id))
  }
  if (product.review != null) {
    formData.append('review', String(product.review))
  }
  if (product.images && product.images.length > 0) {
    product.images.forEach((file) => {
      const fileToAppend = file instanceof File ? file : (file && 'file' in file ? (file as { file: File }).file : null)
      if (fileToAppend instanceof File) {
        formData.append('images', fileToAppend)
      }
    })
  }

  return formData
}

export const getValueStock = (value: number) => {
  if (value <= 25) return 'Low'
  if (value <= 500) return 'Medium'
  return 'Hight'
}

export const getSeverity = (value: number) => {
  if (value <= 25) return 'danger'
  if (value <= 500) return 'info'
  return 'success'
}

export const getIconStock = (status: string) => {
  if (status === 'Low') return 'pi pi-arrow-down'
  if (status === 'Medium') return 'pi pi-arrows-v'
  return 'pi pi-arrow-up'
}
