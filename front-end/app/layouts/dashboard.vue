<template>
  <div class="dashboard flex h-screen w-screen">

    <Sidebar @logout="logout"/>
    <!-- Main -->
    <div class="main flex flex-col flex-1">
      <!-- Header -->
      <Header />
      <!-- Page content -->
      <Card class="content flex-1 p-4 overflow-x-auto" style="border-radius: 0;">
        <template #content><slot /></template>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "~~/store/state";
import Sidebar from "~/components/Sidebar.vue";
import Header from "~/components/Header.vue";
const auth = useAuthStore();
const sidebarOpen = ref(true);
const userMenu = [
  {
    label: "Profile",
    icon: "pi pi-user",
    command: () => navigateTo("/profile"),
  },
  {
    label: "Settings",
    icon: "pi pi-cog",
    command: () => navigateTo("/settings"),
  },
  {
    separator: true,
  },
  {
    label: "Logout",
    icon: "pi pi-sign-out",
    command: logout,
  },
];
const items = ref([
    {
        label: 'Files',
        icon: 'pi pi-file',
        items: [
            {
                label: 'Documents',
                icon: 'pi pi-file',
                items: [
                    {
                        label: 'Invoices',
                        icon: 'pi pi-file-pdf',
                        items: [
                            {
                                label: 'Pending',
                                icon: 'pi pi-stop'
                                
                            },
                            {
                                label: 'Paid',
                                icon: 'pi pi-check-circle'
                            }
                        ]
                    },
                    {
                        label: 'Clients',
                        icon: 'pi pi-users'
                    }
                ]
            },
            {
                label: 'Images',
                icon: 'pi pi-image',
                items: [
                    {
                        label: 'Logos',
                        icon: 'pi pi-image'
                    }
                ]
            }
        ]
    },
    {
        label: 'Cloud',
        icon: 'pi pi-cloud',
        items: [
            {
                label: 'Upload',
                icon: 'pi pi-cloud-upload'
            },
            {
                label: 'Download',
                icon: 'pi pi-cloud-download'
            },
            {
                label: 'Sync',
                icon: 'pi pi-refresh'
            }
        ]
    },
    {
        label: 'Devices',
        icon: 'pi pi-desktop',
        items: [
            {
                label: 'Phone',
                icon: 'pi pi-mobile'
            },
            {
                label: 'Desktop',
                icon: 'pi pi-desktop'
            },
            {
                label: 'Tablet',
                icon: 'pi pi-tablet'
            }
        ]
    }
])

async function logout() {
  await auth.logout()
  .then(() => {navigateTo('/login')});
}
</script>
