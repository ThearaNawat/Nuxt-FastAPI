
export const MessageBox = () => {
    const toast = useToast()

    return{
        success: (msg: string) => toast.add(Success(msg)),
        error: (msg: string) => toast.add(ErrorBox(msg)),
        warning: (msg: string) => toast.add(Warn(msg)),
    }
}