type ConfirmDeleteOptions = {
    message?: string
    header?: string
    acceptLabel?: string
    rejectLabel?: string
}

export const useConfirmDelete = () =>{
    const confirm = useConfirm()
    const confirmDelete = ( onAccept: ()=> void | Promise<void>, options?: ConfirmDeleteOptions) =>{
        confirm.require({
            acceptIcon: 'pi pi-check',
            rejectIcon: 'pi pi-times',
            message: options?.message || 'Are you sure you want to delete?',
            header: options?.header || 'Confirm Delete',
            icon: 'pi pi-exclamation-triangle text-red-500',
            acceptLabel: options?.acceptLabel || 'Delete',
            rejectLabel: options?.rejectLabel || 'Cancel',
            acceptClass: 'p-button-danger',
            
            accept: async () => {
                await onAccept()
            }
        })
    }

    return { confirmDelete }
}