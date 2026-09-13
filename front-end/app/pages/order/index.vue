<template>
    <div id="order">
        <DataTable
            paginator
            :rows="10"
            :rowsPerPageOptions="[5, 10, 20, 50, 100]"
            :value="saleList"
            :loading="loading"
            v-model:filters="filters"
            v-model:selection="selectSales"
            :global-filter-fields="['order_number', 'customer_id', 'status']"
            filter-display="menu"
            data-key="id"
            @row-dblclick="openEditDialog"
            size="small"
            striped-rows
            row-hover
            scrollable
            scroll-height="500px"
        >
            <Toolbar>
                <template #end>
                    <Button label="Create" icon="pi pi-plus" @click="openCreateDialog" />
                    <Button label="Delete" icon="pi pi-trash" class="ml-2" @click="deleteMany" />
                </template>
            </Toolbar>
            <template #header>
                <div class="flex justify-between">
                    <IconField>
                        <InputIcon><i class="pi pi-search" /></InputIcon>
                        <InputText v-model="filters['global'].value" :placeholder="t('search')" />
                    </IconField>
                    <Button icon="pi pi-filter-slash" @click="clearFilter" variant="link" />
                </div>
            </template>
            <Column selection-mode="multiple" header-style="width: 2rem" />
            <Column :header="t('order_number')" field="order_number" sortable />
            <Column :header="t('customer')" field="customer_id" sortable>
                <template #body="{ data }">
                    {{ customerOptions.find((customer: any) => customer.id === data.customer_id)?.customer_name || data.customer_id }}
                </template>
            </Column>
            <Column :header="t('status')" field="status" sortable >
                <template #body="{ data }">
                    <Tag :value="t(data.status)" :severity="getStatusSeverity(data.status)"></Tag>
                </template>
            </Column>
            <Column :header="t('order_date')" field="order_date" sortable>
                <template #body="{ data }">
                    <Button v-if="data.order_date" icon="pi pi-calendar" size="small" variant="link"></Button>
                    <span>{{ formatDate(data.order_date) }}</span>
                </template>
            </Column>
            <Column :header="t('required_date')" field="required_date" sortable>
                <template #body="{ data }">
                    <Button v-if="data.required_date" icon="pi pi-calendar" size="small" variant="link"></Button>
                    <span>{{ formatDate(data.required_date) }}</span>
                </template>
            </Column>
            <Column :header="t('shipped_date')" field="shipped_date" sortable>
                <template #body="{ data }">
                    <Button v-if="data.shipped_date" icon="pi pi-calendar" size="small" variant="link"></Button>
                    <span>{{ formatDate(data.shipped_date) }}</span>
                </template>
            </Column>
            <Column :header="t('notes')" field="notes" sortable>
                <template #body="{ data }">
                    <span>{{ data.notes }}</span>
                </template>
            </Column>
            <template #empty>{{ t('empty') }}</template>
        </DataTable>

        <Dialog :visible="openDialog" :closable="false" style="width: 520px">
            <template #header>
                <Divider>
                    <Button icon="pi pi-shopping-cart" variant="link" style="font-size: 1.7rem;"></Button>
                    <span v-if="!editMode" class="ml-2 text-xl">{{ t('lblHeaderCreate').replace('[0]', t('order')) }}</span>
                    <span v-else class="ml-2 text-xl">{{ t('lblHeaderUpdate').replace('[0]', t('order')) }}</span>
                </Divider>
            </template>
            <template #default>
                <InputGroup class="mt-2">
                    <InputGroupAddon><Button icon="pi pi-hashtag" variant="link" /></InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText v-model="saleForm.order_number" :invalid="Boolean(errors.order_number)" />
                        <label>{{ t('order_number') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message v-if="errors.order_number" severity="error" size="small">{{ errors.order_number }}</Message>

                <InputGroup class="mt-2">
                    <InputGroupAddon><Button icon="pi pi-user" variant="link" /></InputGroupAddon>
                    <FloatLabel variant="on">
                        <Select
                            v-model="saleForm.customer_id"
                            :options="customerOptions"
                            option-label="customer_name"
                            option-value="id"
                            show-clear
                            :invalid="Boolean(errors.customer_id)"
                        />
                        <label>{{ t('customer') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message v-if="errors.customer_id" severity="error" size="small">{{ errors.customer_id }}</Message>

                <InputGroup class="mt-2">
                    <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
                    <FloatLabel variant="on">
                        <DatePicker
                            show-clear
                            icon-display="input"
                            v-model="saleForm.order_date"
                            date-format="dd-mm-yy"
                            update-model-type="date"
                        >
                        </DatePicker>
                        <label>{{ t('order_date') }}</label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
                    <FloatLabel variant="on">
                        <DatePicker
                            show-clear
                            icon-display="input"
                            v-model="saleForm.required_date"
                            date-format="dd-mm-yy"
                            update-model-type="date"
                        >
                        </DatePicker>
                        <label>{{ t('required_date') }}</label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
                    <FloatLabel variant="on">
                        <DatePicker
                            show-clear
                            icon-display="input"
                            v-model="saleForm.shipped_date"
                            date-format="dd-mm-yy"
                            update-model-type="date"
                        >
                        </DatePicker>
                        <label>{{ t('shipped_date') }}</label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon><Button icon="pi pi-info-circle" variant="link" /></InputGroupAddon>
                    <FloatLabel variant="on">
                        <Select
                            v-model="saleForm.status"
                            :options="statusOptions"
                            option-label="label"
                            option-value="value"
                        />
                        <label>{{ t('status') }}</label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon><Button icon="pi pi-pencil" variant="link" /></InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea v-model="saleForm.notes" class="w-full" rows="3" />
                        <label>{{ t('notes') }}</label>
                    </FloatLabel>
                </InputGroup>
            </template>
            <template #footer>
                <Button icon="pi pi-check" :loading="btnLoading" size="small" :label="t('btnSave')" @click="editMode ? update() : create()" />
                <Button icon="pi pi-times" :label="t('btnCancel')" size="small" @click="close" />
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({ layout: 'dashboard' })

    import {
        applySaleValidationErrors,
        createEmptySaleForm,
        createSaleErrors,
        createSaleFilters,
        type SaleErrors,
        type SaleForm
    } from '~/services/sale.service'
    import { formatDate, parseDate } from '~/utils/dateFormat'
    const { t } = useI18n()
    const orderAction = useOrder()
    const { confirmDelete } = useConfirmDelete()
    const customerOptions = ref<any[]>([])
    const statusOptions = ref([
        { label: t('pending'), value: 'pending' },
        { label: t('comfirmed'), value: 'confirmed' },
        { label: t('shipped'), value: 'shipped' },
        { label: t('delivered'), value: 'delivered' },
        { label: t('cancelled'), value: 'cancelled' },
    ])
    const messageBox = MessageBox()
    const saleList = ref<any[]>([])
    const loading = ref(false)
    const btnLoading = ref(false)
    const openDialog = ref(false)
    const editMode = ref(false)
    const filters = ref()
    const selectSales = ref<any[]>([])
    const errors = ref<SaleErrors>(createSaleErrors())
    const saleForm = ref<SaleForm>(createEmptySaleForm())

    const initFilters = () => {
        filters.value = createSaleFilters()
    }
    initFilters()

    const clearFilter = () => initFilters()

    const openCreateDialog = async () => {
        editMode.value = false
        errors.value = createSaleErrors()
        saleForm.value = createEmptySaleForm()

        try {
            const result = await orderAction.nextNumber()
            saleForm.value.order_number = result.order_number
        } catch (error) {
            saleForm.value.order_number = 'ORD-001'
        }

        openDialog.value = true
    }

    const close = () => {
        openDialog.value = false
        editMode.value = false
        btnLoading.value = false
        loading.value = false
        errors.value = createSaleErrors()
        saleForm.value = createEmptySaleForm()
    }

    const openEditDialog = (event: any) => {
        const item = event.data
        editMode.value = true
        saleForm.value = {
            id: item.id,
            order_number: item.order_number ?? '',
            customer_id: item.customer_id ?? null,
            order_date: item.order_date ? parseDate(item.order_date) : new Date(),
            required_date: item.required_date ? parseDate(item.required_date) : null,
            shipped_date: item.shipped_date ? parseDate(item.shipped_date) : null,
            status: item.status ?? 'pending',
            notes: item.notes ?? ''
        }
        openDialog.value = true
    }

    const getStatusSeverity = (status: string) => {
        switch(status) {
            case 'delivered':
                return 'success';
            case 'shipped':
                return 'info';
            case 'confirmed':
                return 'warning';
            case 'pending':
                return 'secondary';
            case 'cancelled':
                return 'danger';
            default:
                return 'secondary';
        }
    };
    const makeSalePayload = (form: SaleForm) => ({
        ...form,
        order_date: form.order_date ? form.order_date.toISOString() : null,
        required_date: form.required_date ? form.required_date.toISOString() : null,
        shipped_date: form.shipped_date ? form.shipped_date.toISOString() : null,
    })

    const successMessage = () => messageBox.success(t('successMessage'))

    const getLookupOptions = async () => {
        try {
            const customers = await $fetch<any[]>('/api/customer')
            customerOptions.value = Array.isArray(customers) ? customers : []
        } catch (error) {
            customerOptions.value = []
        }
    }

    const getSaleList = async () => {
        loading.value = true
        try {
            saleList.value = await orderAction.list()
        } finally {
            loading.value = false
        }
    }

    const create = async () => {
        btnLoading.value = true
        try {
            await orderAction.create(makeSalePayload(saleForm.value))
            successMessage()
            await getSaleList()
            close()
        } catch (error: any) {
            errors.value = applySaleValidationErrors(error?.data?.data?.detail, errors.value)
        } finally {
            btnLoading.value = false
        }
    }

    const update = async () => {
        btnLoading.value = true
        try {
            await orderAction.update(saleForm.value.id as number, makeSalePayload(saleForm.value))
            successMessage()
            await getSaleList()
            close()
        } catch (error: any) {
            errors.value = applySaleValidationErrors(error?.data?.data?.detail, errors.value)
        } finally {
            btnLoading.value = false
        }
    }

    const deleteMany = () => {
        if (!selectSales.value.length) return
        confirmDelete(async () => {
            try {
                const ids = selectSales.value.map((item: any) => item.id)
                await orderAction.remove(ids)
                await getSaleList()
                successMessage()
            } finally {
                selectSales.value = []
            }
        })
    }

    onMounted(() => {
        getLookupOptions()
        getSaleList()
    })
</script>