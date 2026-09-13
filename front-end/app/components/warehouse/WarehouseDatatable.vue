<template>
    <div id="warehouse-datatable">
        <DataTable
            removable-sort
            resizable-columns
            reorderable-columns
            row-hover
            paginator
            size="small"
            :global-filter-fields="['warehouse_name', 'state', 'city', 'address', 'postal_code', 'country']"
            filter-display="menu"
            :sort-order="-1"
            data-key="id"
            :value="warehouses"
            :loading="loading"
            :selection="selectWarehouses"
            @update:selection="(val) => emit('update:selectWarehouses', val)"
            @row-dblclick="openDialogEdit"
            :rows="10" 
            sort-mode="multiple"
            scrollable
            scroll-height="500px"
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            style="max-width: 1320px"
        >
        <Toolbar>
            <template #end>
                <Button :label="t('btnCreate')" icon="pi pi-plus" v-if="canCreate" @click="emit('update:openDialog', true)"></Button>
                <Button :label="t('btnDelete')" icon="pi pi-trash" v-if="canDelete" class="mx-2" @click="deleteMany"></Button>
            </template>
        </Toolbar>
        <template #header>
            <div class="flex justify-between">
                <Button icon="pi pi-filter-slash" variant="link"></Button>
            </div>
        </template>
        <template #empty>{{ t('empty') }}</template>
        <Column selection-mode="multiple"  :exportable="false" header-style="width: 2rem"></Column>
        
        <Column :header="t('lblName')" field="warehouse_name" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('country')" field="country" filter-field="country" sortable style="min-width: 200px">

            <template #filter="{ filterModel }">
                <InputText v-model="filterModel.value" :placeholder="t('search')" />
            </template>
        </Column>
        <Column :header="t('state')" field="state" filter-field="state" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('city')" field="city" filter-field="city" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('postal_code')" field="postal_code" filter-field="postal_code" sortable style="min-width: 200px">
            
            <template #filter="{ filterModel }">
                <InputText v-model="filterModel.value" :placeholder="t('search')" />
            </template>
        </Column>
        
        <Column :header="t('lblAddress')" field="address" filter-field="address" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>

        </DataTable>
    </div>
</template>
<script setup lang="ts">
    import type { Warehouse } from '~~/shared/types/warehouse'
    const { t } = useI18n()
    const props = defineProps<{
        warehouses: Warehouse[],
        loading: boolean,
        selectWarehouses: any[],
        canCreate: boolean,
        canUpdate: boolean,
        canDelete: boolean,
        openDialog: boolean,
        deleteMany: () => void,
        openDialogEdit: (item: any) => void,
    }>()
    const emit = defineEmits<{
        (e: 'update:selectWarehouses', value: any[]): void;
        (e: 'update:openDialog', value: boolean): void;
    }>()
</script>