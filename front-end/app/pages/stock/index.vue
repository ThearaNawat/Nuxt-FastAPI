<template>
  <div id="stock-transaction">
    <Tabs value="0">
          <TabList>
            <TabList>
              <Tab value="0">
                {{t('stock')}}
              </Tab>
              <Tab value="1">
                {{t('stock_transaction')}}
              </Tab>
            </TabList>
          </TabList>
          <TabPanels>
          <TabPanel value="0">
            <DataTable
              v-model:filters="filters"
              v-model:selection="selectStock"
              paginator
              :rows="pagination.limit"
              :total-records="pagination.total"
              :rows-per-page-options="[5, 10, 20, 50, 100]"
              :value="stockList"
              :loading="loading"
              :select-all="selectAll"
              :global-filter-fields="[
                'product.code',
                'product.name',
                'warehouse.warehouse_name',
                'measurement.code',
                'transaction_type',
                'reference_number',
                'reason'
              ]"
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
              @select-all-change="onSelectAllChange"
              @page="onPageChange"
              @row-dblclick="openEditDialog"
            >
              
              <Toolbar >
                <template #start>
                  
                </template>
                <template #end>
                  <Button :label="t('btnCreate')" icon="pi pi-plus" @click="openCreateDialog" />
                  <Button :label="t('btnDelete')" icon="pi pi-trash" class="ml-2" @click="deleteMany" />
                </template>
              </Toolbar>
              <template #header>
                <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                  <IconField class="w-full md:max-w-md">
                    <InputIcon>
                      <i class="pi pi-search" />
                    </InputIcon>
                    <InputText size="small" v-model="filters['global'].value" class="w-full" :placeholder="t('search')" />
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

              <Column :header="t('available')" sortable style="min-width: 180px">
                <template #body="{ data }">
                  <Tag
                    :value="getAviableStock(data.current_quantity, data.reserved_quantity)"
                    icon="pi pi-spin pi-box"
                  >
                    <template v-if="getAviableStock(data.current_quantity, data.reserved_quantity) && data.measurement" #default>
                      {{`${getAviableStock(data.current_quantity, data.reserved_quantity)} ${data.measurement.code}`}}</template>
                    <template v-else #default>{{ 0 }}</template>
                  </Tag>
                </template>
              </Column>
              <Column :header="t('reservedQuantity')"  sortable style="min-width: 180px">
                <template #body="{ data }">
                  <Tag :value="data.reserved_quantity" severity="info" icon="pi pi-box" :rounded="true">
                    <template v-if="data.reserved_quantity && data.measurement_reserved" #default>{{`${data.reserved_quantity} ${data.measurement_reserved.code}`}}</template>
                    <template v-else #default>{{ 0 }}</template>
                  </Tag>
                </template>
              </Column>
              
              <Column :header="t('quantity')" field="quantity" sortable style="min-width: 130px">
                <template #body="{ data }">
                  <Tag :value="data.current_quantity" severity="success" icon="pi pi-box" :rounded="true">
                    <template v-if="data.current_quantity && data.measurement" #default>{{`${data.current_quantity} ${data.measurement.code}`}}</template>
                    <template v-else #default>{{ 0 }}</template>
                  </Tag>
                </template>
              </Column>

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

              <Dialog
                :visible="openDialog"
                :closable="false"
                modal
                style="width: min(860px, 96vw)"
              >
                <template #header>
                  <Divider>
                    <Button icon="pi pi-arrows-h" variant="link" style="font-size: 1.7rem;" />
                    <span v-if="!editMode" class="ml-2 text-xl">
                      {{ t('lblHeaderCreate').replace('[0]', t('stock_transaction')) }}
                    </span>
                    <span v-else class="ml-2 text-xl">
                      {{ t('lblHeaderUpdate').replace('[0]', t('stock_transaction')) }}
                    </span>
                  </Divider>
                </template>

                <template #default>
                  <div class="">
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                          <Button icon="pi pi-box" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                          <Select
                            v-model="stockForm.product_id"
                            :options="productOptions"
                            option-value="id"
                            option-label="name"
                            show-clear
                            :virtual-scroller-options="{ itemSize: 38, }"
                            :invalid="Boolean(errors.product_id)"
                          >
                            

                            <template #option="{ option }">
                              <div class="flex items-center">
                                <span class="font-medium">{{ option.code }} - {{ option.name }}</span>
                              </div>
                            </template>
                          </Select>
                          <label>{{ t('product') }} *</label>
                        </FloatLabel>
                      </InputGroup>
                      <Message v-if="errors.product_id" severity="error" size="small" variant="simple">
                        {{ errors.product_id }}
                      </Message>
                      <InputGroup class="mt-2">
                        <InputGroupAddon>
                          <Button icon="pi pi-warehouse" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                          <Select
                            v-model="stockForm.warehouse_id"
                            :options="warehouseOptions"
                            option-label="warehouse_name"
                            option-value="id"
                            show-clear
                            :invalid="Boolean(errors.warehouse_id)"
                          />
                          <label>{{ t('warehouse') }} *</label>
                        </FloatLabel>
                      </InputGroup>
                      <Message v-if="errors.warehouse_id" severity="error" size="small" variant="simple">
                        {{ errors.warehouse_id }}
                      </Message>

                    <Divider align="left">
                      <span class="text-xs font-semibold uppercase text-slate-500">
                        {{ t('currentQuantity') }}
                      </span>
                    </Divider>

                    <div class="flex items-center gap-2">
                      <div class="w-full">
                        <InputGroup>
                          <InputGroupAddon>
                            <Button icon="pi pi-hashtag" variant="link" />
                          </InputGroupAddon>
                          <FloatLabel variant="on">
                            <InputNumber v-model="stockForm.quantity" :invalid="Boolean(errors.quantity)" />
                            <label>{{ t('currentQuantity') }} *</label>
                          </FloatLabel>
                        </InputGroup>
                        <Message v-if="errors.quantity" severity="error" size="small" variant="simple">
                          {{ errors.quantity }}
                        </Message>
                      </div>
                      <div class="w-full">
                        <InputGroup>
                          <InputGroupAddon>
                            <Button icon="pi pi-hammer" variant="link" />
                          </InputGroupAddon>
                          <FloatLabel variant="on">
                            <Select
                              v-model="stockForm.measurement_id"
                              :options="measurementOptions"
                              option-label="code"
                              option-value="id"
                              show-clear
                              :invalid="Boolean(errors.measurement_id)"
                            >
                              <template #option="{ option }">
                                <div class="flex items-center">
                                  <span class="font-medium mr-2">{{ option.code }}</span>
                                  <span class="text-xs text-slate-500">{{ option.name }}</span>
                                </div>
                              </template>
                            </Select>
                            <label>{{ t('measurement') }}*</label>
                          </FloatLabel>
                        </InputGroup>
                        
                        <Message v-if="errors.measurement_id" severity="error" size="small" variant="simple">
                          {{ errors.measurement_id }}
                        </Message>
                      </div>
                      
                    </div>
                    <Divider align="left">
                      <span class="text-xs font-semibold uppercase text-slate-500">
                        {{ t('reservedQuantity') }}
                      </span>
                    </Divider>

                    <div class="flex items-center gap-2">
                      <InputGroup>
                        <InputGroupAddon>
                          <Button icon="pi pi-calculator" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                          <InputNumber v-model="stockForm.reserved_qty" />
                          <label>{{ t('reservedQuantity') }}</label>
                        </FloatLabel>
                      </InputGroup>
                      <InputGroup>
                        <InputGroupAddon>
                          <Button icon="pi pi-hammer" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                          <Select
                            v-model="stockForm.measurement_reserved_id"
                            :options="measurementOptions"
                            option-label="code"
                            option-value="id"
                            show-clear
                          >
                            <template #option="{ option }">
                              <div class="flex items-center">
                                <span class="font-medium mr-2">{{ option.code }}</span>
                                <span class="text-xs text-slate-500">{{ option.name }}</span>
                              </div>
                            </template>
                          </Select>
                          <label>{{ t('measurement') }}</label>
                        </FloatLabel>
                      </InputGroup>
                    </div>
                    <!-- <InputGroup class="mt-2">
                        <InputGroupAddon>
                          <Button icon="pi pi-hashtag" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                          <InputText v-model="stockForm.reference_number" />
                          <label>{{ t('reference_number') }}</label>
                        </FloatLabel>
                      </InputGroup>
                    <InputGroup class="md:col-span-2 mt-2">
                      <InputGroupAddon>
                        <Button icon="pi pi-comment" variant="link" />
                      </InputGroupAddon>
                      <FloatLabel variant="on">
                        <Textarea v-model="stockForm.reason" rows="4" class="w-full" />
                        <label>{{ t('remark') }}</label>
                      </FloatLabel>
                    </InputGroup> -->
                  </div>
                </template>

                <template #footer>
                  <Button
                    icon="pi pi-check"
                    :loading="btnLoading"
                    size="small"
                    :label="t('btnSave')"
                    class="mt-3"
                    @click="editMode ? update() : create()"
                  />
                  <Button 
                    icon="pi pi-times" 
                    :label="t('btnCancel')" 
                    size="small" 
                    @click="close"
                    class="mt-3"
                  />
                </template>
              </Dialog>
          </TabPanel>
          <TabPanel value="1">
              <StockBalance 
                :measurement-options="measurementOptions"
                :product-options="productOptions"
                :warehouse-options="warehouseOptions"
              />
          </TabPanel>
        </TabPanels>
    </Tabs>
    
  </div>
</template>

<script setup lang="ts">
import type { Measurement } from '~~/shared/types/measurement'
import type { StockItem } from '~/composables/useStock'
import type { product } from '~/composables/useProduct'
import type { Warehouse } from '~~/shared/types/warehouse'
import StockIn from '~/components/stock/StockIn.vue'
import StockOut from '~/components/stock/StockOut.vue'
import StockBalance from '~/components/stock/StockBalance.vue'
import {
  applyStockValidationErrors,
  createEmptyStockForm,
  createStockErrors,
  createStockFilters,
  type StockErrors,
  type StockForm
} from '~/services/stock.service'
import { formatDate } from '~/utils/dateFormat'

definePageMeta({ layout: 'dashboard' })

type ProductLookup = {
  id: number
  code: string
  name: string
  package?: string | null
  measurement_id?: number | null
  measurement_code?: string | null
}

type WarehouseLookup = {
  id: number
  warehouse_name: string
}

type DataTablePageEvent = {
  page: number
  rows: number
}

type StockRowEvent = {
  data: StockItem
}

const { t } = useI18n()
const stockAction = useStock()
const productAction = useProduct()
const warehouseAction = useWarehouse()
const { getAll: getMeasurements } = useMeasurement()
const messageBox = MessageBox()
const { confirmDelete } = useConfirmDelete()

const stockList = ref<StockItem[]>([])
const productOptions = ref<product[]>([])
const warehouseOptions = ref<Warehouse[]>([])
const measurementOptions = ref<Measurement[]>([])
const selectStock = ref<StockItem[]>([])
const loading = ref(false)
const btnLoading = ref(false)
const openDialog = ref(false)
const editMode = ref(false)
const selectAll = ref(false)
const filters = ref(createStockFilters())
const errors = ref<StockErrors>(createStockErrors())
const stockForm = ref<StockForm>(createEmptyStockForm())
const pagination = ref({
  page: 1,
  limit: 10,
  total: 0
})




const getAviableStock = (currentQty: number, resQty: number) => currentQty - resQty


const resetForm = () => {
  errors.value = createStockErrors()
  stockForm.value = createEmptyStockForm()
}

const openCreateDialog = () => {
  resetForm()
  editMode.value = false
  openDialog.value = true
}

const close = () => {
  openDialog.value = false
  editMode.value = false
  btnLoading.value = false
  resetForm()
}

const onSelectAllChange = (event: { checked: boolean }) => {
  selectAll.value = event.checked
  selectStock.value = event.checked ? [...stockList.value] : []
}

const onPageChange = (event: DataTablePageEvent) => {
  pagination.value.page = event.page + 1
  pagination.value.limit = event.rows
  selectStock.value = []
  selectAll.value = false
  getStockList()
}

const clearFilter = () => {
  filters.value = createStockFilters()
  pagination.value.page = 1
  selectStock.value = []
  selectAll.value = false
  getStockList()
}

const openEditDialog = (event: StockRowEvent) => {
  
  const item = event.data
  
  resetForm()
  editMode.value = true
  stockForm.value = {
    id: item.id,
    product_id: item.product_id ?? null,
    warehouse_id: item.warehouse_id ?? null,
    measurement_id: item.measurement_id ?? item.product?.measurement_id ?? null,
    transaction_type: item.transaction_type ?? null,
    quantity: item.current_quantity ?? 0,
    reason: item.reason ?? '',
    reference_number: item.reference_number ?? null,
    measurement_reserved_id: item.measurement_reserved_id ?? null,
    reserved_qty: item.reserved_quantity ?? 0
  }
  openDialog.value = true
}

const successMessage = () => messageBox.success(t('successMessage'))
const warningMessage = () => messageBox.warning(t('warningMessage'))
const errorMessage = () => messageBox.error(t('errorMessage'))
const loadLookupOptions = async () => {
  const [productsResult, measurementsResult] = await Promise.allSettled([
    productAction.getAllProduct(),
    getMeasurements(),
  ])
  await warehouseAction.getAll()
  productOptions.value = productsResult.status === 'fulfilled' && Array.isArray(productsResult.value)
    ? productsResult.value
    : []

  warehouseOptions.value = warehouseAction.warehouses.value

  measurementOptions.value = measurementsResult.status === 'fulfilled' && Array.isArray(measurementsResult.value)
    ? measurementsResult.value
    : []
}

const getStockList = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: pagination.value.page.toString(),
      limit: pagination.value.limit.toString(),
    })
    const response = await stockAction.list(params.toString())
    stockList.value = Array.isArray(response.data) ? response.data : []
    pagination.value.total = response.pagination?.total_records ?? 0
  } catch(error) {
    stockList.value = []
    pagination.value.total = 0

  } finally {
    loading.value = false
  }
}

const create = async () => {
  btnLoading.value = true
  errors.value = createStockErrors()
  
  try {
    if (stockForm.value.reserved_qty == null || stockForm.value.reserved_qty === undefined) {
      stockForm.value.reserved_qty = 0
      stockForm.value.measurement_reserved_id = null
    }
    if(
      (stockForm.value.reserved_qty > 0 && stockForm.value.measurement_reserved_id == null) || 
      (stockForm.value.reserved_qty <= 0 && stockForm.value.measurement_reserved_id != null)
    ) {
      return warningMessage()
    }
    await stockAction.create(stockForm.value)
    successMessage()
    await getStockList()
    close()
  } catch (error) {
    const apiError = error as { data?: { data?: { detail?: unknown } } }
    errors.value = applyStockValidationErrors(apiError?.data?.data?.detail, errors.value)
    if(!errors.value) errorMessage()
  } finally {
    btnLoading.value = false
  }
}

const update = async () => {
  btnLoading.value = true
  errors.value = createStockErrors()
  
  if (stockForm.value.reserved_qty == null || stockForm.value.reserved_qty === undefined) {
    stockForm.value.reserved_qty = 0
    stockForm.value.measurement_reserved_id = null
  }
  try {
    if(
      (stockForm.value.reserved_qty > 0 && stockForm.value.measurement_reserved_id == null) || 
      (stockForm.value.reserved_qty <= 0 && stockForm.value.measurement_reserved_id != null)
    ) {
      return warningMessage()
    }
    await stockAction.update(stockForm.value.id as number, stockForm.value)
    successMessage()
    await getStockList()
    close()
  } catch (error) {
    const apiError = error as { data?: { data?: { detail?: unknown } } }
    errors.value = applyStockValidationErrors(apiError?.data?.data?.detail, errors.value)
    if(!errors.value) errorMessage()
  } finally {
    btnLoading.value = false
  }
}

const deleteMany = () => {
  if (!selectStock.value.length) return warningMessage()

  confirmDelete(async () => {
    loading.value = true
    try {
      await stockAction.remove(selectStock.value.map((item) => item.id))
      successMessage()
      await getStockList()
      selectAll.value = false
    } finally {
      selectStock.value = []
      loading.value = false
    }
  })
}

onMounted(async () => {
  await Promise.all([loadLookupOptions(), getStockList()])
})
</script>
