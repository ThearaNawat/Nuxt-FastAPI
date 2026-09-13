<template>
    <div id="menu">
        <DataTable
            paginator 
            :rows="20" 
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            removable-sort
            resizable-columns
            reorderable-columns
            column-resize-mode="fit"
            size="small"
            :value="menuList"
            :lazy="loading"
            striped-rows
            filter-display="menu"
            v-model:selection="selectMenu"
            v-model:filters="filters"
            :global-filter-fields="['label','path','icon','is_active','type']"
            data-key="id"
            scrollable
            scroll-height="500px"
            
            row-hover
            @row-dblclick="onOpenDialogEdit"
            paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            currentPageReportTemplate="{first} to {last} of {totalRecords}"

        >
            <Toolbar>
                <template #end>
                    <Button :label="t('btnCreate')" icon="pi pi-plus" @click="onOpenDialog"></Button>
                    <Button :label="t('btnDelete')" icon="pi pi-trash" class="ml-2" @click="removeMenu"></Button>
                </template>
            </Toolbar>
            <template #header>
                <div class="flex justify-between">
                    <IconField >
                        <InputIcon>
                            <i class="pi pi-search"></i>
                        </InputIcon>
                        <InputText placeholder="Search" v-model="filters['global'].value"></InputText>
                    </IconField>
                    <Button icon="pi pi-filter-slash" @click="clearFilter" variant="link"></Button>
                </div>
            </template>
            <template #empty>{{ t('empty') }}</template>
            <Column selection-mode="single"  header-style="width: 2rem"></Column>
            <Column :header="t('label')" field="label" sortable>
                <template #body ="{ data }">
                    <div class="text-green-700 font-bold">
                        {{ data.label }}
                    </div>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')" />
                </template>
            </Column>
            <Column :header="t('icon')" field="icon"  sortable>
                <template #body ="{ data }">
                    <div class="text-green-700 font-bold">
                        {{ data.icon }}
                    </div>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')" />
                </template>
            </Column>
            <Column :header="t('path')" sortable field="path">
                <template #body="{ data }">
                    {{ data.path }}
                </template>
                <template #filter = "{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>
            <Column :header="t('order')" sortable field="display_order">
                <template #body="{ data }">
                    {{ data.display_order }}
                </template>
            </Column>
            <Column :header="t('perent')" sortable field="perent_id">
                <template #body="{ data }">
                    {{ data.parent_label }}
                </template>

            </Column>
            <Column :header="t('active')" sortable field="is_active" data-type="boolean">
                <template #body="{ data }">
                    <i class="pi" :class="{ 'pi-check-circle text-green-500': data.is_active, 'pi-times-circle text-red-400': !data.is_active }"></i>
                </template>
                <template #filter="{ filterModel }">
                    <label for="verified-filter" class="font-bold"> Verified </label>
                    <Checkbox v-model="filterModel.value" :indeterminate="filterModel.value === null" binary inputId="verified-filter" />
                </template>
            </Column>
            <Column :header="t('type')" sortable field="type">
                <template #body="{ data }">
                    {{ data.type }}
                </template>
                <template #filter="{ filterModel }">
                    <Select 
                        v-model="filterModel.value" 
                        :options="['MENU','BUTTON']" 
                        :placeholder="t('search')" 
                        showClear
                    >
                    </Select>
                </template>
            </Column>
            <Column :header="t('created_at')" sortable filter-field="created_at" field="created_at" data-type="date">
                <template #body="{ data }">
                    {{ data.created_at }}
                </template>
                <template #filter="{ filterModel }">
                    <DatePicker 
                        v-model="filterModel.value" 
                        date-format="dd-mm-yy"
                        :placeholder="t('search')"
                    >
                    </DatePicker>
                </template>
            </Column>
            <Column :header="t('updated_at')" sortable field="updated_at" data-type="date">
                <template #body="{ data }">
                    {{ data.updated_at }}
                </template>
                <template #filter="{ filterModel }">
                    <DatePicker 
                        v-model="filterModel.value" 
                        date-format="dd-mm-yy" 
                        :placeholder="t('search')"
                    >
                    </DatePicker>
                </template>
            </Column>
        </DataTable>

        <Dialog
            style="width: 500px;"
            :visible="openDialog"
            :closable="false"
        >
            
            <template #header>
                <Divider>
                    <Button icon="pi pi-user-plus" variant="link" size="large" />
                    <span class="text-xl">{{ t('lblHeaderCreate').replace('[0]', t('menu')) }}</span>
                </Divider>
            </template>
            
            <template #default>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            <Button icon="pi pi-user" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputText
                                v-model="menuForm.label"
                            >
                                
                            </InputText>
                            <label>{{ t('label') }}*</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.label">{{ errors.label }}</Message>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            <Button icon="pi pi-user" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputText
                                v-model="menuForm.path"
                            >
                                
                            </InputText>
                            <label>{{ t('path') }}*</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.path">{{ errors.path }}</Message>
                    <InputGroup class="my-2">
                        <InputGroupAddon>
                            <Button icon="pi pi-user" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputText
                                v-model="menuForm.icon"
                            >
                                
                            </InputText>
                            <label>{{ t('icon') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <InputGroup>
                        <InputGroupAddon>
                            <Button icon="pi pi-user" variant="link" />
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputNumber
                                v-model="menuForm.display_order"
                            >
                                
                            </InputNumber>
                            <label>{{ t('order') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            
                            <Button icon="pi pi-slack" size="small" variant="link"></Button>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <Select
                                :options="menuDropdown"
                                show-clear
                                option-label="label"
                                option-value="id"
                                v-model="menuForm.parent_id"
                            >
                                
                            </Select>
                            <label>{{ t('perent') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            
                            <Button icon="pi pi-slack" size="small" variant="link"></Button>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <Select
                                :options="type"
                                show-clear
                                v-model="menuForm.type"
                            >
                                
                            </Select>
                            <label>{{ t('type') }} *</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.type">{{ errors.type }}</Message>
                    <Checkbox binary  class="mr-2" v-model="menuForm.is_active">Active</Checkbox>
                    <label>{{ t('active') }}</label>
            </template>
            <template #footer>
                <Button icon="pi pi-check" :loading="btnLoading" label="Save" size="small" type="submit" @click="editMode ? updateMenu() : createMenu()"></Button>
                <Button icon="pi pi-times" label="Cancel" @click="onCloseDialog" size="small"></Button>
            </template>
        </Dialog>
    </div>
</template>

<script lang="ts" setup>
    definePageMeta({
        layout: 'dashboard',
        // middleware: 'auth'
    })
    import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
    import type { Menu } from '../../composables/useMenu'
    const { t } = useI18n()
    const messageBox = MessageBox()
    const { confirmDelete } = useConfirmDelete()
    const { create, getAllMenu, remove, update } = useMenu()
    const menuList = ref<Menu[]>([])
    const menuDropdown = ref<Menu[]>([])
    const openDialog = ref(false)
    const btnLoading = ref(false)
    const loading = ref(false)
    const editMode = ref(false)
    const selectMenu = ref()
    const filters = ref()
    const type = ref(['MENU','BUTTON'])
    const errors = reactive({label: '', path: '', type: ''})
    const menuForm = reactive<Menu>({ id: 0, label: '', path: '', icon: '', type: '', is_active: true, display_order: 0, parent_id: null })
    const initFilters = () => {
        filters.value = {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            label: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }]},
            icon: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }]},
            is_active: { value: null, matchMode: FilterMatchMode.EQUALS },
            type: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]}
        };
    }
    initFilters()
    const clearFilter = () => {
        initFilters();
        selectMenu.value = null
    }
    
    const successMessage = () => messageBox.success(t('successMessage'))
    const errorMessage = () => messageBox.error(t('errorMessage'))
    const warningMessage = () => messageBox.warning(t('warningMessage'))
    const onOpenDialog = () => openDialog.value = true
    const onClearError = () => {
        errors.label = ''
        errors.path = ''
        errors.type = ''
    }
    const onCloseDialog = () => {
        menuForm.id = 0
        menuForm.label = ''
        menuForm.path = ''
        menuForm.display_order = 0
        menuForm.icon = ''
        menuForm.is_active = false
        menuForm.type = ''
        menuForm.parent_id = 0
        openDialog.value = false
        btnLoading.value = false
        loading.value = false
        editMode.value = false
        onClearError()
    }
    const createMenu = async () => {
        btnLoading.value = true
        loading.value = true
        await create(menuForm)
        .then((res: any) => {
            getAll()
            btnLoading.value = false
            successMessage()
            onCloseDialog()
        })
        .catch((error: any) => {
            btnLoading.value = false
            loading.value = false
        })
    }
    const updateMenu = async () => {
        const { id } = menuForm
        btnLoading.value = true
        loading.value = true
        await update(id, menuForm)
        .then((res: any) => {
            getAll()
            btnLoading.value = false
            loading.value = false
            successMessage()
            onCloseDialog()
        })
        .catch((error: any) => {
            btnLoading.value = false
            loading.value = false
        })
    }
    const removeMenu = async () => {
        if(!selectMenu.value) return warningMessage()
        const menuId = selectMenu.value?.id
        console.log(selectMenu.value)
        confirmDelete(
            async () => {
                loading.value = true
                
                await remove(menuId)
                .then( async () => {
                    await getAll()
                    successMessage()
                    onCloseDialog()
                    loading.value = false
                })
                .catch((error: any) => {
                    loading.value = false
                    errorMessage()
                })
            }
        )
    }
    const getAll = async () => { 
        loading.value = true
        await getAllMenu()
        .then((res: any) => {
            menuList.value = res
            loading.value = false
            menuDropdown.value = menuList.value.filter(item => item.type === 'MENU')
        })
        .catch((error: any) => {
            loading.value = false
        }) 
    }
    const onOpenDialogEdit = (item: any) => {
        editMode.value = true
        menuForm.id = item.data.id
        menuForm.label = item.data.label
        menuForm.path = item.data.path
        menuForm.display_order = item.data.display_order
        menuForm.icon = item.data.icon
        menuForm.is_active = item.data.is_active
        menuForm.type = item.data.type
        menuForm.parent_id = item.data.parent_id
        openDialog.value = true
    }
    
    onMounted(getAll)
</script>

<style lang="scss" scoped>

</style>