<template>
    <div id="supplier">
        <DataTable
            paginator 
            :rows="20" 
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            removable-sort
            resizable-columns
            reorderable-columns
            :value="supplierList"
            :lazy="loading"
            size="small"
            striped-rows
            v-model:selection="selectSupplier"
            v-model:filters="filters"
            :global-filter-fields="['name', 'description', 'code', 'email', 'phone', 'address']"
            filter-display="menu"
            data-key="id"
            row-hover
            @row-dblclick="onOpenDialogEdit"
            scrollable
            scroll-height="500px"
            style="max-width: 1310px;"
        >
            <Toolbar>
                <template #end>
                    <Button :label="t('btnCreate')" icon="pi pi-plus" class="" @click="openDialog = true"></Button>
                    <Button :label="t('btnDelete')" icon="pi pi-trash" class="ml-2" @click="deleteMany"></Button>
                </template>
            </Toolbar>
            <template #header>
                <div class="flex justify-between">
                    <IconField >
                        <InputIcon>
                            <i class="pi pi-search"></i>
                        </InputIcon>
                        <InputText :placeholder="t('search')" v-model="filters['global'].value"></InputText>
                    </IconField>
                    <Button icon="pi pi-filter-slash" @click="clearFilter" variant="link"></Button>
                </div>
            </template>
            <Column selection-mode="multiple"  header-style="width: 2rem"></Column>
            <Column :header="t('lblCode')" field="code" sortable>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" placeholder="Search by code" />
                </template>
            </Column>
            <Column :header="t('lblName')" sortable field="name" >
                <template #filter = "{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>
            <Column :header="t('email')" sortable field="email" class="text-purple-900">
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
                <template #body ="{data}">
                    <Button icon="pi pi-envelope" variant="link"></Button>
                    {{ data.email }}
                </template>
            </Column>
            <Column :header="t('lblPhone')" sortable field="phone" class="text-blue-700">
                <template #filter = "{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
                <template #body = "{ data }">
                    <Button icon="pi pi-phone" size="small" variant="link"></Button>
                    {{ data.phone }}
                </template>
            </Column>
            <Column :header="t('lblAddress')" sortable field="address">
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>
            <Column :header="t('description')" sortable field="description">
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>

            <template #empty>{{ t('empty') }}</template>
        </DataTable>

        <Dialog
            style="width: 500px;"
            :visible="openDialog"
            :closable="false"
        >
            
            <template #header>
                <Divider>
                    <!-- <i class="pi pi-users" style="color: slateblue; font-size: 1.7rem;"></i> -->
                    <Button icon="pi pi-users" size="large" variant="link"></Button>
                    <span v-if="!editMode" class="text-xl">{{ t('lblHeaderCreate').replace('[0]', t('supplier')) }}</span>
                    <span v-else class="text-xl">{{ t('lblHeaderUpdate').replace('[0]', t('supplier')) }}</span>
                </Divider>
            </template>
            
            <template #default>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-id-card" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-id-card" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="supplierForm.code"
                            :invalid="errors.code ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('lblCode') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.code">{{ errors.code }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-user" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-user" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="supplierForm.name"
                            :invalid="errors.name ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('lblName') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.name">{{ errors.name }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-envelope" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-envelope" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="supplierForm.email"
                            :invalid="errors.email ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('email') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.email">{{ errors.email }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-phone" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-phone" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputMask
                            v-model="supplierForm.phone"
                            :invalid="errors.phone ? true : false"
                            mask="999-999-999"
                            auto-clear
                            
                        >
                            
                        </InputMask>
                        <label>{{ t('lblPhone') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.phone">{{ errors.phone }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-address-book" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-address-book" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="supplierForm.address"
                        >
                            
                        </InputText>
                        <label>{{ t('lblAddress') }} </label>
                    </FloatLabel>
                </InputGroup>
                
                <InputGroup class="my-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-pencil" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-pencil" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            v-model="supplierForm.description"
                            class="w-full"
                        >
                            
                        </Textarea>
                        <label>{{ t('description') }}</label>
                    </FloatLabel>
                </InputGroup>
            </template>
            <template #footer>
                <Button icon="pi pi-check" class="mt-2" :loading="btnLoading" :label="t('btnSave')" size="small" type="submit" @click="editMode ? update() : create()"></Button>
                <Button icon="pi pi-times" class="mt-2" :label="t('btnCancel')" @click="close" size="small"></Button>
            </template>
        </Dialog>
    </div>
</template>
<script setup lang="ts">
    definePageMeta({ 
        // middleware: 'auth', 
        layout: 'dashboard'})
    import type { supplier } from '~/composables/useSupplier'
    import {
        applySupplierValidationErrors,
        createEmptySupplierForm,
        createSupplierErrors,
        createSupplierFilters,
        type SupplierErrors,
        type SupplierForm
    } from '~/services/supplier.service'
    import { useAuthStore } from '~~/store/state'
    const { confirmDelete } = useConfirmDelete()
    const { t } = useI18n()
    const supplierAction = useSuppliers()
    const authStore = useAuthStore()
    const { hasPermission } = useFunction()
    const route = useRoute()
    const messageBox = MessageBox()
    const selectSupplier = ref([])
    const supplierList = ref<supplier[]>([])

    const loading = ref(false)
    const btnLoading = ref(false)
    const editMode = ref(false)
    const openDialog = ref(false)
    const filters = ref()
    const errors = ref<SupplierErrors>(createSupplierErrors())
    const supplierForm = ref<SupplierForm>(createEmptySupplierForm())

    const canCreate = computed(() => hasPermission(route.path, 'create'))
    const canUpdate = computed(() => hasPermission(route.path, 'update'))
    const canDelete = computed(() => hasPermission(route.path, 'delete'))
    const canView = computed(() => hasPermission(route.path, 'view'))

    const initFilters = () => {
        filters.value = createSupplierFilters()
    }
    initFilters()
    const clearFilter = () => {
        initFilters();
    }

    const close = ()=>{
        editMode.value = false
        openDialog.value = false
        loading.value = false
        btnLoading.value = false
        errors.value = createSupplierErrors()
        supplierForm.value = createEmptySupplierForm()
    }
    const onOpenDialogEdit = (item: any) => {
        editMode.value = true
        supplierForm.value.id = item.data.id
        supplierForm.value.name = item.data.name
        supplierForm.value.code = item.data.code
        supplierForm.value.address = item.data.address
        supplierForm.value.phone = item.data.phone
        supplierForm.value.email = item.data.email
        supplierForm.value.description = item.data.description
        openDialog.value = true
    }
    const successMessage = () => messageBox.success(t('successMessage'))
    const getAllSupplier = async () => {
        loading.value = true
        supplierList.value = await supplierAction.getAllSupplier()
        loading.value = false
    }
    const create = async () => {
        btnLoading.value = true
        loading.value = true
        await supplierAction.create(supplierForm.value)
        .then((res) => {
            getAllSupplier()
            successMessage()
            btnLoading.value = false
            close()
        })
        .catch((error: any) => {
            errors.value = applySupplierValidationErrors(error?.data?.data?.detail, errors.value)
            loading.value = false
            btnLoading.value = false
        })
    }
    const update = async () => {
        btnLoading.value = true
        loading.value = true
        await supplierAction.update(supplierForm.value.id,supplierForm.value)
        .then((res) =>{
            getAllSupplier()
            close()
            loading.value = false
            btnLoading.value = false
            successMessage()
        })
        .catch((error: any) =>{
            errors.value = applySupplierValidationErrors(error?.data?.data?.detail, errors.value)
            loading.value = false
            btnLoading.value = false
        })
    }
    const remove = async () =>{
        btnLoading.value = true
        loading.value = true
        await supplierAction.remove(selectSupplier.value)
        .then((res) => {
            getAllSupplier()
            loading.value = false
            btnLoading.value = false
            successMessage()
        })
        .catch((error: any) => {
            messageBox.error(t('errorMessage'))
        })
    }
    const deleteMany = () =>{
        if(!selectSupplier.value.length) return

        confirmDelete(
            async () => {
                loading.value = true
                const Ids = selectSupplier.value.map((e: supplier) => e.id)
                await supplierAction.remove(Ids)
                .then( async () => {
                    await getAllSupplier()
                    successMessage()
                })
                .catch((error: any) => {
                    loading.value = false
                    messageBox.error(t('errorMessage'))
                })
            }
        )
    }

    onMounted(() => {
        getAllSupplier()
    })
</script>