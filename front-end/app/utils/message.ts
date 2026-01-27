export const Success = (detail: string) => ({
  severity: 'success',
  summary: 'Success',
  detail,
  life: 2500
})

export const ErrorBox = (detail: string) => ({
  severity: 'error',
  summary: 'Error',
  detail,
  life: 3500
})

export const Warn = (detail: string) => ({
  severity: 'warn',
  summary: 'Warning',
  detail,
  life: 3000
})