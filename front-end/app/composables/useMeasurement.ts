import type { MeasureError, Measurement } from '~~/shared/types/measurement'
import { MeasurementService } from '~/services/measurement.service'
export const useMeasurement = () => {
    
    const getAll = async () => await MeasurementService.getAll()
    const create = async (payload: Measurement) => await MeasurementService.create(payload)
    const update = async (id: number, payload: Measurement) => await MeasurementService.update(id, payload)
    const remove = async (ids: number[]) => await MeasurementService.delete(ids)

    return { getAll, create, update, remove }
}