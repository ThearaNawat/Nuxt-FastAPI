<template>
    <div id="stock-out">
        <DataTable
            v-model:selection="selection"
            paginator
            :rows="pagination.limit"
            :total-records="pagination.total"
            :rows-per-page-options="[5, 10, 20, 50, 100]"
            :value="data"
            :loading="loading"
            filter-display="menu"
            removable-sort
            reorderable-columns
            resizable-columns
            data-key="id"
            row-hover
            scrollable
            striped-rows
            size="small"
            scroll-height="500px"
            style="max-width: 1320px"
            @row-dblclick="openEditMode"
        >
      
            <Toolbar >
                <template #start>
                
                </template>
                <template #end>
                <Button :label="t('btnCreate')" icon="pi pi-plus" @click="onOpenDialog" />
                <Button :label="t('btnDelete')" icon="pi pi-trash" class="ml-2" @click="deleteMany" />
                </template>
            </Toolbar>
            <template #header>
                <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <IconField class="w-full md:max-w-md">
                    <InputIcon>
                    <i class="pi pi-search" />
                    </InputIcon>
                    <InputText size="small"  class="w-full" :placeholder="t('search')" />
                </IconField>
                <Button icon="pi pi-filter-slash" variant="link" @click="clearFilter" />
                </div>
            </template>

            <template #empty>{{ t('empty') }}</template>

            <Column selection-mode="multiple" :exportable="false" header-style="width: 2rem" />

            <Column :header="t('lblCode')" field="product.code" sortable style="min-width: 150px">
                <template #body="{ data }">
                <span class="font-medium">{{ data.product?.code ?? '-' }}</span>
                </template>
            </Column>

            <Column :header="t('product')" field="product.name" sortable style="min-width: 240px">
                <template #body="{ data }">
                <div class="flex flex-col">
                    <span class="font-semibold">{{ data.product?.name }}</span>
                </div>
                </template>
            </Column>
            <Column :header="t('package')" sortable style="min-width: 240px">
                <template #body="{ data }">
                <span 
                    v-if="data.product?.package && data.product?.measurement"
                >{{ `${data.product?.package} ${data.product?.measurement?.code}` }}</span>
                <span v-else>N/A</span>
                </template>
            </Column>

            <Column :header="t('expire_date')" sortable style="min-width: 160px">
                <template #body="{ data }">
                <span>{{ formatDate(data.product.expire_date) }}</span>
                </template>
            </Column>

            <Column :header="t('warehouse')" field="warehouse.warehouse_name" sortable style="min-width: 220px">
                <template #body="{ data }">
                    <Button v-if="data.warehouse?.warehouse_name" icon="pi pi-warehouse" size="small" variant="link" />
                    <span>{{ data.warehouse?.warehouse_name ?? '-' }}</span>
                </template>
            </Column>

            

            <Column :header="t('transaction_type')" field="transaction_type" sortable style="min-width: 180px">
                <template #body="{ data }">
                <Tag
                    :value="data.transaction_type"
                    :severity="data.transaction_type"
                    :icon="data.transaction_type"
                />
                </template>
            </Column>
            <Column :header="t('reservedQuantity')"  sortable style="min-width: 180px">
                <template #body="{ data }">
                <span>{{ data }}</span>
                </template>
            </Column>
            <Column :header="t('reserved_qty_pcs')" sortable style="min-width: 180px">
                <template #body="{ data }">
                <span>{{ data }}</span>
                </template>
            </Column>
            <Column :header="t('quantity')" field="quantity" sortable style="min-width: 130px">
                <template #body="{ data }">
                <Tag :value="data.quantity" severity="secondary" icon="pi pi-box" :rounded="true">
                    <template v-if="data.quantity && data.measurement" #default>{{`${data.quantity} ${data.measurement.code}`}}</template>
                    <template v-else #default>{{ 0 }}</template>
                </Tag>
                </template>
            </Column>

            <Column :header="t('qty_pcs')" field="quantity_pcs" sortable style="min-width: 140px">
                <template #body="{ data }">
                <span>{{ data.quantity_pcs ?? '-' }}</span>
                </template>
            </Column>

            <Column :header="t('broken')" sortable style="min-width: 130px">
                <template #body="{ data }">
                <Tag :value="data.quantity" severity="secondary" icon="pi pi-box" />

                </template>
            </Column>

            <Column :header="t('broken')" field="quantity_pcs" sortable style="min-width: 140px">
                <template #body="{ data }">
                <span>{{ data.quantity_pcs ?? '-' }}</span>
                </template>
            </Column>

            <Column :header="t('reference_number')" field="reference_number" sortable style="min-width: 180px" />

            <Column :header="t('remark')" field="reason" sortable style="min-width: 220px" />

            <Column :header="t('transfer_date')" field="created_at" sortable style="min-width: 160px">
                <template #body="{ data }">
                <span>{{ formatDate(data.created_at) }}</span>
                </template>
            </Column>

            <Column :header="t('updated_at')" field="updated_at" sortable style="min-width: 160px">
                <template #body="{ data }">
                <span>{{ formatDate(data.updated_at) }}</span>
                </template>
            </Column>
        </DataTable>
    </div>
</template>
<script lang="ts" setup>
    interface Props {
        btnLoading: boolean
        loading: boolean
        openDialog: boolean
        editMode: boolean
        data: []
        selection: any
        pagination: { page: 1, limit: 10, total: 0}
    }
    const { t } = useI18n()
    const props = defineProps<Props>()
    const events = defineEmits(['create','update','delete', 'clearFilter', 'onOpenDialog', 'onEditMode'])
    const create = () => events('create')
    const update = () => events('update')
    const openEditMode = () => events('onEditMode')
    const onOpenDialog = () => events('onOpenDialog')
    const clearFilter = () => events('clearFilter')
    const deleteMany = () => events('delete')
</script>