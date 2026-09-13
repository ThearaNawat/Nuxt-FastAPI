import type { Customer, CustomerErrors } from "~~/shared/types/customer"
import { CustomerService } from '~/services/customer.service'
export const useCustomer = () => {
    const { t } = useI18n()
    const customers = ref<Customer[]>([]);
    const customer = ref<Customer | null>(null);
    const loading = ref(false);
    const btnLoading = ref(false)
    const editMode = ref(false)
    const openDialog = ref(false)
    const { confirmDelete } = useConfirmDelete()
    const errors = ref<CustomerErrors>(CustomerService.customerError());
    const messageBox = MessageBox()
    const selectCustomers = ref<any[]>([])
    const customerForm = reactive<Customer>({ id: 0, customer_code: '', customer_name: '', phone_number: '', email: '', payment_terms: '', credit_limit: 0, billing_address: '', shipping_address: ''})
    const onOpenDialogEdit = (item: any, canUpdate: boolean) => {
        if(canUpdate){
            editMode.value = true
            customerForm.id = item.data.id
            customerForm.billing_address = item.data.billing_address
            customerForm.email = item.data.email
            customerForm.contact_person = item.data.contact_person
            customerForm.credit_limit = item.data.credit_limit
            customerForm.customer_code = item.data.customer_code
            customerForm.customer_name = item.data.customer_name
            customerForm.phone_number = item.data.phone_number
            customerForm.payment_terms = item.data.payment_terms
            customerForm.shipping_address = item.data.shipping_address
            openDialog.value = true
        }
    }
    const close = () => {
        customerForm.billing_address = '',
        customerForm.contact_person = '',
        customerForm.credit_limit = 0,
        customerForm.customer_code = '',
        customerForm.customer_name = '',
        customerForm.email = '',
        customerForm.id = 0,
        customerForm.payment_terms = '',
        customerForm.phone_number = '',
        customerForm.shipping_address = ''
        errors.value = CustomerService.customerError()
        openDialog.value = false
        editMode.value = false
    }
    const fetchCustomers = async () => {
        loading.value = true;
        await CustomerService.getAllCustomer()
        .then((res) => {
            customers.value = res
            loading.value = false    
        })
        .catch((error) => {
            loading.value = false
        })
        
    };

    const createCustomer = async (data: Customer) => {
        loading.value = true;
        btnLoading.value = true
        await CustomerService.createCustomer(data)
        .then((res) => {
            loading.value = false
            btnLoading.value = false
            fetchCustomers()
            close()
            messageBox.success(t('successMessage'))
        })
        .catch((error) => {
            errors.value = CustomerService.applyUserValidationErrors(error?.data?.data?.detail, errors.value)
            
            loading.value = false
            btnLoading.value = false
            if (!errors.value) messageBox.error(t('errorMessage'))
        })
    };

    const updateCustomer = async (id: number, data: Customer) => {
        loading.value = true;
        btnLoading.value = true
        await CustomerService.updateCustomer(id, data)
        .then((res) => {
            fetchCustomers()
            messageBox.success(t('successMessage'))
            close()
            loading.value = false
            btnLoading.value = false
        })
        .catch((error) => {
            loading.value = false
            btnLoading.value = false
            errors.value = CustomerService.applyUserValidationErrors(error?.data?.data?.detail, errors.value)
            if(!errors.value)
                messageBox.error(t('errorMessage'))
        })
    };

    const deleteMany = () =>{
        if(!selectCustomers.value.length) return

        confirmDelete(
            async () => {
                loading.value = true
                const customerIds = selectCustomers.value.map((e: any) => e.id)
                await CustomerService.deleteCustomer(customerIds)
                .then((res) => {
                    fetchCustomers()
                    messageBox.success(t('successMessage'))
                    loading.value = false
                })
                .catch((error: any) => {
                    loading.value = false
                    messageBox.error(t('errorMessage'))
                })
            }
        )
    }

    return {
        customers,
        customer,
        loading,
        errors,
        btnLoading,
        customerForm,
        fetchCustomers,
        createCustomer,
        updateCustomer,
        close,
        openDialog,
        onOpenDialogEdit,
        editMode,
        selectCustomers,
        deleteMany
    };
}