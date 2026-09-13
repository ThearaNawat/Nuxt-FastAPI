<template>
  <div id="purchase">
    <DataTable
      v-model:filters="filters"
      v-model:selection="selectPurchases"
      paginator
      :rows="10"
      :rows-per-page-options="[5, 10, 20, 50, 100]"
      :value="purchaseList"
      :loading="loading"
      :global-filter-fields="['order_number', 'supplier.name', 'status', 'payment_status', 'notes']"
      filter-display="menu"
      data-key="id"
      size="small"
      striped-rows
      row-hover
      scrollable
      scroll-height="500px"
      @row-dblclick="openEditDialog"
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
            <InputText v-model="filters['global'].value" placeholder="Search" />
          </IconField>
          <Button icon="pi pi-filter-slash" variant="link" @click="clearFilter" />
        </div>
      </template>

      <Column selection-mode="multiple" header-style="width: 2rem" />
      <Column header="Order Number" field="order_number" sortable />
      <Column header="Supplier" field="supplier_id" sortable>
        <template #body="{ data }">
          {{ formatSupplierLabelById(data.supplier ?? data.supplier_id) }}
        </template>
      </Column>
      <Column header="Status" field="status" sortable>
        <template #body="{ data }">
          <Tag :value="getStatusLabel(data.status)" :severity="getStatusSeverity(data.status)" />
        </template>
      </Column>
      <Column header="Payment Status" field="payment_status" sortable>
        <template #body="{ data }">
          <Tag
            :value="getPaymentStatusLabel(data.payment_status)"
            :severity="getPaymentStatusSeverity(data.payment_status)"
          />
        </template>
      </Column>
      <Column header="Order Date" field="order_date" sortable>
        <template #body="{ data }">
          {{ formatDate(data.order_date) }}
        </template>
      </Column>
      <Column header="Required Date" field="required_date" sortable>
        <template #body="{ data }">
          {{ formatDate(data.required_date) }}
        </template>
      </Column>
      <Column header="Received Date" field="received_date" sortable>
        <template #body="{ data }">
          {{ formatDate(data.received_date) }}
        </template>
      </Column>
      <Column header="Actions" body-class="text-center" :style="{ width: '90px' }">
        <template #body="{ data }">
          <div class="flex items-center justify-center gap-1">
            <Button icon="pi pi-eye" text size="small" @click="openViewDialog({ data })" />
            <Button icon="pi pi-pencil" text size="small" @click="openEditDialog({ data })" />
            <Button icon="pi pi-trash" text size="small" severity="danger" @click="deleteOne(data)" />
          </div>
        </template>
      </Column>
      <template #empty>No purchase orders found.</template>
    </DataTable>

    <Dialog :visible="openDialog" :closable="false" style="width: 90vw; max-width: 1000px">
      <template #header>
        <span class="text-xl">
          {{ viewMode ? `${t('purchase')} Details` : editMode ? t('lblHeaderUpdate').replace('[0]', t('purchase')) : t('lblHeaderCreate').replace('[0]', t('purchase')) }}
        </span>
      </template>
      <template #default>
        
        <div>
          <div class="grid gap-2 sm:grid-cols-2">
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-hashtag" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <InputText v-model="purchaseForm.order_number" readonly />
                <label>{{ t('order_number') }}</label>
              </FloatLabel>
            </InputGroup>

            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-briefcase" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <Select
                  v-model="purchaseForm.supplier_id"
                  :options="supplierOptions"
                  option-label="name"
                  option-value="id"
                  show-clear
                  :invalid="Boolean(errors.supplier_id)"
                />
                <label>{{ t('supplier') }} *</label>
              </FloatLabel>
            </InputGroup>

            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <DatePicker
                  v-model="purchaseForm.order_date"
                  show-clear
                  icon-display="input"
                  date-format="dd-mm-yy"
                  update-model-type="date"
                />
                <label>{{ t('order_date') }}</label>
              </FloatLabel>
            </InputGroup>

            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <DatePicker
                  v-model="purchaseForm.required_date"
                  show-clear
                  icon-display="input"
                  date-format="dd-mm-yy"
                  update-model-type="date"
                />
                <label>{{ t('required_date') }}</label>
              </FloatLabel>
            </InputGroup>

            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <DatePicker
                  v-model="purchaseForm.received_date"
                  show-clear
                  icon-display="input"
                  date-format="dd-mm-yy"
                  update-model-type="date"
                />
                <label>{{ t('recieve_date') }}</label>
              </FloatLabel>
            </InputGroup>

            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-info-circle" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <Select
                  v-model="purchaseForm.status"
                  :options="statusOptions"
                  option-label="label"
                  option-value="value"
                />
                <label>{{ t('order_status') }}</label>
              </FloatLabel>
            </InputGroup>

            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-credit-card" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <Select
                  v-model="purchaseForm.payment_status"
                  :options="paymentStatusOptions"
                  option-label="label"
                  option-value="value"
                />
                <label>{{ t('payment_status') }}</label>
              </FloatLabel>
            </InputGroup>
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-credit-card" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <InputNumber
                  :format="true"
                  v-model="purchaseForm.tax_amount"
                >
                
                </InputNumber>
                <label>{{ t('tax') }}</label>
              </FloatLabel>
            </InputGroup>
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-credit-card" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <InputNumber
                  :format="true"
                  v-model="purchaseForm.discount_amount"
                >
                
                </InputNumber>
                <label>{{ t('discount') }}</label>
              </FloatLabel>
            </InputGroup>
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-credit-card" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <InputNumber
                  :format="true"
                  v-model="purchaseForm.sub_total"
                >
                
                </InputNumber>
                <label>{{ t('sub_total') }}</label>
              </FloatLabel>
            </InputGroup>
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-credit-card" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <InputNumber
                  :format="true"
                  v-model="purchaseForm.total_amount"
                >
                
                </InputNumber>
                <label>{{ t('total') }}</label>
              </FloatLabel>
            </InputGroup>
            <InputGroup class="mt-2">
              <InputGroupAddon><Button icon="pi pi-credit-card" variant="link" /></InputGroupAddon>
              <FloatLabel variant="on">
                <Select
                  :options="[]"
                  option-label="label"
                  option-value="value"
                />
                <label>{{ t('currentcy') }}</label>
              </FloatLabel>
            </InputGroup>
          </div>

          <InputGroup class="mt-2">
            <InputGroupAddon><Button icon="pi pi-pencil" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <Textarea v-model="purchaseForm.notes" class="w-full" rows="1"/>
              <label>{{ t('notes') }}</label>
            </FloatLabel>
          </InputGroup>

          <div class="mt-4">
            <div class="flex items-center justify-between mb-2">
              <span class="font-semibold">{{ t('purchase_items') }}</span>
              <Button icon="pi pi-plus" size="small" :label="t('add_item')" @click="addPurchaseItem" />
            </div>

            <div class="overflow-auto border rounded-md max-h-[250px]">
              <table class="min-w-full text-sm">
                <thead class="bg-gray-100">
                  <tr>
                    <th class="p-2 text-left">Product</th>
                    <th class="p-2 text-right">Qty</th>
                    <th class="p-2 text-right">Unit Cost</th>
                    <th class="p-2 text-right">Total</th>
                    <th class="p-2 text-center">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in purchaseForm.items" :key="index">
                    <td class="p-2 w-full">
                      <Select
                        v-model="item.product_id"
                        :options="productOptions"
                        option-label="name"
                        option-value="id"
                        filter
                        :virtual-scroller-options="{ itemSize: 38, autoSize: true}"
                        class="w-full"
                        show-clear
                      >
                        <template #option="{ option }">
                          <div class="flex items-center">
                            <span class="font-medium mr-2">{{ option.code }}</span>
                            <span class="text-xs text-slate-500">{{ option.name }}</span>
                          </div>
                        </template>
                      </Select>
                    </td>
                    <td class="p-2">
                      <InputNumber
                        v-model="item.quantity"
                        :min="1"
                        class="w-full"
                        @change="updatePurchaseItemTotal(item)"
                      />
                    </td>
                    <td class="p-2">
                      <InputNumber
                        v-model="item.unit_cost"
                        :min="0"
                        mode="decimal"
                        :show-buttons="false"
                        class="w-full"
                        @change="updatePurchaseItemTotal(item)"
                      />
                    </td>
                    
                    <td class="p-2 text-right">{{ getPurchaseItemTotal(item).toFixed(2) }}</td>
                    <td class="p-2 text-center">
                      <Button icon="pi pi-trash" severity="danger" text size="small" @click="removePurchaseItem(index)" />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <Message v-if="errors.items" severity="error" size="small" class="mt-2">{{ errors.items }}</Message>
            <div class="flex flex-col gap-2 justify-end mt-2 sm:flex-row sm:items-center">
              <div class="text-sm text-slate-600">Line totals update automatically when qty or cost changes.</div>
              <div class="ml-auto font-semibold">Total Purchase: {{ getPurchaseOrderTotal().toFixed(2) }}</div>
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <Button
          v-if="!viewMode"
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
import { computed, onMounted, ref } from 'vue'
import {
  applyPurchaseValidationErrors,
  createEmptyPurchaseForm,
  createEmptyPurchaseItem,
  createPurchaseErrors,
  createPurchaseFilters,
  type PurchaseErrors,
  type PurchaseForm,
  type PurchaseItemForm,
} from '~/services/purchase.service'
import { usePurchase } from '~/composables/usePurchase'
import { formatDate, parseDate } from '~/utils/dateFormat'
import type { PurchaseOrder, PurchaseProduct, PurchaseSupplier } from '~~/shared/types/purchase'

definePageMeta({ layout: 'dashboard' })

type PurchaseOrderItemState = PurchaseItemForm & {
  product?: PurchaseProduct | null
}

type PurchaseFormState = Omit<PurchaseForm, 'items'> & {
  items: PurchaseOrderItemState[]
  supplier?: PurchaseSupplier | null
}

type PurchaseRowEvent = {
  data: PurchaseOrder
}

type ValidationErrorResponse = {
  data?: {
    data?: {
      detail?: unknown
    }
  }
}

const { t } = useI18n()
const purchaseAction = usePurchase()
const { confirmDelete } = useConfirmDelete()
const messageBox = MessageBox()
const supplierOptions = ref<PurchaseSupplier[]>([])
const productOptions = ref<PurchaseProduct[]>([])
const purchaseList = ref<PurchaseOrder[]>([])
const loading = ref(false)
const btnLoading = ref(false)
const openDialog = ref(false)
const editMode = ref(false)
const viewMode = ref(false)
const filters = ref(createPurchaseFilters())
const selectPurchases = ref<PurchaseOrder[]>([])
const errors = ref<PurchaseErrors>(createPurchaseErrors())
const purchaseForm = ref<PurchaseFormState>(createEmptyPurchaseForm() as PurchaseFormState)

const statusOptions = computed(() => [
  { label: t('pending'), value: 'pending' },
  { label: t('confirmed'), value: 'confirmed' },
  { label: t('shipped'), value: 'shipped' },
  { label: t('delivered'), value: 'delivered' },
  { label: t('cancelled'), value: 'cancelled' },
])

const paymentStatusOptions = computed(() => [
  { label: t('pending'), value: 1 },
  { label: t('paid'), value: 2 },
  { label: t('partially_paid'), value: 3 },
  { label: t('overdue'), value: 4 },
])

const clearFilter = () => {
  filters.value = createPurchaseFilters()
  selectPurchases.value = []
}

const fetchSupplierOptions = async () => {
  try {
    const suppliers = await $fetch<PurchaseSupplier[]>('/api/supplier')
    supplierOptions.value = Array.isArray(suppliers) ? suppliers : []
  } catch {
    supplierOptions.value = []
  }
}

const fetchProductOptions = async () => {
  try {
    const products = await $fetch<PurchaseProduct[]>('/api/product')
    productOptions.value = Array.isArray(products) ? products : []
  } catch {
    productOptions.value = []
  }
}

const getPurchaseList = async () => {
  loading.value = true
  try {
    purchaseList.value = await purchaseAction.list()
  } catch {
    purchaseList.value = []
  } finally {
    loading.value = false
  }
}

const loadNextOrderNumber = async () => {
  if (editMode.value) return

  try {
    const result = await purchaseAction.nextNumber()
    purchaseForm.value.order_number = result.order_number
  } catch {
    purchaseForm.value.order_number = 'ORD-001'
  }
}

const getSupplierById = (supplierId: number | null) =>
  supplierOptions.value.find((supplier) => supplier.id === supplierId) ?? null

const formatSupplierLabel = (supplier: PurchaseSupplier | null | undefined) => {
  if (!supplier) return '-'
  return supplier.code ? `${supplier.code} - ${supplier.name}` : supplier.name
}

const formatSupplierLabelById = (supplier: PurchaseSupplier | number | null | undefined) => {
  if (typeof supplier === 'number') {
    const lookup = getSupplierById(supplier)
    return lookup ? formatSupplierLabel(lookup) : String(supplier)
  }

  return formatSupplierLabel(supplier)
}


const formatStatusLabel = (status: string | null | undefined) => {
  if (!status) return '-'
  return statusOptions.value.find((option) => option.value === status)?.label ?? status
}

const getStatusLabel = (status: string | null | undefined) => formatStatusLabel(status)

const getStatusSeverity = (status: string | null | undefined) => {
  switch (status) {
    case 'pending':
      return 'warn'
    case 'confirmed':
      return 'info'
    case 'shipped':
      return 'secondary'
    case 'delivered':
      return 'success'
    case 'cancelled':
      return 'danger'
    default:
      return 'secondary'
  }
}

const getPaymentStatusLabel = (status: number) => {
  if (!status) return '-'
  return paymentStatusOptions.value.find((option) => option.value === status)?.label ?? status
}

const getPaymentStatusSeverity = (status: number) => {
  switch (status) {
    case 1:
      return 'warn'
    case 2:
      return 'success'
    case 3:
      return 'info'
    case 4:
      return 'danger'
    default:
      return 'secondary'
  }
}

const getPurchaseItemTotal = (item: PurchaseItemForm | PurchaseOrderItemState) => {
  const quantity = Number(item.quantity ?? 0)
  const unitCost = Number(item.unit_cost ?? 0)
  return Number((quantity * unitCost).toFixed(2))
}

const updatePurchaseItemTotal = (item: PurchaseOrderItemState) => {
  item.total_cost = getPurchaseItemTotal(item)
}

const normalizePurchaseItems = (items: PurchaseOrder['items']) => {
  if (!Array.isArray(items) || !items.length) {
    return [createEmptyPurchaseItem()] as PurchaseOrderItemState[]
  }

  return items.map((lineItem) => {
    const quantity = Number(lineItem.quantity ?? 1)
    const unitCost = Number(lineItem.unit_cost ?? 0)

    return {
      product_id: lineItem.product_id ?? null,
      quantity,
      unit_cost: unitCost,
      expire_date: lineItem.expire_date ? parseDate(lineItem.expire_date) : null,
      total_cost:
        lineItem.total_cost != null ? Number(lineItem.total_cost) : Number((quantity * unitCost).toFixed(2)),
      product: lineItem.product ?? null,
    }
  }) as PurchaseOrderItemState[]
}

const normalizePurchaseForm = (item: PurchaseOrder): PurchaseFormState => ({
  id: item.id,
  order_number: item.order_number,
  supplier_id: item.supplier_id ?? null,
  order_date: item.order_date ? parseDate(item.order_date) : new Date(),
  required_date: item.required_date ? parseDate(item.required_date) : null,
  received_date: item.received_date ? parseDate(item.received_date) : null,
  status: item.status ?? 'pending',
  payment_status: item.payment_status ?? 1,
  notes: item.notes ?? '',
  items: normalizePurchaseItems(item.items),
  supplier: item.supplier ?? null,
  sub_total: item.sub_total,
  discount_amount: item.discount_amount,
  tax_amount: item.tax_amount,
  total_amount: item.total_amount
})

const validatePurchaseForm = () => {
  const nextErrors = createPurchaseErrors()

  if (!purchaseForm.value.supplier_id) {
    nextErrors.supplier_id = 'Supplier is required.'
  }

  if (!purchaseForm.value.items.length) {
    nextErrors.items = 'Add at least one purchase item.'
  } else if (
    purchaseForm.value.items.some(
      (item) => !item.product_id || item.quantity <= 0 || item.unit_cost < 0,
    )
  ) {
    nextErrors.items = 'Every item requires product, qty, and unit cost.'
  }

  return nextErrors
}

const resetForm = () => {
  errors.value = createPurchaseErrors()
  purchaseForm.value = createEmptyPurchaseForm() as PurchaseFormState
}

const openCreateDialog = async () => {
  editMode.value = false
  viewMode.value = false
  resetForm()
  openDialog.value = true
  await loadNextOrderNumber()
}

const openEditDialog = (event: PurchaseRowEvent) => {
  editMode.value = true
  viewMode.value = false
  errors.value = createPurchaseErrors()
  purchaseForm.value = normalizePurchaseForm(event.data)
  openDialog.value = true
}

const openViewDialog = (event: PurchaseRowEvent) => {
  editMode.value = false
  viewMode.value = true
  errors.value = createPurchaseErrors()
  purchaseForm.value = normalizePurchaseForm(event.data)
  openDialog.value = true
}

const close = () => {
  openDialog.value = false
  editMode.value = false
  viewMode.value = false
  btnLoading.value = false
  errors.value = createPurchaseErrors()
  purchaseForm.value = createEmptyPurchaseForm() as PurchaseFormState
}

const addPurchaseItem = () => {
  purchaseForm.value.items.push(createEmptyPurchaseItem() as PurchaseOrderItemState)
}

const removePurchaseItem = (index: number) => {
  if (purchaseForm.value.items.length > 1) {
    purchaseForm.value.items.splice(index, 1)
  }
}

const getPurchaseOrderTotal = () =>
  purchaseForm.value.items.reduce((sum, item) => sum + getPurchaseItemTotal(item), 0)



const formatDateValue = (value: string | Date | null) => {
  if (!value) return null
  if (value instanceof Date) return value.toISOString()
  return parseDate(value)?.toISOString() ?? null
}

const makePurchasePayload = (form: PurchaseFormState) => ({
  order_number: form.order_number,
  supplier_id: form.supplier_id,
  order_date: formatDateValue(form.order_date),
  required_date: formatDateValue(form.required_date),
  received_date: formatDateValue(form.received_date),
  status: form.status,
  payment_status: form.payment_status,
  notes: form.notes,
  supplier: form.supplier ?? null,
  sub_total: form.sub_total,
  discount_amount: form.discount_amount,
  tax_amount: form.tax_amount,
  total_amount: form.total_amount,
  items: form.items.map((item) => ({
    product_id: item.product_id,
    quantity: item.quantity,
    unit_cost: item.unit_cost,
    expire_date: formatDateValue(item.expire_date),
    total_cost: item.total_cost ?? getPurchaseItemTotal(item),
  })),
})

const applyApiValidationErrors = (error: unknown) => {
  const apiError = error as ValidationErrorResponse
  errors.value = applyPurchaseValidationErrors(apiError?.data?.data?.detail, errors.value)
}

const create = async () => {
  btnLoading.value = true
  const nextErrors = validatePurchaseForm()
  if (nextErrors.supplier_id || nextErrors.items) {
    errors.value = nextErrors
    btnLoading.value = false
    return
  }

  try {
    await purchaseAction.create(makePurchasePayload(purchaseForm.value))
    messageBox.success(t('successMessage'))
    await getPurchaseList()
    close()
  } catch (error) {
    applyApiValidationErrors(error)
  } finally {
    btnLoading.value = false
  }
}

const update = async () => {
  const purchaseId = purchaseForm.value.id
  if (typeof purchaseId !== 'number') return

  btnLoading.value = true
  const nextErrors = validatePurchaseForm()
  if (nextErrors.supplier_id || nextErrors.items) {
    errors.value = nextErrors
    btnLoading.value = false
    return
  }

  try {
    await purchaseAction.update(purchaseId, makePurchasePayload(purchaseForm.value))
    messageBox.success(t('successMessage'))
    await getPurchaseList()
    close()
  } catch (error) {
    applyApiValidationErrors(error)
  } finally {
    btnLoading.value = false
  }
}

const deleteOrders = (ids: number[]) => {
  if (!ids.length) {
    messageBox.warning(t('warningMessage'))
    return
  }

  confirmDelete(async () => {
    loading.value = true
    try {
      await purchaseAction.remove(ids)
      messageBox.success(t('successMessage'))
      await getPurchaseList()
      selectPurchases.value = []
    } finally {
      loading.value = false
    }
  })
}

const deleteMany = () => {
  const ids = selectPurchases.value
    .map((item) => item.id)
    .filter((id): id is number => typeof id === 'number')

  deleteOrders(ids)
}

const deleteOne = (purchaseOrder: PurchaseOrder) => {
  if (typeof purchaseOrder.id !== 'number') {
    messageBox.warning(t('warningMessage'))
    return
  }

  deleteOrders([purchaseOrder.id])
}

onMounted(async () => {
  await Promise.all([fetchSupplierOptions(), fetchProductOptions(), getPurchaseList(), loadNextOrderNumber()])
})
</script>
