<template>
  <div class="flex h-screen w-screen">

    <Sidebar @logout="logout"/>
    <!-- Main -->
    <div class="main flex flex-col flex-1">
      <!-- Header -->
      <Header />
      <!-- Page content -->
      <Card class="content flex-1 p-4 overflow-auto" style="border-radius: 0;">
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

async function logout() {
  await auth.logout()
  .then(() => {navigateTo('/login')});
}
</script>
