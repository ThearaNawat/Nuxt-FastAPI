<script setup lang="ts">
type BackendMenuNode = {
  id?: number
  label: string
  path?: string | null
  icon?: string | null
  badge?: number | null
  parent_id?: number | null
  display_order?: number | null
  type?: string | null
  is_active?: boolean | null
  children?: BackendMenuNode[]
}

type PanelMenuItem = {
  label: string
  icon?: string
  badge?: string
  path: string
  command?: () => void
  items?: PanelMenuItem[]
}
import type { User, MenuNode } from "~~/store/state"
import { useAuthStore } from "~~/store/state";
import { useRouter } from "vue-router";
import { computed } from "vue";
const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
const emit = defineEmits(['logout'])

const iconAliases: Record<string, string> = {
  LayoutDashboard: 'pi pi-home',
  Package: 'pi pi-box',
  Box: 'pi pi-box',
  Tag: 'pi pi-tag',
  BarChart3: 'pi pi-chart-bar',
  ArrowRightLeft: 'pi pi-arrows-h',
  ShoppingCart: 'pi pi-shopping-cart',
  FileText: 'pi pi-file',
  Users: 'pi pi-users',
  Shield: 'pi pi-shield',
  Lock: 'pi pi-lock',
  Settings: 'pi pi-cog',
  MicrochipAi: 'pi pi-microchip-ai',
  Briefcase: 'pi pi-briefcase',
  Slack: 'pi pi-slack',
  Warehouse: 'pi pi-warehouse',
  Receipt: 'pi pi-receipt',
  Comment: 'pi pi-comment',
}



const resolveIcon = (icon?: string | null) => {
  if (!icon) {
    return undefined
  }

  if (icon.startsWith('pi ')) {
    return icon
  }

  if (icon.startsWith('pi-')) {
    return `pi ${icon}`
  }

  return iconAliases[icon] ?? undefined
}



const buildMenuModel = (nodes: MenuNode[] = []): PanelMenuItem[] => {
  return nodes.reduce<PanelMenuItem[]>((items, node) => {
    const children = buildMenuModel(Array.isArray(node.children) ? node.children : [])

    const menuItem: PanelMenuItem = {
      label: node.label,
      icon: resolveIcon(node.icon),
      items: children.length ? children : [],
      path: node.path as string,
    }

    items.push(menuItem)
    return items
  }, [])
}


const remoteMenu = computed(() => buildMenuModel(auth.getMenu as MenuNode[]))
const user = computed(() => auth.getUser as User)

async function logout() {
  emit('logout')
}
</script>

<template>
  <Card class="w-72 h-screen overflow-y-auto border-r flex flex-col" style="border-radius: 0;">
    <template #title>
      <div class="flex items-center justify-center">
        <Avatar
          shape="circle"
          size="xlarge"
        >

        </Avatar>
      </div>
      <div class="flex items-center px-6">

        <Button 
          icon="pi pi-spin pi-envelope"
          variant="link"
          size="small"
        >
        </Button>
        <span class="font-bold text-sm text-[#334155]">{{ user?.email }}</span>
      </div>
      <Divider></Divider>
    </template>

    <template #content>
      <div class="flex-1 overflow-y-auto py-4 space-y-2">
        <PanelMenu
          :model="remoteMenu"
        >
          <template #item="{ item }">
            <router-link v-if="item.path" v-slot="{ href, navigate }" :to="item.path" custom>
              <a v-ripple class="flex items-center px-4 cursor-pointer group" :href="href" @click="navigate">
                <Button :icon="item.icon" :class="item.icon ? '' : 'mr-3'" size="small" variant="link" />
                <span 
                  :class="['ml-2', { 'font-semibold': item.items }]" 
                >
                  {{ t(item.label?.toString().toLocaleLowerCase() as string) }}
                </span>
                <Badge v-if="item?.items?.length" class="ml-auto" :value="item?.items?.length" />
              </a>
            </router-link>
            <a v-else v-ripple class="flex items-center px-4 cursor-pointer group">
                <Button :icon="item.icon" :class="item.icon ? '' : 'mr-3'" size="small" variant="link" />
                <span 
                  :class="['ml-2', { 'font-semibold': item.items }]" 
                >
                  {{ t(item.label?.toString().toLocaleLowerCase() as string) }}
                </span>
                <Badge v-if="item?.items?.length" class="ml-auto" :value="item?.items?.length" />
            </a>
          </template>
        </PanelMenu>
          
      </div>
    </template>

    <template #footer>
      <Button
        class="w-full"
        :label="t('btnLogout')"
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
