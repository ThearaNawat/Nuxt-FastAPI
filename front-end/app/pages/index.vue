<template>
  <div id="dashboard" class="space-y-6 pb-8 overflow-auto">
    <!-- KPI Cards Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800">
        <template #content>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-600 dark:text-gray-300 text-sm font-semibold mb-2">Total Sales</p>
              <p class="text-3xl font-bold text-blue-600 dark:text-blue-300">{{ totalSales }}</p>
              <p class="text-green-600 text-xs mt-2">+12% from last month</p>
            </div>
            <i class="pi pi-shopping-cart text-3xl text-blue-200 dark:text-blue-400"></i>
          </div>
        </template>
      </Card>

      <Card class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900 dark:to-green-800">
        <template #content>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-600 dark:text-gray-300 text-sm font-semibold mb-2">Total Orders</p>
              <p class="text-3xl font-bold text-green-600 dark:text-green-300">{{ totalOrders }}</p>
              <p class="text-green-600 text-xs mt-2">+8% from last month</p>
            </div>
            <i class="pi pi-list text-3xl text-green-200 dark:text-green-400"></i>
          </div>
        </template>
      </Card>

      <Card class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900 dark:to-purple-800">
        <template #content>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-600 dark:text-gray-300 text-sm font-semibold mb-2">Products in Stock</p>
              <p class="text-3xl font-bold text-purple-600 dark:text-purple-300">{{ productsInStock }}</p>
              <p class="text-red-600 text-xs mt-2">3 low stock items</p>
            </div>
            <i class="pi pi-box text-3xl text-purple-200 dark:text-purple-400"></i>
          </div>
        </template>
      </Card>

      <Card class="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900 dark:to-orange-800">
        <template #content>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-600 dark:text-gray-300 text-sm font-semibold mb-2">Active Customers</p>
              <p class="text-3xl font-bold text-orange-600 dark:text-orange-300">{{ activeCustomers }}</p>
              <p class="text-green-600 text-xs mt-2">+5 new this month</p>
            </div>
            <i class="pi pi-users text-3xl text-orange-200 dark:text-orange-400"></i>
          </div>
        </template>
      </Card>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Sales Revenue Chart -->
      <Card class="lg:col-span-2">
        <template #header>
          <div class="flex items-center justify-between p-4">
            <h5 class="text-lg font-bold">Sales Revenue Trend</h5>
            <div class="flex gap-2">
              <Button icon="pi pi-download" severity="secondary" text size="small" />
            </div>
          </div>
        </template>
        <template #content>
          <Chart type="line" :data="chartDataSalesRevenue" :options="chartOptionsSalesRevenue" class="h-[20rem]" />
        </template>
      </Card>

      <!-- Order Status Distribution -->
      <Card>
        <template #header>
          <div class="flex items-center justify-between p-4">
            <h5 class="text-lg font-bold">Order Status</h5>
          </div>
        </template>
        <template #content>
          <Chart type="doughnut" :data="chartDataOrderStatus" :options="chartOptionsOrderStatus" class="h-[20rem]" />
        </template>
      </Card>
    </div>

    <!-- Top Products & Stock Levels -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Top Selling Products -->
      <Card>
        <template #header>
          <div class="flex items-center justify-between p-4">
            <h5 class="text-lg font-bold">Top Selling Products</h5>
            <Button icon="pi pi-arrow-right" severity="secondary" text size="small" />
          </div>
        </template>
        <template #content>
          <DataTable :value="topProducts" :rows="5" striped-rows>
            <Column field="name" header="Product Name"></Column>
            <Column field="sales" header="Sales">
              <template #body="slotProps">
                <Tag :value="`${slotProps.data.sales} units`" severity="info"></Tag>
              </template>
            </Column>
            <Column field="revenue" header="Revenue">
              <template #body="slotProps">
                <span class="font-semibold text-green-600">{{ slotProps.data.revenue }}</span>
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>

      <!-- Stock Level Overview -->
      <Card>
        <template #header>
          <div class="flex items-center justify-between p-4">
            <h5 class="text-lg font-bold">Stock Levels by Category</h5>
            <Button icon="pi pi-arrow-right" severity="secondary" text size="small" />
          </div>
        </template>
        <template #content>
          <Chart type="bar" :data="chartDataStockByCategory" :options="chartOptionsStockByCategory" class="h-[15rem]" />
        </template>
      </Card>
    </div>

    <!-- Monthly Performance & Orders by Customer -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Orders by Month -->
      <Card>
        <template #header>
          <div class="flex items-center justify-between p-4">
            <h5 class="text-lg font-bold">Orders by Month</h5>
          </div>
        </template>
        <template #content>
          <Chart type="bar" :data="chartDataOrdersByMonth" :options="chartOptionsOrdersByMonth" class="h-[15rem]" />
        </template>
      </Card>

      <!-- Category Performance -->
      <Card>
        <template #header>
          <div class="flex items-center justify-between p-4">
            <h5 class="text-lg font-bold">Sales by Category</h5>
          </div>
        </template>
        <template #content>
          <Chart type="pie" :data="chartDataCategoryPerformance" :options="chartOptionsCategoryPerformance" class="h-[15rem]" />
        </template>
      </Card>
    </div>

    <!-- Recent Orders Table -->
    <Card>
      <template #header>
        <div class="flex items-center justify-between p-4">
          <h5 class="text-lg font-bold">Recent Orders</h5>
          <Button label="View All" icon="pi pi-arrow-right" severity="secondary" text size="small" />
        </div>
      </template>
      <template #content>
        <DataTable :value="recentOrders" :rows="10" striped-rows class="p-datatable-sm">
          <Column field="orderNumber" header="Order #" style="width: 10%"></Column>
          <Column field="customer" header="Customer" style="width: 20%"></Column>
          <Column field="orderDate" header="Date" style="width: 15%">
            <template #body="slotProps">
              {{ formatDate(slotProps.data.orderDate) }}
            </template>
          </Column>
          <Column field="total" header="Total" style="width: 15%">
            <template #body="slotProps">
              <span class="font-semibold text-green-600">${{ slotProps.data.total }}</span>
            </template>
          </Column>
          <Column field="status" header="Status" style="width: 15%">
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)"></Tag>
            </template>
          </Column>
          <Column header="Action" style="width: 10%">
            <template #body>
              <Button icon="pi pi-eye" severity="info" text rounded size="small" />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';

definePageMeta({
    // middleware: 'auth',
    layout: 'dashboard'
});

// KPI Data
const totalSales = ref('$125,430');
const totalOrders = ref('342');
const productsInStock = ref('1,245');
const activeCustomers = ref('847');

// Recent Orders Mock Data
const recentOrders = ref([
    { orderNumber: 'ORD-001', customer: 'John Doe', orderDate: '2024-07-18', total: '2,500', status: 'delivered' },
    { orderNumber: 'ORD-002', customer: 'Jane Smith', orderDate: '2024-07-17', total: '1,850', status: 'shipped' },
    { orderNumber: 'ORD-003', customer: 'Mike Johnson', orderDate: '2024-07-16', total: '3,200', status: 'confirmed' },
    { orderNumber: 'ORD-004', customer: 'Sarah Williams', orderDate: '2024-07-15', total: '950', status: 'pending' },
    { orderNumber: 'ORD-005', customer: 'Tom Brown', orderDate: '2024-07-14', total: '2,100', status: 'delivered' },
    { orderNumber: 'ORD-006', customer: 'Lisa Garcia', orderDate: '2024-07-13', total: '1,750', status: 'shipped' },
    { orderNumber: 'ORD-007', customer: 'David Lee', orderDate: '2024-07-12', total: '2,850', status: 'delivered' },
    { orderNumber: 'ORD-008', customer: 'Emma Davis', orderDate: '2024-07-11', total: '1,200', status: 'confirmed' },
]);

// Top Products Mock Data
const topProducts = ref([
    { name: 'Premium Coffee Beans', sales: 450, revenue: '$18,000' },
    { name: 'Organic Tea Mix', sales: 320, revenue: '$12,800' },
    { name: 'Dark Chocolate Bar', sales: 285, revenue: '$14,250' },
    { name: 'Honey Jar (1kg)', sales: 210, revenue: '$10,500' },
    { name: 'Almond Butter', sales: 180, revenue: '$9,000' },
]);

// Chart Data - Sales Revenue Trend
const chartDataSalesRevenue = ref();
const chartOptionsSalesRevenue = ref();

const setChartDataSalesRevenue = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    return {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
            {
                label: 'Monthly Revenue',
                borderColor: documentStyle.getPropertyValue('--p-blue-500'),
                backgroundColor: documentStyle.getPropertyValue('--p-blue-100'),
                fill: true,
                tension: 0.4,
                data: [28000, 32000, 35000, 31000, 42000, 48000, 52000, 49000, 55000, 58000, 61000, 65000]
            }
        ]
    };
};

const setChartOptionsSalesRevenue = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
    const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

    return {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: textColor }
            }
        },
        scales: {
            x: {
                ticks: { color: textColorSecondary },
                grid: { color: surfaceBorder }
            },
            y: {
                ticks: { color: textColorSecondary },
                grid: { color: surfaceBorder }
            }
        }
    };
};

// Chart Data - Order Status
const chartDataOrderStatus = ref();
const chartOptionsOrderStatus = ref();

const setChartDataOrderStatus = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    return {
        labels: ['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled'],
        datasets: [
            {
                data: [12, 25, 35, 250, 8],
                backgroundColor: [
                    documentStyle.getPropertyValue('--p-yellow-500'),
                    documentStyle.getPropertyValue('--p-blue-500'),
                    documentStyle.getPropertyValue('--p-purple-500'),
                    documentStyle.getPropertyValue('--p-green-500'),
                    documentStyle.getPropertyValue('--p-red-500')
                ]
            }
        ]
    };
};

const setChartOptionsOrderStatus = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    return {
        plugins: {
            legend: {
                labels: { color: textColor }
            }
        }
    };
};

// Chart Data - Stock by Category
const chartDataStockByCategory = ref();
const chartOptionsStockByCategory = ref();

const setChartDataStockByCategory = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    return {
        labels: ['Beverages', 'Snacks', 'Dairy', 'Bakery', 'Frozen'],
        datasets: [
            {
                label: 'Stock Quantity',
                backgroundColor: documentStyle.getPropertyValue('--p-purple-500'),
                data: [320, 245, 180, 150, 200]
            }
        ]
    };
};

const setChartOptionsStockByCategory = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
    const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

    return {
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
            legend: {
                labels: { color: textColor }
            }
        },
        scales: {
            x: {
                ticks: { color: textColorSecondary },
                grid: { color: surfaceBorder }
            },
            y: {
                ticks: { color: textColorSecondary },
                grid: { color: surfaceBorder }
            }
        }
    };
};

// Chart Data - Orders by Month
const chartDataOrdersByMonth = ref();
const chartOptionsOrdersByMonth = ref();

const setChartDataOrdersByMonth = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    return {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
            {
                label: 'Number of Orders',
                backgroundColor: documentStyle.getPropertyValue('--p-green-500'),
                data: [18, 22, 25, 20, 32, 35, 28, 30, 33, 35, 38, 40]
            }
        ]
    };
};

const setChartOptionsOrdersByMonth = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
    const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

    return {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: textColor }
            }
        },
        scales: {
            x: {
                ticks: { color: textColorSecondary },
                grid: { color: surfaceBorder }
            },
            y: {
                ticks: { color: textColorSecondary },
                grid: { color: surfaceBorder }
            }
        }
    };
};

// Chart Data - Category Performance
const chartDataCategoryPerformance = ref();
const chartOptionsCategoryPerformance = ref();

const setChartDataCategoryPerformance = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    return {
        labels: ['Beverages', 'Snacks', 'Dairy', 'Bakery', 'Frozen'],
        datasets: [
            {
                data: [28000, 22000, 18000, 15000, 16000],
                backgroundColor: [
                    documentStyle.getPropertyValue('--p-orange-500'),
                    documentStyle.getPropertyValue('--p-cyan-500'),
                    documentStyle.getPropertyValue('--p-pink-500'),
                    documentStyle.getPropertyValue('--p-indigo-500'),
                    documentStyle.getPropertyValue('--p-teal-500')
                ]
            }
        ]
    };
};

const setChartOptionsCategoryPerformance = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    return {
        plugins: {
            legend: {
                labels: { color: textColor }
            }
        }
    };
};

// Format Date Helper
const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

// Get Status Severity
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

onMounted(() => {
    chartDataSalesRevenue.value = setChartDataSalesRevenue();
    chartOptionsSalesRevenue.value = setChartOptionsSalesRevenue();
    chartDataOrderStatus.value = setChartDataOrderStatus();
    chartOptionsOrderStatus.value = setChartOptionsOrderStatus();
    chartDataStockByCategory.value = setChartDataStockByCategory();
    chartOptionsStockByCategory.value = setChartOptionsStockByCategory();
    chartDataOrdersByMonth.value = setChartDataOrdersByMonth();
    chartOptionsOrdersByMonth.value = setChartOptionsOrdersByMonth();
    chartDataCategoryPerformance.value = setChartDataCategoryPerformance();
    chartOptionsCategoryPerformance.value = setChartOptionsCategoryPerformance();
});
</script>