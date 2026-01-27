export const parseStringDate = (value: string | null)=> {
        if (!value) return null

        const [day, month, year] = value.split('/')
        var date = new Date(Number(year), Number(month) - 1, Number(day))
        return date
    }
export const formatDate = (value: Date) => {
    if (!value) return ''
    return value.toLocaleDateString('en-US', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}