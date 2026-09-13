type ConfirmDeleteOptions = {
    message?: string
    header?: string
    acceptLabel?: string
    rejectLabel?: string
}

export const useConfirmDelete = () =>{
    const confirm = useConfirm()
    const { t } = useI18n()
    const confirmDelete = ( onAccept: ()=> void | Promise<void>, options?: ConfirmDeleteOptions) =>{
        confirm.require({
            acceptIcon: 'pi pi-check',
            rejectIcon: 'pi pi-times',
            message: options?.message || t('confirmDeleteMessage'),
            header: options?.header || t('confirmDeleteHeader'),
            icon: 'pi pi-exclamation-triangle text-red-500',
            acceptLabel: options?.acceptLabel || t('btnDelete'),
            rejectLabel: options?.rejectLabel || t('btnCancel'),
            acceptClass: 'p-button-danger',
            
            accept: async () => {
                await onAccept()
            }
        })
    }

    return { confirmDelete }
}