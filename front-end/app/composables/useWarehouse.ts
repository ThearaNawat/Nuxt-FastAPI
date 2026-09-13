import type { Warehouse, WarehouseError } from "~~/shared/types/warehouse";
import { WarehouseService } from '~/services/warehouse.service'
export const useWarehouse = () => {
    const btnLoading = ref(false)
    const loading = ref(false)
    const { t } = useI18n()
    const { confirmDelete } = useConfirmDelete()
    const messageBox = MessageBox()
    const warehouses = ref<Warehouse[]>([]);
    const selectWarehouses = ref<any[]>([])
    const successMessage = () => messageBox.success(t('successMessage'))
    const errorMessage = () => messageBox.error(t('errorMessage'))
    const warningMessage = () => messageBox.warning(t('warningMessage'))
    const openDialog = ref(false)
    const editMode = ref(false)
    const warehouseForm = reactive<Warehouse>({ id: 0, warehouse_name: '', address: '', city: '', state: '', postal_code: '', country: ''})
    const errors = ref<WarehouseError>(WarehouseService.warehouseError());
    const onOpenDialogEdit = (item: any, canUpdate: boolean) => {
        if(canUpdate){
            editMode.value = true
            warehouseForm.id = item.data.id
            warehouseForm.warehouse_name = item.data.warehouse_name
            warehouseForm.address = item.data.address
            warehouseForm.city = item.data.city
            warehouseForm.state = item.data.state
            warehouseForm.postal_code = item.data.postal_code
            warehouseForm.country = item.data.country
            openDialog.value = true
        }
    }
    const close = () => {
        warehouseForm.id = 0
        warehouseForm.warehouse_name = ''
        warehouseForm.address = ''
        warehouseForm.city = ''
        warehouseForm.state = ''
        warehouseForm.postal_code = ''
        warehouseForm.country = ''
        openDialog.value = false
        editMode.value = false
        errors.value = WarehouseService.warehouseError()
    }
    const getAll = async () => {
        loading.value = true
        await WarehouseService.getAllWarehouse()
        .then((res) => {
            warehouses.value = res
            loading.value = false    
        })
        .catch((error) => {
            loading.value = false
        })
    }
    const deleteMany = async () => {
        if(!selectWarehouses.value.length) return
        confirmDelete(
            async () => {
                loading.value = true
                await WarehouseService.deleteManyWarehouse(selectWarehouses.value.map((item) => item.id))
                .then((res) => {
                    getAll()
                    successMessage()
                    loading.value = false

                })
                .catch((error) => {
                    errors.value = WarehouseService.applyWarehouseValidationErrors(error?.data?.data?.detail, errors.value)
                    loading.value = false
                    if (!errors.value) errorMessage()
                })
            }
        )
    }
    const create = async (data: Warehouse) => {
        loading.value = true
        btnLoading.value = true
        await WarehouseService.createWarehouse(data)
        .then((res) => {
            getAll()
            successMessage()
            loading.value = false
            btnLoading.value = false
            close()
        })
        .catch((error) => {
            errors.value = WarehouseService.applyWarehouseValidationErrors(error?.data?.data?.detail, errors.value)
            loading.value = false
            btnLoading.value = false
            if (!errors.value) errorMessage()
        })
    }
    const update = async (id: number, data: Warehouse) => {
        loading.value = true
        btnLoading.value = true
        await WarehouseService.updateWarehouse(id, data)
        .then((res) => {
            getAll()
            successMessage()
            loading.value = false
            btnLoading.value = false
            close()
        })
        .catch((error) => {
            errors.value = WarehouseService.applyWarehouseValidationErrors(error?.data?.data?.detail, errors.value)
            loading.value = false
            btnLoading.value = false
            if (!errors.value) errorMessage()
        })
    }


    return {
        warehouses,
        selectWarehouses,
        loading,
        btnLoading,
        openDialog,
        editMode,
        warehouseForm,
        getAll,
        deleteMany,
        create,
        update,
        onOpenDialogEdit,
        close,
        errors

    }
}