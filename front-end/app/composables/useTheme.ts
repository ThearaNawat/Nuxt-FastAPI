export const useTheme = () => {
  const theme = useState<'light' | 'dark'>('theme', () => 'light')

  const apply = (mode: 'light' | 'dark') => {
    theme.value = mode
    if (import.meta.client) {
      document.documentElement.classList.toggle('dark', mode === 'dark')
      localStorage.setItem('theme', mode)
    }
  }

  const toggle = () => apply(theme.value === 'dark' ? 'light' : 'dark')

  const init = () => {
    if (!import.meta.client) return
    const saved = localStorage.getItem('theme') as 'light' | 'dark' | null
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    apply(saved ?? (prefersDark ? 'dark' : 'light'))
  }

  return { theme, init, toggle, apply }
}
