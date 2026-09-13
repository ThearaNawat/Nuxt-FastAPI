<template>
  <div id="accounting">
    <DataTable
      paginator
      :rows="pagination.limit"
      @page="onPageChange"
      :rowsPerPageOptions="[5, 10, 20, 50, 100]"
      :value="invoiceList"
      :loading="loading"
      v-model:filters="filters"
      v-model:selection="selectedInvoices"
      :global-filter-fields="['invoice_number', 'customer.customer_name', 'order.order_number', 'status']"
      filter-display="menu"
      data-key="id"
      @row-dblclick="openEditDialog"
      row-hover
      scrollable
      scroll-height="500px"
      size="small"
    >
      <Toolbar>
        <template #end>
          <Button :label="t('btnCreate')" icon="pi pi-plus" @click="openCreateDialog" />
          <Button :label="t('btnDelete')" icon="pi pi-trash" class="ml-2" @click="deleteMany" />
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

      <Column :header="t('invoice_number')" field="invoice_number" sortable />
      <Column :header="t('customer')" field="customer.customer_name" sortable>
        <template #body="{ data }">
          {{ getCustomerName(data.customer) }}
        </template>
      </Column>
      <Column :header="t('order_number')" field="order.order_number" sortable>
        <template #body="{ data }">
          {{ data.order?.order_number || '-' }}
        </template>
      </Column>
      <Column :header="t('invoice_date')" field="invoice_date" sortable>
        <template #body="{ data }">
          <span>{{ formatDate(data.invoice_date) }}</span>
        </template>
      </Column>
      <Column :header="t('due_date')" field="due_date" sortable>
        <template #body="{ data }">
          <span>{{ formatDate(data.due_date) || '-' }}</span>
        </template>
      </Column>
      <Column :header="t('amount')" field="amount" sortable>
        <template #body="{ data }">
          {{ data.amount.toFixed(2) }}
        </template>
      </Column>
      <Column :header="t('paid_amount')" field="paid_amount" sortable>
        <template #body="{ data }">
          {{ data.paid_amount.toFixed(2) }}
        </template>
      </Column>
      <Column :header="t('status')" field="status" sortable>
        <template #body="{ data }">
          <Tag :value="t(data.status)" :severity="getStatusSeverity(data.status)" />
        </template>
      </Column>
      <Column body-class="text-center" :style="{ width: '90px' }">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" text size="small" @click="openEditDialog({ data })" />
        </template>
      </Column>
      <template #empty>{{ t('empty') }}</template>
    </DataTable>

    <Dialog :visible="openDialog" :closable="false" style="width: 680px">
      <template #header>
        <Divider>
          <Button variant="link" icon="pi pi-building-columns" size="large" />
          <span class="text-xl">
            {{ editMode ? t('lblHeaderUpdate').replace('[0]', t('accounting')) : t('lblHeaderCreate').replace('[0]', t('accounting')) }}
          </span>
        </Divider>
      </template>
      <template #default>
        <div class="grid gap-2 sm:grid-cols-2">
          <div>
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-hashtag" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <InputText v-model="invoiceForm.invoice_number" :invalid="Boolean(errors.invoice_number)" />
                <label>{{ t('invoice_number') }} *</label>
              </FloatLabel>
            </InputGroup>
            <Message v-if="errors.invoice_number" severity="error" size="small" variant="simple">{{ errors.invoice_number }}</Message>
          </div>

          <div>
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-user" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <Select
                  v-model="invoiceForm.customer_id"
                  :options="customerOptions"
                  option-label="customer_name"
                  option-value="id"
                  show-clear
                  :invalid="Boolean(errors.customer_id)"
                />
                <label>{{ t('customer') }} *</label>
              </FloatLabel>
            </InputGroup>
            <Message v-if="errors.customer_id" severity="error" size="small" variant="simple">{{ errors.customer_id }}</Message>
          </div>

          <InputGroup class="mt-2">
            <InputGroupAddon><Button icon="pi pi-shopping-cart" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <Select
                v-model="invoiceForm.order_id"
                :options="orderOptions"
                option-label="order_number"
                option-value="id"
                show-clear
              />
              <label>{{ t('order_number') }}</label>
            </FloatLabel>
          </InputGroup>

          <InputGroup class="mt-2">
            <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <DatePicker
                show-clear
                icon-display="input"
                v-model="invoiceForm.invoice_date"
                date-format="dd-mm-yy"
                update-model-type="date"
              />
              <label>{{ t('invoice_date') }}</label>
            </FloatLabel>
          </InputGroup>

          <InputGroup class="mt-2">
            <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <DatePicker
                show-clear
                icon-display="input"
                v-model="invoiceForm.due_date"
                date-format="dd-mm-yy"
                update-model-type="date"
              />
              <label>{{ t('due_date') }}</label>
            </FloatLabel>
          </InputGroup>

          <InputGroup class="mt-2">
            <InputGroupAddon><Button icon="pi pi-dollar" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <InputNumber v-model="invoiceForm.amount" :min="0" class="w-full" />
              <label>{{ t('amount') }}</label>
            </FloatLabel>
          </InputGroup>

          <InputGroup class="mt-2">
            <InputGroupAddon><Button icon="pi pi-money-bill" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <InputNumber v-model="invoiceForm.paid_amount" :min="0" class="w-full" />
              <label>{{ t('paid_amount') }}</label>
            </FloatLabel>
          </InputGroup>

          <InputGroup class="mt-2 sm:col-span-2">
            <InputGroupAddon><Button icon="pi pi-info-circle" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <Select
                v-model="invoiceForm.status"
                :options="statusOptions"
                option-label="label"
                option-value="value"
              />
              <label>{{ t('status') }}</label>
            </FloatLabel>
          </InputGroup>
        </div>
      </template>
      <template #footer>
        <Button
          icon="pi pi-check"
          :loading="btnLoading"
          size="small"
          :label="t('btnSave')"
          @click="editMode ? update() : create()"
        />
        <Button icon="pi pi-times" :label="t('btnCancel')" size="small" @click="close" />
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

import { createEmptyInvoiceForm, createInvoiceErrors, type InvoiceErrors, type InvoiceForm } from '~~/shared/types/invoice'
import { createInvoiceFilters, InvoiceService } from '~/services/invoice.service'
import { formatDate, parseDate } from '~/utils/dateFormat'
import { useInvoice } from '~/composables/useInvoice'
import type { Invoice } from '~~/shared/types/invoice'

const { t } = useI18n()
const invoiceAction = useInvoice()
const { confirmDelete } = useConfirmDelete()
const messageBox = MessageBox()
const customerOptions = ref<any[]>([])
const orderOptions = ref<any[]>([])
const statusOptions = ref([
  { label: t('draft'), value: 'draft' },
  { label: t('issued'), value: 'issued' },
  { label: t('partially_paid'), value: 'partially_paid' },
  { label: t('paid'), value: 'paid' },
  { label: t('overdue'), value: 'overdue' },
  { label: t('cancelled'), value: 'cancelled' },
])
const pagination = ref({
        page: 1,
        limit: 10,
        total: 0
})
const invoiceList = ref<Invoice[]>([])
const loading = ref(false)
const btnLoading = ref(false)
const openDialog = ref(false)
const editMode = ref(false)
const filters = ref()
const selectedInvoices = ref<any[]>([])
const errors = ref<InvoiceErrors>(createInvoiceErrors())
const invoiceForm = ref<InvoiceForm>(createEmptyInvoiceForm())

const onPageChange = (event: any) => {
        pagination.value.page = event.page + 1
        pagination.value.limit = event.rows
        getInvoiceList()
    }
const initFilters = () => {
  filters.value = createInvoiceFilters()
}
initFilters()

const clearFilter = () => {
  pagination.value.page = 1
  initFilters()
  getInvoiceList()
}

const fetchCustomerOptions = async () => {
  try {
    const customers = await $fetch<any[]>('/api/customer')
    customerOptions.value = Array.isArray(customers) ? customers : []
  } catch {
    customerOptions.value = []
  }
}

const fetchOrderOptions = async () => {
  try {
    const orders = await $fetch<any[]>('/api/order')
    orderOptions.value = Array.isArray(orders) ? orders : []
  } catch {
    orderOptions.value = []
  }
}

const getInvoiceList = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
        page: pagination.value.page.toString(),
        limit: pagination.value.limit.toString()
    })
    const response = await invoiceAction.list(params)
    invoiceList.value = response?.data
    pagination.value.total = response?.pagination?.total_records || 0
  } finally {
    loading.value = false
  }
}

const validateInvoiceForm = () => {
  const nextErrors = createInvoiceErrors()
  if (!invoiceForm.value.invoice_number) nextErrors.invoice_number = 'Invoice number is required.'
  if (!invoiceForm.value.customer_id) nextErrors.customer_id = 'Customer is required.'
  if (invoiceForm.value.amount <= 0) nextErrors.amount = 'Amount must be greater than zero.'
  return nextErrors
}

const openCreateDialog = () => {
  editMode.value = false
  errors.value = createInvoiceErrors()
  invoiceForm.value = createEmptyInvoiceForm()
  openDialog.value = true
}

const openEditDialog = (event: any) => {
  const item = event.data
  editMode.value = true
  errors.value = createInvoiceErrors()
  invoiceForm.value = {
    id: item.id,
    invoice_number: item.invoice_number,
    order_id: item.order_id ?? null,
    customer_id: item.customer_id,
    invoice_date: item.invoice_date ? parseDate(item.invoice_date) : new Date(),
    due_date: item.due_date ? parseDate(item.due_date) : null,
    amount: Number(item.amount ?? 0),
    paid_amount: Number(item.paid_amount ?? 0),
    status: item.status ?? 'draft',
  }
  openDialog.value = true
}

const close = () => {
  openDialog.value = false
  editMode.value = false
  btnLoading.value = false
  loading.value = false
  errors.value = createInvoiceErrors()
  invoiceForm.value = createEmptyInvoiceForm()
}

const getCustomerName = (customer: any) => customer?.customer_name || '-'

const getStatusSeverity = (status: string) => {
  if (status === 'paid') return 'success'
  if (status === 'overdue') return 'danger'
  if (status === 'partially_paid') return 'warning'
  if (status === 'cancelled') return 'danger'
  if (status === 'issued') return 'info'
  return 'secondary'
}

const create = async () => {
  btnLoading.value = true
  const nextErrors = validateInvoiceForm()
  if (nextErrors.invoice_number || nextErrors.customer_id || nextErrors.amount) {
    errors.value = nextErrors
    btnLoading.value = false
    return
  }

  try {
    await invoiceAction.create(invoiceForm.value)
    messageBox.success(t('successMessage'))
    await getInvoiceList()
    close()
  } catch (error: any) {
    errors.value = InvoiceService.applyInvoiceValidationErrors(error?.data?.data?.detail, errors.value)
  } finally {
    btnLoading.value = false
  }
}

const update = async () => {
  btnLoading.value = true
  const nextErrors = validateInvoiceForm()
  if (nextErrors.invoice_number || nextErrors.customer_id || nextErrors.amount) {
    errors.value = nextErrors
    btnLoading.value = false
    return
  }

  try {
    await invoiceAction.update(invoiceForm.value.id as number, invoiceForm.value)
    messageBox.success(t('successMessage'))
    await getInvoiceList()
    close()
  } catch (error: any) {
    errors.value = InvoiceService.applyInvoiceValidationErrors(error?.data?.data?.detail, errors.value)
  } finally {
    btnLoading.value = false
  }
}

const deleteMany = () => {
  if (!selectedInvoices.value.length) return
  confirmDelete(async () => {
    try {
      const ids = selectedInvoices.value.map((item: any) => item.id)
      await invoiceAction.remove(ids)
      await getInvoiceList()
      messageBox.success(t('successMessage'))
    } finally {
      selectedInvoices.value = []
    }
  })
}

onMounted(() => {
  fetchCustomerOptions()
  fetchOrderOptions()
  getInvoiceList()
})
</script>
