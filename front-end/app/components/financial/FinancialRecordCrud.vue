<template>
  <main :id="recordType" class="space-y-6 pb-8">
    <section class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p :class="['text-sm font-medium', labels.accentClass]">Financial</p>
        <h1 class="mt-1 text-2xl font-semibold tracking-tight">{{ labels.title }}</h1>
        <p class="mt-1 text-sm text-surface-500">{{ labels.description }}</p>
      </div>

      <div class="flex flex-wrap gap-2">
        <Button label="Refresh" icon="pi pi-refresh" severity="secondary" outlined size="small" :loading="loading" @click="loadRecords" />
        <Button :label="labels.createLabel" icon="pi pi-plus" size="small" @click="openCreateDialog" />
      </div>
    </section>

    <section class="grid grid-cols-1 gap-4 sm:grid-cols-3" :aria-label="`${labels.title} summary`">
      <Card :class="['border', labels.summaryBorderClass]">
        <template #content>
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-surface-600 dark:text-surface-300">Total {{ labels.title.toLocaleLowerCase() }}</p>
              <p class="mt-2 text-3xl font-semibold">{{ formatAmount(totalAmount) }}</p>
              <p class="mt-2 text-xs text-surface-500">All recorded entries</p>
            </div>
            <span :class="['flex h-11 w-11 items-center justify-center rounded-xl', labels.iconClass]">
              <i :class="[labels.icon, 'text-xl']" />
            </span>
          </div>
        </template>
      </Card>

      <Card class="border border-blue-100 bg-blue-50/70 dark:border-blue-900/70 dark:bg-blue-950/30">
        <template #content>
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-surface-600 dark:text-surface-300">This month</p>
              <p class="mt-2 text-3xl font-semibold">{{ formatAmount(thisMonthAmount) }}</p>
              <p class="mt-2 text-xs text-surface-500">{{ formatNumber(thisMonthCount) }} {{ thisMonthCount === 1 ? 'entry' : 'entries' }}</p>
            </div>
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-100 text-blue-600 dark:bg-blue-900/70 dark:text-blue-300">
              <i class="pi pi-calendar text-xl" />
            </span>
          </div>
        </template>
      </Card>

      <Card class="border border-violet-100 bg-violet-50/70 dark:border-violet-900/70 dark:bg-violet-950/30">
        <template #content>
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-surface-600 dark:text-surface-300">Entries</p>
              <p class="mt-2 text-3xl font-semibold">{{ formatNumber(records.length) }}</p>
              <p class="mt-2 text-xs text-surface-500">{{ formatNumber(categoryCount) }} categor{{ categoryCount === 1 ? 'y' : 'ies' }} used</p>
            </div>
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-100 text-violet-600 dark:bg-violet-900/70 dark:text-violet-300">
              <i class="pi pi-list text-xl" />
            </span>
          </div>
        </template>
      </Card>
    </section>

    <Card>
      <template #content>
        <DataTable
          v-model:selection="selectedRecords"
          v-model:filters="filters"
          :value="records"
          :loading="loading"
          :global-filter-fields="['category', 'counterparty', 'reference_number', 'description']"
          data-key="id"
          paginator
          :rows="10"
          :rows-per-page-options="[5, 10, 20, 50, 100]"
          filter-display="menu"
          size="small"
          striped-rows
          row-hover
          scrollable
          scroll-height="500px"
          @row-dblclick="openEditDialog"
        >
          <template #header>
            <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <IconField class="w-full sm:w-80">
                <InputIcon ><i class="pi pi-search"  /></InputIcon>
                <InputText v-model="filters.global.value" class="w-full" size="small" placeholder="Search entries" />
              </IconField>
              <div class="flex gap-2">
                <Button label="Delete" icon="pi pi-trash" severity="danger" outlined size="small" :disabled="!selectedRecords.length" @click="deleteMany" />
                <Button icon="pi pi-filter-slash" severity="secondary" text size="small" aria-label="Clear filters" @click="clearFilter" />
              </div>
            </div>
          </template>

          <Column selection-mode="multiple" header-style="width: 2.75rem" />
          <Column header="Date" field="transaction_date" sortable>
            <template #body="{ data }">{{ formatDate(data.transaction_date) }}</template>
          </Column>
          <Column header="Category" field="category" sortable />
          <Column :header="labels.counterpartyLabel" field="counterparty" sortable>
            <template #body="{ data }">{{ data.counterparty || '—' }}</template>
          </Column>
          <Column header="Amount" field="amount" sortable body-class="text-right">
            <template #body="{ data }"><span :class="['font-medium', labels.amountClass]">{{ formatAmount(toNumber(data.amount)) }}</span></template>
          </Column>
          <Column header="Reference" field="reference_number" sortable>
            <template #body="{ data }">{{ data.reference_number || '—' }}</template>
          </Column>
          <Column header="Description" field="description" sortable>
            <template #body="{ data }">{{ data.description || '—' }}</template>
          </Column>
          <Column body-class="text-center" style="width: 4.5rem">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" severity="secondary" text size="small" :aria-label="`Edit ${labels.title.toLocaleLowerCase()} entry`" @click="openEditDialog({ data })" />
            </template>
          </Column>
          <template #empty>
            <div class="py-8 text-center text-sm text-surface-500">No {{ labels.title.toLocaleLowerCase() }} entries have been recorded.</div>
          </template>
        </DataTable>
      </template>
    </Card>

    <Dialog 
      v-model:visible="dialogVisible" 
      modal 
      :closable="true" 
      style="width: min(560px, calc(100vw - 2rem))"
    >
      <template #header>
        <Divider>
          <i :class="[labels.icon, labels.accentClass, 'text-xl']" />
          <span class="ml-2 text-xl">{{ editMode ? `Update ${labels.title}` : labels.createLabel }}</span>
        </Divider>
      </template>

      <div class="grid gap-3 sm:grid-cols-2">
        <div class="mt-2">
          <InputGroup>
            <InputGroupAddon><Button icon="pi pi-calendar" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <DatePicker v-model="recordForm.transaction_date" show-icon icon-display="input" date-format="dd-mm-yy" :invalid="Boolean(errors.transaction_date)" class="w-full" />
              <label>Date *</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="errors.transaction_date" severity="error" size="small" variant="simple">{{ errors.transaction_date }}</Message>
        </div>

        <div class="mt-2">
          <InputGroup>
            <InputGroupAddon><Button icon="pi pi-dollar" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <InputNumber v-model="recordForm.amount" :min="0" :min-fraction-digits="2" :max-fraction-digits="2" :invalid="Boolean(errors.amount)" class="w-full" />
              <label>Amount *</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="errors.amount" severity="error" size="small" variant="simple">{{ errors.amount }}</Message>
        </div>

        <div>
          <InputGroup>
            <InputGroupAddon><Button icon="pi pi-tag" variant="link" /></InputGroupAddon>
            <FloatLabel variant="on">
              <InputText v-model.trim="recordForm.category" :invalid="Boolean(errors.category)" />
              <label>Category *</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="errors.category" severity="error" size="small" variant="simple">{{ errors.category }}</Message>
        </div>

        <InputGroup>
          <InputGroupAddon><Button icon="pi pi-user" variant="link" /></InputGroupAddon>
          <FloatLabel variant="on">
            <InputText v-model.trim="recordForm.counterparty" />
            <label>{{ labels.counterpartyLabel }}</label>
          </FloatLabel>
        </InputGroup>

        <InputGroup class="sm:col-span-2">
          <InputGroupAddon><Button icon="pi pi-hashtag" variant="link" /></InputGroupAddon>
          <FloatLabel variant="on">
            <InputText v-model.trim="recordForm.reference_number" />
            <label>Reference number</label>
          </FloatLabel>
        </InputGroup>

        <InputGroup class="sm:col-span-2">
          <InputGroupAddon><Button icon="pi pi-align-left" variant="link" /></InputGroupAddon>
          <FloatLabel variant="on">
            <Textarea v-model.trim="recordForm.description" class="w-full" rows="3" auto-resize />
            <label>Description</label>
          </FloatLabel>
        </InputGroup>
      </div>

      <template #footer>
        <Button 
          icon="pi pi-check" 
          :label="t('btnSave')" 
          :loading="saving" 
          size="small"
          @click="editMode ? updateRecord() : createRecord()" 
        />
        <Button 
          icon="pi pi-times" 
          :label="t('btnCancel')" 
          size="small"
          @click="closeDialog"
        />
      </template>
    </Dialog>
  </main>
</template>

<script setup lang="ts">
import { formatDate, parseDate } from '~/utils/dateFormat'
import { useFinancialRecord } from '~/composables/useFinancialRecord'
import { createFinancialRecordFilters } from '~/services/financial-record.service'
import {
  createEmptyFinancialRecordForm,
  createFinancialRecordErrors,
  type FinancialRecord,
  type FinancialRecordErrors,
  type FinancialRecordForm,
  type FinancialRecordType,
} from '~~/shared/types/financial-record'
const { t } = useI18n()
const props = defineProps<{ recordType: FinancialRecordType }>()
const financialRecordAction = useFinancialRecord(props.recordType)
const { confirmDelete } = useConfirmDelete()
const messageBox = MessageBox()

const records = ref<FinancialRecord[]>([])
const selectedRecords = ref<FinancialRecord[]>([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const editMode = ref(false)
const filters = ref(createFinancialRecordFilters())
const errors = ref<FinancialRecordErrors>(createFinancialRecordErrors())
const recordForm = ref<FinancialRecordForm>(createEmptyFinancialRecordForm())

const labels = computed(() => props.recordType === 'income'
  ? {
      title: 'Income',
      description: 'Record and review money received by your business.',
      createLabel: 'Add income',
      counterpartyLabel: 'Source',
      icon: 'pi pi-wallet',
      accentClass: 'text-emerald-600',
      amountClass: 'text-emerald-600',
      iconClass: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/70 dark:text-emerald-300',
      summaryBorderClass: 'border-emerald-100 bg-emerald-50/70 dark:border-emerald-900/70 dark:bg-emerald-950/30',
    }
  : {
      title: 'Expense',
      description: 'Record and review money spent by your business.',
      createLabel: 'Add expense',
      counterpartyLabel: 'Payee',
      icon: 'pi pi-credit-card',
      accentClass: 'text-rose-600',
      amountClass: 'text-rose-600',
      iconClass: 'bg-rose-100 text-rose-600 dark:bg-rose-900/70 dark:text-rose-300',
      summaryBorderClass: 'border-rose-100 bg-rose-50/70 dark:border-rose-900/70 dark:bg-rose-950/30',
    })

const toNumber = (value: number | string | null | undefined) => {
  const amount = Number(value)
  return Number.isFinite(amount) ? amount : 0
}

const formatAmount = (value: number) => new Intl.NumberFormat(undefined, {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
}).format(value)

const formatNumber = (value: number) => new Intl.NumberFormat().format(value)

const totalAmount = computed(() => records.value.reduce((total, record) => total + toNumber(record.amount), 0))
const thisMonthRecords = computed(() => {
  const today = new Date()
  return records.value.filter((record) => {
    const date = record.transaction_date ? parseDate(record.transaction_date) : null
    return date && date.getFullYear() === today.getFullYear() && date.getMonth() === today.getMonth()
  })
})
const thisMonthAmount = computed(() => thisMonthRecords.value.reduce((total, record) => total + toNumber(record.amount), 0))
const thisMonthCount = computed(() => thisMonthRecords.value.length)
const categoryCount = computed(() => new Set(records.value.map((record) => record.category.trim().toLocaleLowerCase()).filter(Boolean)).size)

const clearFilter = () => {
  filters.value = createFinancialRecordFilters()
}

const resetForm = () => {
  errors.value = createFinancialRecordErrors()
  recordForm.value = createEmptyFinancialRecordForm()
}

const openCreateDialog = () => {
  editMode.value = false
  resetForm()
  dialogVisible.value = true
}

const openEditDialog = (event: { data: FinancialRecord }) => {
  const record = event.data
  editMode.value = true
  errors.value = createFinancialRecordErrors()
  recordForm.value = {
    id: record.id,
    transaction_date: parseDate(record.transaction_date) ?? new Date(),
    amount: toNumber(record.amount),
    category: record.category,
    counterparty: record.counterparty ?? '',
    reference_number: record.reference_number ?? '',
    description: record.description ?? '',
  }
  dialogVisible.value = true
}

const closeDialog = () => {
  dialogVisible.value = false
  editMode.value = false
  saving.value = false
  resetForm()
}

const validate = () => {
  const nextErrors = createFinancialRecordErrors()
  if (!recordForm.value.transaction_date) nextErrors.transaction_date = 'Date is required.'
  if (recordForm.value.amount <= 0) nextErrors.amount = 'Amount must be greater than zero.'
  if (!recordForm.value.category.trim()) nextErrors.category = 'Category is required.'
  return nextErrors
}

const makePayload = (): FinancialRecordForm => ({
  ...recordForm.value,
  transaction_date: recordForm.value.transaction_date ? new Date(recordForm.value.transaction_date) : null,
  category: recordForm.value.category.trim(),
  counterparty: recordForm.value.counterparty.trim(),
  reference_number: recordForm.value.reference_number.trim(),
  description: recordForm.value.description.trim(),
})

const loadRecords = async () => {
  loading.value = true
  try {
    records.value = await financialRecordAction.list()
  } catch {
    records.value = []
    messageBox.error(`Unable to load ${labels.value.title.toLocaleLowerCase()} records.`)
  } finally {
    loading.value = false
  }
}

const save = async (action: () => Promise<unknown>) => {
  const nextErrors = validate()
  if (nextErrors.transaction_date || nextErrors.amount || nextErrors.category) {
    errors.value = nextErrors
    return
  }

  saving.value = true
  try {
    await action()
    await loadRecords()
    messageBox.success(`${labels.value.title} record saved.`)
    closeDialog()
  } catch {
    messageBox.error(`Unable to save this ${labels.value.title.toLocaleLowerCase()} record.`)
  } finally {
    saving.value = false
  }
}

const createRecord = async () => save(() => financialRecordAction.create(makePayload()))

const updateRecord = async () => {
  if (typeof recordForm.value.id !== 'number') return
  await save(() => financialRecordAction.update(recordForm.value.id as number, makePayload()))
}

const deleteMany = () => {
  const ids = selectedRecords.value
    .map((record) => record.id)
    .filter((id): id is number => typeof id === 'number')

  if (!ids.length) return

  confirmDelete(async () => {
    loading.value = true
    try {
      await financialRecordAction.remove(ids)
      selectedRecords.value = []
      await loadRecords()
      messageBox.success(`${labels.value.title} record${ids.length === 1 ? '' : 's'} deleted.`)
    } catch {
      messageBox.error(`Unable to delete the selected ${labels.value.title.toLocaleLowerCase()} records.`)
    } finally {
      loading.value = false
    }
  })
}

onMounted(loadRecords)
</script>
