import { InvoiceService } from '~/services/invoice.service'
import type { InvoiceForm } from '~~/shared/types/invoice'

export const useInvoice = () => {
  const list = async (query?: Record<string, any>) => await InvoiceService.getAllInvoices(query)
  const create = async (payload: InvoiceForm) => await InvoiceService.createInvoice(payload)
  const update = async (id: number, payload: InvoiceForm) => await InvoiceService.updateInvoice(id, payload)
  const remove = async (ids: number[]) => await InvoiceService.deleteInvoices(ids)

  return { list, create, update, remove }
}
