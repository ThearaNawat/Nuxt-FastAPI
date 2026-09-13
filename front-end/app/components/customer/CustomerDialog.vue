<template>
    <div>
        <Dialog
            style="width: 500px;"
            :visible="openDialog"
            :closable="false"
        >
            
            <template #header>
                <Divider>
                    <Button icon="pi pi-user" size="large" variant="link"></Button>
                    <span v-if="!editMode" class="text-xl">{{ t('lblHeaderCreate').replace('[0]', t('customer')) }}</span>
                    <span v-else class="text-xl">{{ t('lblHeaderUpdate').replace('[0]', t('customer')) }}</span>
                </Divider>
            </template> 
            
            <template #default>

                
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="customerForm.customer_code"
                        >
                            
                        </InputText>
                        <label>{{ t('lblCode') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.customer_code">{{ errors.customer_code }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="customerForm.customer_name"
                        >
                            
                        </InputText>
                        <label>{{ t('lblName') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.customer_name">{{ errors.customer_name }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-phone" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputMask
                            mask="999-999-9999"
                            v-model="customerForm.phone_number"
                        >
                            
                        </InputMask>
                        <label>{{ t('lblPhone') }} </label>
                    </FloatLabel>
                </InputGroup>
                <!-- <Message severity="error" variant="simple" size="small" v-if="errors.package">{{ errors.package }}</Message> -->
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-envelope" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="customerForm.email"
                        >
                        </InputText>
                        <label>{{ t('email') }} </label>
                    </FloatLabel>
                </InputGroup>
                <!-- <Message severity="error" variant="simple" size="small" v-if="errors.phone">{{ errors.phone }}</Message> -->
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="customerForm.contact_person"
                        >
                        </InputText>
                        <label>{{ t('contact') }} </label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputNumber
                            v-model="customerForm.credit_limit"
                            mode="decimal"
                            currency="USD"
                        >
                        </InputNumber>
                        <label>{{ t('credit_limit') }} </label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="customerForm.payment_terms"
                        >
                        </InputText>
                        <label>{{ t('payment_term') }} </label>
                    </FloatLabel>
                </InputGroup>
                
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-slack" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            class="w-full"
                            v-model="customerForm.shipping_address"
                        >
                            
                        </Textarea>
                        <label>{{ t('lblAddress') }}</label>
                    </FloatLabel>
                </InputGroup>
                <!-- <Message severity="error" variant="simple" size="small" v-if="errors.category_id">{{ errors.category_id }}</Message> -->
                <InputGroup class="my-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-pencil" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            class="w-full"
                            v-model="customerForm.billing_address"
                        >
                            
                        </Textarea>
                        <label>{{ t('lblAddress') }}</label>
                    </FloatLabel>
                </InputGroup>
                <Checkbox binary class="mr-2">{{ t('active') }}</Checkbox>
                <label>{{t('active')}}</label>
            </template>
            <template #footer>
                <Button icon="pi pi-check" class="mt-2" :loading="btnLoading" :label="t('btnSave')" size="small" type="submit" @click="handleSubmit"></Button>
                <Button icon="pi pi-times" class="mt-2" :label="t('btnCancel')" @click="closeDialog" size="small"></Button>
            </template>
        </Dialog>
    </div>
</template>
<script setup lang="ts">
    import type { Customer, CustomerErrors } from '~~/shared/types/customer'
    interface Prop {
        openDialog: boolean 
        editMode: boolean
        btnLoading: boolean
        customerForm: Customer
        errors: CustomerErrors
    }
    const { t } = useI18n()
    const props = defineProps<Prop>()
    
    const emits = defineEmits(['closeDialog', 'handleSubmit'])
    const closeDialog = () => emits('closeDialog')
    const handleSubmit = () => emits('handleSubmit')
</script>