<template>
  <div class="min-h-screen bg-white text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <Toast />
    <ConfirmDialog />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
<script setup lang="ts">
  const { init } = useTheme()
  onMounted(init)
</script>

<style>
  body{
    font-family:"Battambang", system-ui, sans-serif;
  }
</style>
