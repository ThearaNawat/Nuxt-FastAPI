<script setup lang="ts">
import type Popover from 'primevue/popover'

type PrimaryName = 'green' | 'blue' | 'indigo' | 'emerald' | 'orange' | 'red' |'purple' | 'pink'

const op = ref<InstanceType<typeof Popover> | null>(null)

const primary = useState<PrimaryName>('ui_primary', () => 'indigo')

const COLORS: Record<PrimaryName, { c600: string; c700: string; c500: string }> = {
    green:   { c500: '#22c55e', c600: '#16a34a', c700: '#15803d' },//'#11ba82' 
    blue:    { c500: '#3b82f6', c600: '#2563eb', c700: '#1d4ed8' },
    indigo:  { c500: '#6366f1', c600: '#4f46e5', c700: '#4338ca' },
    emerald: { c500: '#10b981', c600: '#059669', c700: '#047857' },
    orange:  { c500: '#f97316', c600: '#ea580c', c700: '#c2410c' },
    red:     { c500: '#ef4444', c600: '#dc2626', c700: '#b91c1c' },
    purple:  { c500: '#a855f7', c600: '#9333ea', c700: '#7e22ce' },
    pink:    { c500: '#ec4899', c600: '#db2777', c700: '#be185d' },
}

function open(e: Event) {
  op.value?.toggle(e)
}

function applyColor(name: PrimaryName) {
  primary.value = name
  if (import.meta.client) localStorage.setItem('ui_primary', name)

  const p = COLORS[name]
  const root = document.documentElement.style
  root.setProperty('--p-primary-500', p.c500)
  root.setProperty('--p-primary-600', p.c600)
  root.setProperty('--p-primary-700', p.c700)
  root.setProperty('--p-primary-color', p.c600)
  root.setProperty('--p-primary-contrast-color', '#ffffff')

  op.value?.hide()
}

onMounted(() => {
  const saved = (localStorage.getItem('ui_primary') as PrimaryName | null)
  if (saved && COLORS[saved]) applyColor(saved)
})
</script>

<template>
  <!-- <i class="pi pi-palette" @click="open" style="font-size: 1.4rem;color: green; cursor: pointer;"></i> -->
  <Button size="large" icon="pi pi-palette" @click="open" variant="link"></Button>
  <Popover ref="op" :dismissable="true" class="w-[220px]">
    <div class="p-2">
      <div class="text-xs font-semibold text-surface-700 dark:text-surface-200 mb-2">
        Primary color
      </div>

      <div class="flex flex-wrap gap-2">
        <button
          v-for="(v, k) in COLORS"
          :key="k"
          class="w-6 h-6 rounded-full ring-1 ring-surface-200 dark:ring-surface-700"
          :style="{ backgroundColor: v.c600 }"
          @click="applyColor(k as PrimaryName)"
        >
          <span
            v-if="primary === k"
            class="block w-full h-full rounded-full ring-2 ring-white/90"
          />
        </button>
      </div>
    </div>
  </Popover>
</template>
