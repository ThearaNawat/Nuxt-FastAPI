
export const MessageBox = () => {
    const toast = useToast()
    const { t } = useI18n()
    return{
        success: (msg: string) => toast.add(Success(msg, t)),
        error: (msg: string) => toast.add(ErrorBox(msg, t)),
        warning: (msg: string) => toast.add(Warn(msg, t)),
    }
}