export type Measurement = {
    id?: number
    code: string
    name: string
    description: string
    status: boolean
}

export type MeasureError = {
    code: string
    name: string
}