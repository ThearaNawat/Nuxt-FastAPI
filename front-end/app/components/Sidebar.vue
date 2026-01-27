<script setup lang="ts">
const router = useRouter();
const menu = [
  {
    label: "Product",
    icon: "pi pi-briefcase",
    command: () => router.push("/product"),
  },
  {
    label: "Category",
    icon: "pi pi-slack",
    command: () => router.push("/category"),
  },
  {
    label: "Supplier",
    icon: "pi pi-users",
    command: () => router.push("/supplier"),
  },
  {
    label: "Stock",
    icon: "pi pi-warehouse",
    command: () => router.push("/stock"),
  },
  {
    label: "Order",
    icon: "pi pi-receipt",
    command: () => router.push("/order"),
  },
  {
    label: "Bot",
    icon: "pi pi-microchip-ai",
    items:[
      {
        label: "Line Bot",
        icon: "pi pi-comment",
        command: () => router.push("/line-bot"),
      },
    ]
  }
];

const uiKit = [
  {
    label: "User",
    icon: "pi pi-user",
    command: () => router.push("/user"),
  },
  {
    label: "Role",
    icon: "pi pi-wrench",
    command: () => router.push("/"),
  },
  
];
const emit = defineEmits(['logout'])

async function logout(){
  emit('logout')
}
</script>

<template>
  <Card class="w-72 h-screen border-r flex flex-col" style="border-radius: 0;">
    <!-- Brand -->
    <template #title>
      <div class="flex items-center gap-3 px-6">
        <i class="pi pi-spin pi-bolt text-green-600 text-4xl"></i>
        <span class="font-bold text-lg text-[#334155]">ULTIMA</span>
      </div>
      <Divider></Divider>
    </template>

    <!-- Menu -->
    <template #content>
      <div class="flex-1 overflow-y-auto  py-4 space-y-2">
      <PanelMenu
        :model="menu"
        class="ultima-menu"
      />

      <!-- Section -->
      <div class="px-2 text-xs font-semibold text-slate-400 uppercase">
        Setting
      </div>

      <PanelMenu
        :model="uiKit"
        class="ultima-menu"
      />
    </div>
    </template>

    <template #footer>
      <Button 
        class="w-full" 
        label="Logout" 
        icon="pi pi-sign-out" 
        @click="logout"
      >
      </Button>
    </template>
      
  </Card>
</template>

<style>
.ultima-menu {
  border: green;
}

.ultima-menu .p-panelmenu-header-content,
.ultima-menu .p-menuitem-content {
  background: transparent;
}

.ultima-menu .p-panelmenu-header-link,
.ultima-menu .p-menuitem-link {
  color: #334155;
  font-weight: 500;
}

.ultima-menu .p-menuitem-link:hover {
  background: #f1f5f9;
}

.ultima-menu .router-link-active,
.ultima-menu .p-menuitem-link-active {
  background: #eef2ff;
  color: #4338ca;
}

.ultima-menu .p-menuitem-icon {
  color: #64748b;
}
</style>
