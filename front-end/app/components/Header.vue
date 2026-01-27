<template>
    <Menubar style="border-radius: 0;">
        <template #start>
          <div class="flex items-center gap-3">
            
            <button
              class="text-gray-600 hover:text-gray-900"
              @click="openSideBar = !openSideBar"
            >
              <i class="pi pi-bars text-lg"></i>
            </button>
          </div>
        </template>

        <template #end>
            <div class="md:flex items-center w-1/3">
              <IconField >
                  <InputIcon class="pi pi-search" />
                  <InputText placeholder="Search" />
              </IconField>
              <div class="flex items-center ml-3">
                <!-- <i class="pi pi-globe" @click="toggler" style="font-size: 1.4rem;color: green; cursor: pointer;" /> -->
                <Button size="large" icon="pi pi-globe" @click="toggler" variant="link"></Button>
                <!-- <OverlayBadge value="1" size="small">
                  <i class="pi pi-bell" style="font-size: 1.4rem;color: green; cursor: pointer;" />
                   <Button size="large" icon="pi pi-bell" variant="link"></Button>
                </OverlayBadge> -->
                  <!-- <i :class="theme !== 'dark' ? 'pi pi-sun' : 'pi pi-moon'" style="font-size: 1.4rem;color: green; cursor: pointer;" @click="toggle"/> -->
                  <Button size="large" @click="toggle" :icon="theme !== 'dark' ? 'pi pi-sun' : 'pi pi-moon'" variant="link"></Button>
                  <ComponentColorPicker />
                  <!-- <i class="pi pi-cog pi-spin" style="font-size: 1.4rem;color: green; cursor: pointer;" /> -->
                  <Button size="large" icon="pi pi-cog pi-spin" variant="link"></Button>
              </div>
            </div>

            <Popover ref="op" :dismissable="true">
              <div class="flex flex-col gap-4">
                  <Button @click="hideButton('en')" label="English" size="small" variant="text"></Button>
                  <Button @click="hideButton('kh')" label="Khmer" size="small" variant="text"></Button>
              </div>
            </Popover>
        </template>
        
      </Menubar>
</template>
<script setup lang="ts">
    import type Popover from 'primevue/popover'
    import ComponentColorPicker from './ComponentColorPicker.vue'
    const props = defineProps({ openSideBar: Boolean})
    const { theme, toggle } = useTheme()
    const $i18n = useI18n()
    const op = ref<InstanceType<typeof Popover> | null>(null)
    const toggler = (event: Event) => {
      op.value?.toggle(event);
    }
    const hideButton = (lang: string) => {
      op.value?.hide()
      if(lang === 'en') 
        $i18n.setLocale('en')
      else
        $i18n.setLocale('kh') 
    }
</script>