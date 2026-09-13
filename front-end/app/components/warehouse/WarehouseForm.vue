<template>
    <div id="warehouse-dialog">

        <Dialog
            style="width: 500px;"
            :visible="openDialog"
            :closable="false"
        >
            
            <template #header>
                <Divider>
                    <Button icon="pi pi-user" size="large" variant="link"></Button>
                    <span v-if="!editMode" class="text-xl">{{ t('lblHeaderCreate').replace('[0]', t('warehouse')) }}</span>
                    <span v-else class="text-xl">{{ t('lblHeaderUpdate').replace('[0]', t('warehouse')) }}</span>
                </Divider>
            </template> 
            
            <template #default>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-warehouse" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="warehouseForm.warehouse_name"
                        >
                            
                        </InputText>
                        <label>{{ t('lblName') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.warehouse_name">{{ errors.warehouse_name }}</Message>
                
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-envelope" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="warehouseForm.postal_code"
                        >
                        </InputText>
                        <label>{{ t('postal_code') }} </label>
                    </FloatLabel>
                </InputGroup>
                <!-- <Message severity="error" variant="simple" size="small" v-if="errors.phone">{{ errors.phone }}</Message> -->
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="warehouseForm.state"
                        >
                        </InputText>
                        <label>{{ t('state') }} </label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="warehouseForm.city"
                        >
                        </InputText>
                        <label>{{ t('city') }} </label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="warehouseForm.country"
                        >
                        </InputText>
                        <label>{{ t('country') }} </label>
                    </FloatLabel>
                </InputGroup>
                
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-slack" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            class="w-full"
                            v-model="warehouseForm.address"
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
    const { t } = useI18n()
    const props = defineProps<{
        openDialog: boolean,
        editMode: boolean,
        warehouseForm: Warehouse,
        errors: WarehouseError,
        btnLoading: boolean
    }>()
    const emit = defineEmits<{
        (e: 'closeDialog'): void,
        (e: 'handleSubmit'): void
    }>()
    const closeDialog = () => emit('closeDialog')
    const handleSubmit = () => emit('handleSubmit')

</script>