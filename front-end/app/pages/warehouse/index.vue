<template>
    <div id="warehouse">
        <WarehouseDatatable
            :warehouses="warehouses"
            :loading="loading"
            v-model:selectWarehouses="selectWarehouses"
            v-model:openDialog="openDialog"
            :openDialogEdit="openDialogEdit"
            :canCreate="canCreate"
            :canUpdate="canUpdate"
            :canDelete="canDelete"
            :deleteMany="deleteMany"
        />
        <WarehouseForm
            :openDialog="openDialog"
            :editMode="editMode"
            :warehouseForm="warehouseForm"
            :errors="errors"
            :btnLoading="btnLoading"
            @handleSubmit="handleSubmit"
            @closeDialog="close"
        />
    </div>
</template>
<script lang="ts" setup>
    definePageMeta({
        layout: 'dashboard'
    })

    import WarehouseForm from '~/components/warehouse/WarehouseForm.vue'
    import WarehouseDatatable from '~/components/warehouse/WarehouseDatatable.vue'
    const { 
        btnLoading, 
        close, 
        create,
        deleteMany, 
        editMode, 
        errors, 
        getAll, 
        loading, 
        onOpenDialogEdit, 
        openDialog, 
        selectWarehouses, 
        update, 
        warehouseForm, 
        warehouses,
    } = useWarehouse()
    const { t } = useI18n()
    const { hasPermission } = useFunction()
    const route = useRoute()
    const canCreate = computed(() => hasPermission(route.name as string, 'create'))
    const canUpdate = computed(() => hasPermission(route.name as string, 'update'))
    const canDelete = computed(() => hasPermission(route.name as string, 'delete'))
    const canView = computed(() => hasPermission(route.name as string, 'access'))
    const handleSubmit = () => {
        if(!editMode.value)
            create(warehouseForm)
        else
            update(warehouseForm.id, warehouseForm)
    }
    const openDialogEdit = (item: any) => {
        onOpenDialogEdit(item, canUpdate.value)
    }
    onMounted(getAll)
</script>