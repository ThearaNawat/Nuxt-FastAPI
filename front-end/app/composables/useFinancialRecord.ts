import { FinancialRecordService } from '~/services/financial-record.service'
import type { FinancialRecordForm, FinancialRecordType } from '~~/shared/types/financial-record'

export const useFinancialRecord = (recordType: FinancialRecordType) => ({
  list: () => FinancialRecordService.list(recordType),
  create: (payload: FinancialRecordForm) => FinancialRecordService.create(recordType, payload),
  update: (id: number, payload: FinancialRecordForm) => FinancialRecordService.update(recordType, id, payload),
  remove: (ids: number[]) => FinancialRecordService.remove(recordType, ids),
})
