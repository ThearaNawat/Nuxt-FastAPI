<template>
    <div id="customer">
        <DataTable
            removable-sort
            resizable-columns
            reorderable-columns
            row-hover
            :value="customers"
            paginator
            :loading="loading"
            v-model:selection="selectCustomers"
            size="small"
            :global-filter-fields="['customer_name', 'phone_number', 'customer_code', 'email', 'contact_person', 'payment_term', 'billing_address', 'shipping_address']"
            filter-display="menu"
            :sort-order="-1"
            data-key="id"
            :rows="10" 
            sort-mode="multiple"
            scrollable
            scroll-height="500px"
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            style="max-width: 1320px"
            @row-dblclick="handleEdit"
        >
        <Toolbar>
            <template #end>
                <Button :label="t('btnCreate')" icon="pi pi-plus" v-show="canCreate" @click="openDialog = true"></Button>
                <Button :label="t('btnDelete')" icon="pi pi-trash" v-show="canDelete" class="mx-2" @click="deleteMany"></Button>
                <Button :label="t('btnExport')" icon="pi pi-file-excel" ></Button>
            </template>
        </Toolbar>
        <template #header>
            <div class="flex justify-between">
                <Button icon="pi pi-filter-slash" variant="link"></Button>
            </div>
        </template>
        <template #empty>{{ t('empty') }}</template>
        <Column selection-mode="multiple"  :exportable="false" header-style="width: 2rem"></Column>
        <Column :header="t('lblCode')" field="customer_code" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('lblName')" field="customer_name" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('payment_term')" field="payment_terms" filter-field="payment_terms" sortable class="text-orange-700" style="min-width: 200px">
            
            
        </Column>
        <Column :header="t('contact')" field="contact_person" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('lblPhone')" field="phone_number" sortable style="min-width: 200px">
            <template #body = "{ data }">
                <Button icon="pi pi-phone" size="small" variant="link"></Button>
                {{ data.phone_number }}
            </template>
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('email')" field="email" sortable style="min-width: 200px">
            <template #body="{ data }">
                <Button icon="pi pi-envelope pi-spin" size="small" variant="link"></Button>
                <span>{{ data.email }}</span>
            </template>
            <template #filter="{ filterModel }">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('credit_limit')" field="credit_limit" sortable style="min-width: 200px">
            
        </Column>
        <Column :header="t('lblAddress')" field="shipping_address" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>

        <Column :header="t('lblAddress')" field="billing_address" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>

        </DataTable>

        
        <CustomerDialog 
            :openDialog="openDialog" 
            :editMode="editMode" 
            :customerForm="customerForm" 
            :errors="errors" 
            :btnLoading="btnLoading" 
            @closeDialog="close" 
            @handleSubmit="handleSubmit"
        />
    </div>
</template>
<script lang="ts" setup>
    definePageMeta({
        layout: 'dashboard'
    })
    import CustomerDialog from '~/components/customer/CustomerDialog.vue'
    const { createCustomer, customers, errors, fetchCustomers, loading, updateCustomer, customerForm, close, btnLoading, openDialog, onOpenDialogEdit, editMode, selectCustomers, deleteMany } = useCustomer()
    const { t } = useI18n()
    const { hasPermission } = useFunction()
    const route = useRoute()
    const canCreate = computed(() => hasPermission(route.name as string, 'create'))
    const canUpdate = computed(() => hasPermission(route.name as string, 'update'))
    const canDelete = computed(() => hasPermission(route.name as string, 'delete'))
    const canView = computed(() => hasPermission(route.name as string, 'access'))
    const handleEdit = (item: any) => {
        onOpenDialogEdit(item, canUpdate.value)
    }
    const handleSubmit = () => {
        if(!editMode.value)
            createCustomer(customerForm)
        else
            updateCustomer(customerForm.id, customerForm)
    }
    onMounted(() => {
        fetchCustomers()
    })
    
</script>