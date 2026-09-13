export interface Warehouse {
    id: number;
    warehouse_name: string;
    address: string;
    city: string;
    state: string;
    postal_code: string;
    country: string;
}
export interface WarehouseError {
    warehouse_name: string;
}