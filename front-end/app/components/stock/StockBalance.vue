<template>
    <div id="stock-balance">
        <DataTable
            paginator
            :rows="pagination.limit"
            :total-records="pagination.total"
            v-model:selection="selectStock"
            :rows-per-page-options="[5, 10, 20, 50, 100]"
            :value="data"
            :loading="loading"
            :global-filter-fields="[]"
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
                    <InputText size="small" v-model="filters['global'].value" class="w-full" :placeholder="t('search')" />
                </IconField>
                <Button icon="pi pi-filter-slash" variant="link" @click="clearFilter" />
                </div>
            </template>

            <template #empty>{{ t('empty') }}</template>
            <Column selection-mode="multiple" :exportable="false" header-style="width: 2rem" />
            <Column :header="t('lblCode')" field="product.code" sortable style="min-width: 150px">
                <template #body="{ data }">
                  <span class="font-medium">{{ data.stock_transaction_details[0]?.product?.code ?? '-' }}</span>
                </template>
            </Column>
            <Column :header="t('product')" field="product.name" sortable style="min-width: 240px">
                <template #body="{ data }">
                  <div class="flex flex-col">
                    <span class="font-semibold">{{ data.stock_transaction_details[0]?.product?.name }}</span>
                  </div>
                </template>
            </Column>
            <Column :header="t('package')" sortable style="min-width: 240px">
              <template #body="{ data }">
                <span 
                  v-if="data.stock_transaction_details[0]?.product?.package && data.stock_transaction_details[0]?.product?.measurement"
                >
                {{ `${data.stock_transaction_details[0]?.product?.package} ${data.stock_transaction_details[0]?.product?.measurement?.code}`}}
                </span>
                <span v-else>N/A</span>
              </template>
            </Column>
            <Column :header="t('expire_date')" sortable style="min-width: 160px">
                <template #body="{ data }">
                <span>{{ formatDate(data.stock_transaction_details[0]?.product?.expire_date) }}</span>
                </template>
            </Column>
            <Column :header="t('warehouse')" field="warehouse.warehouse_name" sortable style="min-width: 220px">
                <template #body="{ data }">
                  <Button v-if="data.warehouse?.warehouse_name" icon="pi pi-warehouse" size="small" variant="link" />
                  <span>{{ data.warehouse?.warehouse_name ?? '-' }}</span>
                </template>
            </Column>
            <Column :header="t('to_warehouse')" field="to_warehouse.warehouse_name" sortable style="min-width: 220px">
                <template #body="{ data }">
                    <Button v-if="data.to_warehouse?.warehouse_name" icon="pi pi-warehouse" size="small" variant="link" />
                    <span>{{ data.to_warehouse?.warehouse_name ?? '' }}</span>
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
            <Column :header="t('quantity')" field="quantity" sortable style="min-width: 130px">
                <template #body="{ data }">
                <Tag :value="data.quantity" severity="secondary" icon="pi pi-spin pi-box" :rounded="true">
                    <template 
                      v-if="data.stock_transaction_details[0]?.product 
                      && data.stock_transaction_details[0]?.measurement" 
                      #default>
                      {{`${data.stock_transaction_details[0]?.quantity} ${data.stock_transaction_details[0]?.measurement?.code}`}}
                    </template>
                    <template v-else #default>{{ 0 }}</template>
                </Tag>
                </template>
            </Column>
            <Column :header="t('transfer_number')" field="transaction_number" sortable style="min-width: 180px" />
            <Column :header="t('reference_number')" field="reference_number" sortable style="min-width: 180px" />

            <Column :header="t('remark')" field="reason" sortable style="min-width: 220px" />

            <Column :header="t('transfer_date')" field="created_at" sortable style="min-width: 160px">
                <template #body="{ data }">
                <span>{{ formatDate(data.created_at) }}</span>
                </template>
            </Column>

            <Column :header="t('action')" style="min-width: 160px">
                <template #body="{ data }">
                  <Button
                      icon="pi pi-eye"
                      severity="warning"
                      text
                      
                      size="small"
                      @click="onOpenDetailDialog(data)"
                  />
                </template>
            </Column>
        </DataTable>
        <Dialog
          :visible="openDialog"
          :closable="false"
          modal
          :maximizable="true"
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
              
                <div class="flex items-center gap-2 justify-between">
                  <div class="w-full">
                      <InputGroup class="mt-2 w-full">
                          <InputGroupAddon>
                              <Button icon="pi pi-warehouse" variant="link" />
                          </InputGroupAddon>
                          <FloatLabel variant="on">
                          <Select
                              v-model="stockForm.warehouse_id"
                              :options="props.warehouseOptions"
                              option-value="id"
                              option-label="warehouse_name"
                              :invalid="Boolean(errors.warehouse_id)"
                          />
                          <label>{{ t('warehouse') }} *</label>
                          </FloatLabel>
                      </InputGroup>
                      <Message v-if="errors.warehouse_id" severity="error" size="small" variant="simple">
                          {{ errors.warehouse_id }}
                      </Message>    
                  </div>
                  <div class="w-full">
                    <InputGroup class="mt-2 w-full">
                      <InputGroupAddon>
                      <Button icon="pi pi-warehouse" variant="link" />
                      </InputGroupAddon>
                      <FloatLabel variant="on">
                      <Select
                          v-model="stockForm.to_warehouse_id"
                          :options="props.warehouseOptions"
                          option-label="warehouse_name"
                          option-value="id"
                          show-clear
                      />
                      <label>{{ t('warehouse') }} </label>
                      </FloatLabel>
                  </InputGroup>
                  </div>
                </div>

                <InputGroup class="mt-2">
                  <InputGroupAddon>
                    <Button icon="pi pi-warehouse" variant="link" />
                  </InputGroupAddon>
                  <FloatLabel variant="on">
                    <Select
                      v-model="stockForm.transaction_type"
                      :options="transactionTypeOptions"
                      option-label="label"
                      option-value="value"
                      show-clear
                      :invalid="Boolean(errors.transaction_type)"
                    />
                    <label>{{ t('transaction_type') }} *</label>
                  </FloatLabel>
                </InputGroup>
                <Message v-if="errors.transaction_type" severity="error" size="small" variant="simple">
                  {{ errors.transaction_type }}
                </Message>
              <div class="flex items-center gap-2">
                  <InputGroup class="mt-2">
                      <InputGroupAddon>
                          <Button icon="pi pi-hashtag" variant="link" />
                      </InputGroupAddon>
                      <FloatLabel variant="on">
                          <InputText v-model="stockForm.transaction_number" />
                          <label>{{ t('transfer_number') }}</label>
                      </FloatLabel>
                  </InputGroup>
                  <InputGroup class="mt-2">
                      <InputGroupAddon>
                          <Button icon="pi pi-hashtag" variant="link" />
                      </InputGroupAddon>
                      <FloatLabel variant="on">
                          <InputText v-model="stockForm.reference_number" />
                          <label>{{ t('reference_number') }}</label>
                      </FloatLabel>
                  </InputGroup>
              </div>
              <InputGroup class="md:col-span-2 mt-2">
                <InputGroupAddon>
                  <Button icon="pi pi-comment" variant="link" />
                </InputGroupAddon>
                <FloatLabel variant="on">
                  <Textarea v-model="stockForm.reason" rows="2" class="w-full" />
                  <label>{{ t('remark') }}</label>
                </FloatLabel>
              </InputGroup>
              <Divider>
                  <span class="text-xs font-semibold uppercase text-slate-500">
                  {{ `${t('currentQuantity')} ${t('product')}` }}
                  </span>
              </Divider>
              <Button
                :label="t('btnCreate') + ' ' + t('product')"
                icon="pi pi-plus"
                class="mb-1"
                size="small"
                @click="addNewRowProduct"
              />
              <DataTable 
                :value="stockForm.details" 
                editMode="cell" 
                show-gridlines
                show-headers
                rezizable-columns
                scroll-height="300px"
                column-resize-mode="fit"
                size="small"
                striped-rows
                scrollable
                @cell-edit-complete="onCellEditComplete"
                :pt="{
                  table: { style: 'min-width: 50rem' },
                  column: {
                    bodycell: ({ state }: { state: any }) => ({
                      class: [{ '!py-0': state['d_editing'] }]
                    })
                  }
                }"
              >
                  <Column 
                    v-for="col of columns" 
                    :key="col.field" 
                    :field="col.field" 
                    :header="col.header" 
                    style="width: 15%"
                  >
                      <template #body="{ data, field }">
                        <!-- Product -->
                        <template v-if="field === 'product_id'">
                            {{ getProductName(data.product_id) }}
                        </template>

                        <!-- Measurement -->
                        <template v-else-if="field === 'measurement_id'">
                            {{ getMeasurementName(data.measurement_id) }}
                        </template>

                        <!-- Currency -->
                        <template v-else-if="field === 'currency_id'">
                            {{ getCurrencyName(data.currency_id) }}
                        </template>

                        <template v-else-if="field === 'total_price'">
                            <span class="float-right">{{ data.total_price }}</span>
                        </template>

                        <template v-else>
                            {{ data[field as string]  }}
                        </template>
                      </template>
                      <template #editor="{ data, field }">
                          <!-- PRODUCT -->
                        <Select
                            v-if="field === 'product_id'"
                            v-model="data.product_id"
                            :options="productOptions"
                            optionLabel="name"
                            optionValue="id"
                            :placeholder="t('select').replace('{0}',t('product'))"
                            show-clear
                            size="small"
                            filter
                            fluid
                            :highlight-on-select="true"
                            :virtual-scroller-options="{ itemSize: 38, }"
                        />

                        <!-- QUANTITY -->
                        <InputNumber
                            v-else-if="field === 'quantity'"
                            v-model="data.quantity"
                            :min="0"
                            autofocus
                            size="small"
                            fluid
                            
                        />
                        <!-- MEASUREMENT @update:modelValue="calculateTotal(data)" -->
                        <Select
                            v-else-if="field === 'measurement_id'"
                            v-model="data.measurement_id"
                            :options="measurementOptions"
                            optionLabel="code"
                            optionValue="id"
                            size="small"
                            :placeholder="t('select').replace('{0}',t('measurement'))"
                            fluid
                        />

                        <!-- UNIT PRICE -->
                        <InputNumber
                            v-else-if="field === 'unit_price'"
                            v-model="data.unit_price"
                            :min="0"
                            autofocus
                            size="small"
                        />
                        <!-- @update:modelValue="calculateTotal(data)" -->
                        <!-- EXCHANGE RATE -->
                        <InputNumber
                            v-else-if="field === 'exchange_rate'"
                            v-model="data.exchange_rate"
                            :min="0"
                            autofocus
                            fluid
                            size="small"
                            
                        />

                        

                        <!-- CURRENCY @update:modelValue="calculateTotal(data)" -->
                        <Select
                            v-else-if="field === 'currency_id'"
                            v-model="data.currency_id"
                            :options="currencies"
                            optionLabel="code"
                            optionValue="id"
                            size="small"
                            :placeholder="t('select').replace('{0}',t('currency'))"
                            fluid
                        />
                      </template>
                  </Column>
                  <Column :header="t('action')">
                    <template #body="{ index }">
                        <Button
                            icon="pi pi-trash"
                            severity="danger"
                            variant="text"
                            size="small"
                            @click="removeRowProductDetail(index)"
                        />
                    </template>
                </Column>
              </DataTable>
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
        <Dialog
          v-model:visible="openDetailDialog"
          :closable="true"
          modal
          :maximizable="true"
          style="width: 100%; height: 100%;"
          :header="t('detail')"
        >
          <template #default>
            <DataTable
              paginator
              :rows="pagination.limit"
              :total-records="pagination.total"
              :rows-per-page-options="[5, 10, 20, 50, 100]"
              :value="stockTransactionDetail"
              :loading="loading"
              :global-filter-fields="[]"
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
              
            >
              <template #header>
                <Toolbar style="border: none;">
                  <template #start>
                    <Button icon="pi pi-filter-slash" variant="link" @click="clearFilter" />
                  </template>
                  <template #end>
                    <Button icon="pi pi-file-excel" class="mr-2" :label="t('export')"  />
                    <Button icon="pi pi-file-pdf" :label="t('export')" />
                  </template>
                </Toolbar>
              </template>

              <template #empty>{{ t('empty') }}</template>
              
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
                  <span>{{ formatDate(data.product?.expire_date) }}</span>
                  </template>
              </Column>
              <Column :header="t('quantity')" field="quantity" sortable style="min-width: 130px">
                <template #body="{ data }">
                  <Tag :value="data.quantity" severity="secondary" icon="pi pi-spin pi-box" :rounded="true">
                      <template 
                        v-if="data.measurement && data.quantity > 0" 
                        #default>
                        {{`${data.quantity} ${data.measurement?.code}`}}
                      </template>
                      <template v-else #default>{{ data.quantity }}</template>
                  </Tag>
                </template>
              </Column>
              <Column :header="t('unit_price')" field="unit_price" sortable style="min-width: 130px">
                <template #body="{ data }">
                  <Tag :value="data.unit_price" :rounded="true">
                      <template v-if="data.unit_price && data.currency" #default>
                        {{`${data.unit_price} ${data.currency?.symbol}`}}
                      </template>
                      <template v-else #default>{{ data.unit_price }}</template>
                  </Tag>
                </template>
              </Column>
              <Column :header="t('exchange_rate')" field="exchange_rate" sortable style="min-width: 130px">
                <template #body="{ data }">
                  <Tag :value="data.exchange_rate" :rounded="true">
                      <template #default>
                        {{`${data.exchange_rate}`}}
                      </template>
                  </Tag>
                </template>
              </Column>
              <Column :header="t('total_price')" field="total_price" sortable style="min-width: 130px;">
                <template #body="{ data }">
                  <Tag :value="data.total_price" :rounded="true" class="float-right">
                      <template v-if="data.total_price && data.currency" #default>
                        {{`${data.total_price} ${data.currency?.symbol}`}}
                      </template>
                      <template v-else #default>{{ data.total_price }}</template>
                  </Tag>
                </template>
              </Column>
              <Column :header="t('base_total_price')" field="base_total_price" sortable style="min-width: 130px">
                <template #body="{ data }">
                  <Tag :value="data.base_total_price" :rounded="true" class="float-right">
                      <template #default>
                        {{`${data.base_total_price}`}}
                      </template>
                  </Tag>
                </template>
              </Column>
              <Column :header="t('currency')" field="currency.code" sortable style="min-width: 180px" />
              <Column :header="t('transfer_date')" field="created_at" sortable style="min-width: 160px">
                <template #body="{ data }">
                  <span>{{ formatDate(data.created_at) }}</span>
                </template>
              </Column>
            </DataTable>
          </template>
          
        </Dialog>
    </div>
</template>
<script lang="ts" setup>
    import type { Errors, StockTransactionDetailCreate, StockTransactionCreate, TransactionType } from '~~/shared/types/stocktransaction'
    import type { Measurement} from '~~/shared/types/measurement'
    import type { product } from '~/composables/useProduct'
    import type { Warehouse } from '~~/shared/types/warehouse'
    import type { Currency } from '~~/shared/types/currency'
    interface Pagination {
        page: number
        limit: number
        total: number
    }
    interface Props {
        productOptions: product[],
        warehouseOptions: Warehouse[],
        measurementOptions: Measurement[]
    }
    const { confirmDelete } = useConfirmDelete()
    const currencyAction = useCurrency()
    const messageBox = MessageBox()
    const StockTransactionActions = useStockTransaction()
    const pagination = ref<Pagination>({ page: 1, limit: 10, total: 0})
    const stockForm = ref<StockTransactionCreate>(StockTransactionActions.createEmptyStockTransaction())
    const errors = ref<Errors>(StockTransactionActions.createStockTransactionErrors())
    const filters = ref(StockTransactionActions.createStockTransactionFilters())
    const { t } = useI18n()
    const props = defineProps<Props>()
    const data = ref([])
    const openDetailDialog = ref(false)
    const btnLoading = ref(false)
    const loading = ref(false)
    const editMode = ref(false)
    const openDialog = ref(false)
    const selectStock = ref([])
    const stockTransactionDetail = ref<StockTransactionDetailCreate[]>([])
    const successMessage = () => messageBox.success(t('successMessage'))
    const warningMessage = () => messageBox.warning(t('warningMessage'))
    const errorMessage = () => messageBox.error(t('errorMessage'))
    const currencies = ref<Currency[]>([
        
    ])
    const addNewRowProduct = () => {
        stockForm.value.details.push({
            product_id: null,
            measurement_id: null,
            quantity: 0,
            total_price: 0,
            unit_price: 0,
            exchange_rate: 0,
            currency_id: null,
        })
    }
    const onOpenDetailDialog = (data: any) => {
      openDetailDialog.value = true
      stockTransactionDetail.value = data.stock_transaction_details
    }
    const removeRowProductDetail = (index: number) => {
      stockForm.value.details.splice(index, 1)
    }
    const columns = ref([
        { field: 'product_id', header: t('product') },
        { field: 'quantity', header: t('quantity') },
        { field: 'measurement_id', header: t('measurement') },
        { field: 'unit_price', header: t('unit_price') },
        { field: 'exchange_rate', header: t('exchange_rate') },
        { field: 'total_price', header: t('total') },
        { field: 'currency_id', header: t('currency') },
    ]);
    const calculateTotal = (row: any) => {
      const quantity = Number(row.quantity) || 0
      const unitPrice = Number(row.unit_price) || 0
      const exchangeRate = Number(row.exchange_rate) || 1

      row.total_price = quantity * unitPrice * exchangeRate
    }
    const formatCurrency = (value: number) => {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
    }
    const getAllCurrency = async () => { 
      try{
        currencies.value = await currencyAction.getAllCurrency()
      }catch(error){
        errorMessage()
      }finally{

      }
    }
    const getProductName = (id: number | null) => {
      const product = props.productOptions.find(
          item => item.id === id
      )
      const productName = product?.name 
      return productName ?? ''
    }
    const getMeasurementName = (id: number | null) => {
    const measurement = props.measurementOptions.find(
        item => item.id === id
    )

      return measurement?.code ?? ''
    }
    const getCurrencyName = (id: number | null) => {
    const currency = currencies.value.find(
        item => item.id === id
    )

      return currency?.code ?? ''
    }
    const onCellEditComplete = (event: any) => {
      const { data, newValue, field } = event as { data: StockTransactionDetailCreate; newValue: any; field: keyof StockTransactionDetailCreate };
      if (field === 'total_price') {
          return
      }
      data[field] = newValue
      if (
          field === 'quantity' ||
          field === 'unit_price' ||
          field === 'exchange_rate'
      ) {
        calculateTotal(data)
      }
    }
    
    const onOpenDialog = () => {
      editMode.value = false
      errors.value = StockTransactionActions.createStockTransactionErrors()
      stockForm.value = StockTransactionActions.createEmptyStockTransaction()
      openDialog.value = true
    }
    const clearFilter = () => { 
      filters.value = StockTransactionActions.createStockTransactionFilters()
      selectStock.value = []
      getAll()
    }
    const create = async () => {
      try{
        console.log(`Stock Form >>>>>>>>>>>>>>>>>`, stockForm.value)
        btnLoading.value = true
        loading.value = true
        await StockTransactionActions.createStockTransaction(stockForm.value)
        await getAll()
        successMessage()
        close()
      }catch(error){
        const apiError = error as { data?: { data?: { detail?: unknown } } }
        errors.value = StockTransactionActions.applyStockTransactionValidationErrors(apiError?.data?.data?.detail, errors.value)
        if(!errors.value) errorMessage()
      }finally{
        btnLoading.value = false
        loading.value = false
      }
    }
    const update = async () => {
      try{
        btnLoading.value = true
        loading.value = true
        await StockTransactionActions.update(stockForm.value.id as number, stockForm.value)
        await getAll()
        successMessage()
        close()
      }catch(error){
        const apiError = error as { data?: { data?: { detail?: unknown } } }
        errors.value = StockTransactionActions.applyStockTransactionValidationErrors(apiError?.data?.data?.detail, errors.value)
        if(!errors.value) errorMessage()
      }finally{
        btnLoading.value = false
        loading.value = false
      }
    }
    const deleteMany = () => {
      if (!selectStock.value.length) return warningMessage()

      confirmDelete(async () => {
        loading.value = true
        try {
          await StockTransactionActions.remove(selectStock.value.map((item: any) => item.id))
          successMessage()
          await getAll()
        } catch (error) {
          errorMessage()
        }
        finally {
          selectStock.value = []
          loading.value = false
        }
      })
    }
    const getAll = async () => {
      loading.value = true
      const params = new URLSearchParams({
        page: pagination.value.page.toString(),
        limit: pagination.value.limit.toString(),
      })
      try{
        const response = await StockTransactionActions.getAll(params.toString()) as any
        data.value = Array.isArray(response.data) ? response.data : []
        pagination.value.total = response.pagination?.total_records ?? 0
      }
      catch(error){
      
      }finally{
        loading.value = false
      }
    }
    const close = () => {
      openDialog.value = false
      stockForm.value = StockTransactionActions.createEmptyStockTransaction()
    }
    const openEditMode = (data: any) => {
      const value = data.data
      editMode.value =true
      stockForm.value.id = value.id
      stockForm.value.reason = value.reason
      stockForm.value.reference_number = value.reference_number
      stockForm.value.warehouse_id = value.warehouse_id
      stockForm.value.to_warehouse_id = value.to_warehouse_id
      stockForm.value.transaction_number = value.transaction_number
      stockForm.value.transaction_type = value.transaction_type
      const details = value.stock_transaction_details
      const stock_detail = []
      const detail = { 
        product_id: details.product_id,
        measurement_id: details.measurement_id,
        quantity: details.quantity,
        unit_price: details.unit_price,
        currency_id: details.currency_id,
        total_price: details.total_price,
        exchange_rate: details.exchange_rate
      } as StockTransactionDetailCreate
      stock_detail.push(detail)
      stockForm.value.details = value.stock_transaction_details
      openDialog.value = true
    }
    const transactionTypeOptions = [
        { label: t('stock_in'), value: 'STOCK_IN' },
        { label: t('stock_out'), value: 'STOCK_OUT' },
        { label: t('adjustment'), value: 'ADJUSTMENT' },
        { label: t('return'), value: 'RETURN' },
        { label: t('damage'), value: 'DAMAGE' },
        { label: t('quarantine'), value: 'QUARANTINE' },
        { label: t('internal_transfer'), value: 'INTERNAL_TRANSFER' },
    ]
    onMounted(() => {
      getAll()
      getAllCurrency()
    })
</script>