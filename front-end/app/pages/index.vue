<template>
  <main id="dashboard" class="space-y-6 pb-8">
    <section class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="text-sm font-medium text-primary">Dashboard</p>
        <h1 class="mt-1 text-2xl font-semibold tracking-tight">Business overview</h1>
        <p class="mt-1 text-sm text-surface-500">
          A live summary of the records available to you.
          <span v-if="lastUpdated">Updated {{ formatUpdatedAt(lastUpdated) }}.</span>
        </p>
      </div>

      <div class="flex flex-wrap gap-2">
        <Button label="New order" icon="pi pi-plus" size="small" @click="navigateTo('/order')" />
        <Button label="View stock" icon="pi pi-warehouse" severity="secondary" outlined size="small" @click="navigateTo('/stock')" />
        <Button icon="pi pi-refresh" severity="secondary" outlined size="small" :loading="loading" aria-label="Refresh dashboard" @click="loadDashboard" />
      </div>
    </section>

    <Message v-if="hasUnavailableSources" severity="warn" :closable="false">
      Some dashboard data could not be loaded because it is unavailable for your account.
    </Message>

    <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4" aria-label="Key metrics">
      <Card v-if="available.orders" class="border border-blue-100 bg-blue-50/70 dark:border-blue-900/70 dark:bg-blue-950/30">
        <template #content>
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-surface-600 dark:text-surface-300">Total orders</p>
              <p class="mt-2 text-3xl font-semibold">{{ formatNumber(orders.length) }}</p>
              <p class="mt-2 text-xs text-surface-500">{{ deliveredOrders }} delivered · {{ openOrders }} open</p>
            </div>
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-100 text-blue-600 dark:bg-blue-900/70 dark:text-blue-300">
              <i class="pi pi-shopping-cart text-xl" />
            </span>
          </div>
        </template>
      </Card>

      <Card v-if="available.invoices" class="border border-emerald-100 bg-emerald-50/70 dark:border-emerald-900/70 dark:bg-emerald-950/30">
        <template #content>
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-surface-600 dark:text-surface-300">Invoice amount</p>
              <p class="mt-2 text-3xl font-semibold">{{ formatAmount(invoiceTotal) }}</p>
              <p class="mt-2 text-xs text-surface-500">{{ formatAmount(invoicePaid) }} paid · {{ formatAmount(invoiceOutstanding) }} outstanding</p>
            </div>
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-100 text-emerald-600 dark:bg-emerald-900/70 dark:text-emerald-300">
              <i class="pi pi-receipt text-xl" />
            </span>
          </div>
        </template>
      </Card>

      <Card v-if="available.customers" class="border border-amber-100 bg-amber-50/70 dark:border-amber-900/70 dark:bg-amber-950/30">
        <template #content>
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-surface-600 dark:text-surface-300">Customers</p>
              <p class="mt-2 text-3xl font-semibold">{{ formatNumber(customers.length) }}</p>
              <p class="mt-2 text-xs text-surface-500">{{ customersWithOrders }} with recorded orders</p>
            </div>
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-amber-100 text-amber-600 dark:bg-amber-900/70 dark:text-amber-300">
              <i class="pi pi-users text-xl" />
            </span>
          </div>
        </template>
      </Card>

      <Card v-if="available.products" class="border border-violet-100 bg-violet-50/70 dark:border-violet-900/70 dark:bg-violet-950/30">
        <template #content>
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-surface-600 dark:text-surface-300">Inventory units</p>
              <p class="mt-2 text-3xl font-semibold">{{ formatNumber(inventoryUnits) }}</p>
              <p class="mt-2 text-xs text-surface-500">{{ lowStockProducts.length }} products at or below 25 units</p>
            </div>
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-100 text-violet-600 dark:bg-violet-900/70 dark:text-violet-300">
              <i class="pi pi-box text-xl" />
            </span>
          </div>
        </template>
      </Card>
    </section>

    <section v-if="loading" class="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <Card v-for="item in 3" :key="item" class="lg:first:col-span-2">
        <template #content><Skeleton height="19rem" /></template>
      </Card>
    </section>

    <template v-else>
      <section v-if="available.orders" class="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card class="lg:col-span-2">
          <template #title>
            <div class="flex items-center justify-between gap-3">
              <span>Orders over the last six months</span>
              <Tag :value="`${orders.length} total`" severity="info" />
            </div>
          </template>
          <template #content>
            <div v-if="orders.length" class="h-80">
              <Chart type="line" :data="orderTrendData" :options="lineChartOptions" class="h-full" />
            </div>
            <DashboardEmpty v-else icon="pi pi-shopping-cart" message="No orders have been recorded yet." />
          </template>
        </Card>

        <Card>
          <template #title>Order status</template>
          <template #content>
            <div v-if="orders.length" class="h-80">
              <Chart type="doughnut" :data="orderStatusData" :options="doughnutChartOptions" class="h-full" />
            </div>
            <DashboardEmpty v-else icon="pi pi-chart-pie" message="No order status data yet." />
          </template>
        </Card>
      </section>

      <section v-if="available.products" class="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <template #title>Inventory by category</template>
          <template #content>
            <div v-if="products.length" class="h-72">
              <Chart type="bar" :data="stockByCategoryData" :options="barChartOptions" class="h-full" />
            </div>
            <DashboardEmpty v-else icon="pi pi-box" message="No products have been added yet." />
          </template>
        </Card>

        <Card>
          <template #title>
            <div class="flex items-center justify-between gap-3">
              <span>Inventory attention</span>
              <Button label="View stock" icon="pi pi-arrow-right" severity="secondary" text size="small" @click="navigateTo('/stock')" />
            </div>
          </template>
          <template #content>
            <DataTable v-if="lowStockProducts.length" :value="lowStockProducts" size="small" striped-rows>
              <Column field="name" header="Product">
                <template #body="{ data }">
                  <div>
                    <p class="font-medium">{{ data.name }}</p>
                    <p class="text-xs text-surface-500">{{ productCategoryName(data) }}</p>
                  </div>
                </template>
              </Column>
              <Column header="Available" class="text-right">
                <template #body="{ data }">
                  <Tag :value="formatNumber(productStock(data))" :severity="productStock(data) === 0 ? 'danger' : 'warn'" />
                </template>
              </Column>
            </DataTable>
            <DashboardEmpty v-else icon="pi pi-check-circle" message="No products are at or below 25 units." />
          </template>
        </Card>
      </section>

      <section v-if="available.orders">
        <Card>
          <template #title>
            <div class="flex items-center justify-between gap-3">
              <span>Recent orders</span>
              <Button label="View all" icon="pi pi-arrow-right" severity="secondary" text size="small" @click="navigateTo('/order')" />
            </div>
          </template>
          <template #content>
            <DataTable v-if="recentOrders.length" :value="recentOrders" size="small" striped-rows responsive-layout="scroll">
              <Column field="order_number" header="Order #" />
              <Column header="Customer">
                <template #body="{ data }">{{ customerName(data.customer_id) }}</template>
              </Column>
              <Column header="Order date">
                <template #body="{ data }">{{ formatDate(data.order_date) }}</template>
              </Column>
              <Column header="Required date">
                <template #body="{ data }">{{ formatDate(data.required_date) }}</template>
              </Column>
              <Column header="Status">
                <template #body="{ data }">
                  <Tag :value="formatStatus(data.status)" :severity="orderStatusSeverity(data.status)" />
                </template>
              </Column>
            </DataTable>
            <DashboardEmpty v-else icon="pi pi-shopping-cart" message="No orders have been recorded yet." />
          </template>
        </Card>
      </section>

      <section v-if="!hasAnyData" class="py-12">
        <DashboardEmpty icon="pi pi-database" message="There is no dashboard data to display yet." />
      </section>
    </template>
  </main>
</template>

<script setup lang="ts">
import type { AxiosInstance } from 'axios'
// import { computed, defineComponent, h, onMounted, ref } from 'vue'

definePageMeta({ layout: 'dashboard' })

type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled' | string

type SalesOrder = {
  id: number
  order_number: string
  customer_id: number | null
  order_date?: string | null
  required_date?: string | null
  status: OrderStatus
}

type Customer = {
  id: number
  customer_name: string
}

type Product = {
  id: number
  name: string
  category_id?: number | null
  category_name?: string | null
  stock?: number | string | null
}

type Category = {
  id: number
  name: string
}

type Invoice = {
  id: number
  amount: number | string
  paid_amount: number | string
  status: string
}

type InvoiceResponse = { data?: Invoice[] }
type DataSource = 'orders' | 'customers' | 'products' | 'categories' | 'invoices'

const { $axios } = useNuxtApp()
const axios = $axios as AxiosInstance

const loading = ref(true)
const lastUpdated = ref<Date | null>(null)
const orders = ref<SalesOrder[]>([])
const customers = ref<Customer[]>([])
const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const invoices = ref<Invoice[]>([])
const available = ref<Record<DataSource, boolean>>({
  orders: false,
  customers: false,
  products: false,
  categories: false,
  invoices: false,
})

const DashboardEmpty = defineComponent({
  props: {
    icon: { type: String, required: true },
    message: { type: String, required: true },
  },
  setup(props) {
    return () => h('div', { class: 'flex h-56 flex-col items-center justify-center text-center text-surface-500' }, [
      h('i', { class: `${props.icon} mb-3 text-3xl text-surface-300` }),
      h('p', { class: 'text-sm' }, props.message),
    ])
  },
})

const toNumber = (value: number | string | null | undefined) => {
  const numberValue = Number(value)
  return Number.isFinite(numberValue) ? numberValue : 0
}

const formatNumber = (value: number) => new Intl.NumberFormat().format(value)
const formatAmount = (value: number) => new Intl.NumberFormat(undefined, { maximumFractionDigits: 2 }).format(value)

const formatDate = (value?: string | null) => {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return new Intl.DateTimeFormat(undefined, { day: '2-digit', month: 'short', year: 'numeric' }).format(date)
}

const formatUpdatedAt = (value: Date) => new Intl.DateTimeFormat(undefined, {
  day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit',
}).format(value)

const formatStatus = (status: OrderStatus) => {
  if (!status) return 'Unknown'
  return status.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

const orderStatusSeverity = (status: OrderStatus) => ({
  delivered: 'success',
  shipped: 'info',
  confirmed: 'warn',
  pending: 'secondary',
  cancelled: 'danger',
}[status] ?? 'secondary') as 'success' | 'info' | 'warn' | 'secondary' | 'danger'

const productStock = (product: Product) => toNumber(product.stock)
const categoryNames = computed(() => new Map(categories.value.map((category) => [category.id, category.name])))
const productCategoryName = (product: Product) =>
  product.category_name || (product.category_id ? categoryNames.value.get(product.category_id) : undefined) || 'Uncategorized'

const customerNames = computed(() => new Map(customers.value.map((customer) => [customer.id, customer.customer_name])))
const customerName = (customerId: number | null) => customerId ? customerNames.value.get(customerId) || `Customer #${customerId}` : '—'

const deliveredOrders = computed(() => orders.value.filter((order) => order.status === 'delivered').length)
const openOrders = computed(() => orders.value.filter((order) => !['delivered', 'cancelled'].includes(order.status)).length)
const customersWithOrders = computed(() => new Set(orders.value.map((order) => order.customer_id).filter(Boolean)).size)
const inventoryUnits = computed(() => products.value.reduce((total, product) => total + productStock(product), 0))
const lowStockProducts = computed(() => products.value
  .filter((product) => productStock(product) <= 25)
  .sort((first, second) => productStock(first) - productStock(second))
  .slice(0, 6))

const invoiceTotal = computed(() => invoices.value.reduce((total, invoice) => total + toNumber(invoice.amount), 0))
const invoicePaid = computed(() => invoices.value.reduce((total, invoice) => total + toNumber(invoice.paid_amount), 0))
const invoiceOutstanding = computed(() => Math.max(invoiceTotal.value - invoicePaid.value, 0))

const dateValue = (value?: string | null) => {
  const date = value ? new Date(value).getTime() : 0
  return Number.isNaN(date) ? 0 : date
}

const recentOrders = computed(() => [...orders.value]
  .sort((first, second) => dateValue(second.order_date) - dateValue(first.order_date))
  .slice(0, 8))

const hasAnyData = computed(() => orders.value.length + customers.value.length + products.value.length + invoices.value.length > 0)
const hasUnavailableSources = computed(() => !loading.value && ['orders', 'customers', 'products', 'invoices']
  .some((source) => !available.value[source as DataSource]))

const monthBuckets = computed(() => {
  const now = new Date()
  return Array.from({ length: 6 }, (_, index) => {
    const date = new Date(now.getFullYear(), now.getMonth() - (5 - index), 1)
    return {
      key: `${date.getFullYear()}-${date.getMonth()}`,
      label: new Intl.DateTimeFormat(undefined, { month: 'short' }).format(date),
    }
  })
})

const orderTrendData = computed(() => ({
  labels: monthBuckets.value.map((month) => month.label),
  datasets: [{
    label: 'Orders',
    data: monthBuckets.value.map((month) => orders.value.filter((order) => {
      const date = order.order_date ? new Date(order.order_date) : null
      return date && !Number.isNaN(date.getTime()) && `${date.getFullYear()}-${date.getMonth()}` === month.key
    }).length),
    borderColor: '#3b82f6',
    backgroundColor: 'rgba(59, 130, 246, 0.14)',
    fill: true,
    tension: 0.35,
    pointRadius: 3,
    pointHoverRadius: 5,
  }],
}))

const orderStatusData = computed(() => {
  const statuses: OrderStatus[] = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
  const counts = statuses.map((status) => orders.value.filter((order) => order.status === status).length)
  return {
    labels: statuses.map(formatStatus),
    datasets: [{
      data: counts,
      backgroundColor: ['#94a3b8', '#f59e0b', '#38bdf8', '#22c55e', '#ef4444'],
      borderWidth: 0,
      hoverOffset: 5,
    }],
  }
})

const stockByCategoryData = computed(() => {
  const totals = new Map<string, number>()
  products.value.forEach((product) => {
    const category = productCategoryName(product)
    totals.set(category, (totals.get(category) || 0) + productStock(product))
  })
  const entries = [...totals.entries()].sort((first, second) => second[1] - first[1]).slice(0, 6)
  return {
    labels: entries.map(([name]) => name),
    datasets: [{
      label: 'Units in stock',
      data: entries.map(([, quantity]) => quantity),
      backgroundColor: '#8b5cf6',
      borderRadius: 6,
      maxBarThickness: 32,
    }],
  }
})

const lineChartOptions = {
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: false }, ticks: { color: '#64748b' } },
    y: { beginAtZero: true, ticks: { precision: 0, color: '#64748b' }, grid: { color: 'rgba(148, 163, 184, 0.18)' } },
  },
}

const doughnutChartOptions = {
  maintainAspectRatio: false,
  cutout: '63%',
  plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, usePointStyle: true, padding: 14, color: '#64748b' } } },
}

const barChartOptions = {
  maintainAspectRatio: false,
  indexAxis: 'y',
  plugins: { legend: { display: false } },
  scales: {
    x: { beginAtZero: true, ticks: { precision: 0, color: '#64748b' }, grid: { color: 'rgba(148, 163, 184, 0.18)' } },
    y: { ticks: { color: '#64748b' }, grid: { display: false } },
  },
}

const loadDashboard = async () => {
  loading.value = true

  const [ordersResult, customersResult, productsResult, categoriesResult, invoicesResult] = await Promise.allSettled([
    axios.get('/sales-order/'),
    axios.get('/customer/'),
    axios.get('/product/'),
    axios.get('/category/'),
    axios.get('/invoice/?page=1&limit=100'),
  ])

  available.value.orders = ordersResult.status === 'fulfilled'
  available.value.customers = customersResult.status === 'fulfilled'
  available.value.products = productsResult.status === 'fulfilled'
  available.value.categories = categoriesResult.status === 'fulfilled'
  available.value.invoices = invoicesResult.status === 'fulfilled'

  orders.value = ordersResult.status === 'fulfilled' && Array.isArray(ordersResult.value.data) ? ordersResult.value.data : []
  customers.value = customersResult.status === 'fulfilled' && Array.isArray(customersResult.value.data) ? customersResult.value.data : []
  products.value = productsResult.status === 'fulfilled' && Array.isArray(productsResult.value.data) ? productsResult.value.data : []
  categories.value = categoriesResult.status === 'fulfilled' && Array.isArray(categoriesResult.value.data) ? categoriesResult.value.data : []
  invoices.value = invoicesResult.status === 'fulfilled' && Array.isArray((invoicesResult.value.data as InvoiceResponse)?.data)
    ? (invoicesResult.value.data as InvoiceResponse).data as Invoice[]
    : []

  lastUpdated.value = new Date()
  loading.value = false
}

onMounted(loadDashboard)
</script>
