
export const Success = (detail: string, t: any) => ({
  severity: 'success',
  summary: t('success'),
  detail,
  life: 2500
})

export const ErrorBox = (detail: string, t: any) => ({
  severity: 'error',
  summary: t('error'),
  detail,
  life: 3500
})

export const Warn = (detail: string, t: any) => ({
  severity: 'warn',
  summary: t('warning'),
  detail,
  life: 3000
})