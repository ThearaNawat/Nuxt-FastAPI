export const parseStringDate = (value: string | null)=> {
        if (!value) return null

        const [day, month, year] = value.split('/')
        var date = new Date(Number(year), Number(month) - 1, Number(day))
        return date
    }
export const formatDate = (value: string | Date | null) => {
  if (!value) return ''
  const date = value instanceof Date ? value : parseDate(value)
  if (!date || Number.isNaN(date.getTime())) return ''

  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

export const parseDate = (value: string | Date | null) => {
  if (!value) return null
  if (value instanceof Date) return value

  let normalized = value
  if (normalized.indexOf('-') > 0) {
    normalized = normalized.replaceAll('-', '/')
  }

  const [year, month, day] = normalized.split('/')
  if (year && month && day) {
    return new Date(Number(year), Number(month) - 1, Number(day.substring(0, 2)))
  }

  return new Date(normalized)
}