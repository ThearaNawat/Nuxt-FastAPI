<template>
    <div id="category">
        <DataTable
            paginator 
            :rows="20" 
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            removable-sort
            resizable-columns
            reorderable-columns
            :value="categoryList"
            :lazy="loading"
            size="small"
            striped-rows
            v-model:selection="selectCategory"
            v-model:filters="filters"
            :global-filter-fields="['name', 'description', 'code']"
            filter-display="menu"
            data-key="id"
            @row-dblclick="OpenDialogEdit"
            row-hover
            scrollable
            scroll-height="650px"
            :virtual-scroller-options="{ itemSize: 46 }"
            paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            currentPageReportTemplate="{first} to {last} of {totalRecords}"
        >
            <Toolbar>
                <template #end>
                    <Button :label="t('btnCreate')" icon="pi pi-plus" @click="openDialog = true"></Button>
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
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"/>
                </template>
            </Column>
            <Column :header="t('lblName')" sortable field="name" >
                <template #filter = "{ filterModel }">
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
                    <i class="pi pi-slack" style="color: slateblue; font-size: 1.7rem;"></i>
                    <span v-if="!editMode" class="ml-2 text-xl">{{ t('lblHeaderCreate').replace('[0]', t('category')) }}</span>
                    <span v-else class="ml-2 text-xl">{{ t('lblHeaderUpdate').replace('[0]', t('category')) }}</span>
                </Divider>
            </template>
            
            <template #default>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-slack" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-slack" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="categoryForm.code"
                            :invalid="errors.code ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('lblCode') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.code">{{ errors.code }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-slack" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-slack" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="categoryForm.name"
                            :invalid="errors.name ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('lblName') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.name">{{ errors.name }}</Message>
                <InputGroup class="my-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-pencil" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-pencil" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            v-model="categoryForm.description"
                            class="w-full"
                        >
                            
                        </Textarea>
                        <label>{{ t('description') }}</label>
                    </FloatLabel>
                </InputGroup>
            </template>
            <template #footer>
                <Button icon="pi pi-check" :loading="btnLoading" :label="t('btnSave')" size="small" type="submit" @click="editMode ? update() : create()"></Button>
                <Button icon="pi pi-times" :label="t('btnCancel')" @click="close" size="small"></Button>
            </template>
        </Dialog>
    </div>
</template>
<script setup lang="ts">
    definePageMeta({
        middleware: 'auth',
        layout: 'dashboard'
    })
    import { FilterMatchMode, FilterOperator} from '@primevue/core/api'
    const { confirmDelete } = useConfirmDelete()
    const { t } = useI18n()
    const messageBox = MessageBox()
    const categoryAction = useCategory() 
    const selectCategory = ref([])
    const categoryList = ref<category[]>([])
    const loading = ref(false)
    const btnLoading = ref(false)
    const editMode = ref(false)
    const openDialog = ref(false)
    const filters = ref()
    const errors = ref({code: '', name: ''})
    const categoryForm = ref({
        id: 0, name: '', code: '', description: ''
    })
    const initFilters = () => {
        filters.value = {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },            
            code: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
            description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }]}
        };
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
        errors.value = {name: '', code: ''}
        categoryForm.value = { id: 0, name: '', code: '', description: ''}
    }
    const OpenDialogEdit = (item: any) => {
        editMode.value = true
        categoryForm.value.id = item.data.id
        categoryForm.value.name = item.data.name
        categoryForm.value.code = item.data.code
        categoryForm.value.description = item.data.description
        openDialog.value = true
    }
    const successMessage = () => messageBox.success('Your data was saved successfully.')
    const getCategoryList = async () => {
        loading.value = true
        categoryList.value = await categoryAction.getAllCategory()
        loading.value = false
    }
    const create = async () => {
        btnLoading.value = true
        loading.value = true
        await categoryAction.create(categoryForm.value)
        .then((res) => {
            getCategoryList()
            successMessage()
            btnLoading.value = false
            close()
        })
        .catch((error: any) => {
            let respondedData = error?.data?.data?.detail
            if(typeof respondedData != 'string' && respondedData.length > 0){
                for(var i = 0; i < respondedData.length; i++){
                    let fieldName = respondedData[i].loc[1]
                    if(fieldName === 'name') errors.value.name = respondedData[i].msg
                    
                    if(fieldName === 'code') errors.value.code = respondedData[i].msg

                }
            }
            loading.value = false
            btnLoading.value = false
            //messageBox.error('An issue have occurred please inform technicial support.')
        })
    }
    const update = async () => {
        btnLoading.value = true
        loading.value = true
        await categoryAction.update(categoryForm.value.id,categoryForm.value)
        .then((res) =>{
            getCategoryList()
            close()
            loading.value = false
            btnLoading.value = false
            successMessage()
        })
        .catch((error: any) =>{
            let respondedData = error?.data?.data?.detail
            var x = typeof respondedData
            console.log(x)
            if(typeof respondedData != 'string' && respondedData.length > 0){
                for(var i = 0; i < respondedData.length; i++){
                    let fieldName = respondedData[i].loc[1]
                    if(fieldName === 'name') errors.value.name = respondedData[i].msg
                    
                    if(fieldName === 'code') errors.value.code = respondedData[i].msg

                }
            }
            loading.value = false
            btnLoading.value = false
        })
        const remove = async () =>{
            btnLoading.value = true
            loading.value = true
            await categoryAction.remove(selectCategory.value)
            .then((res) => {
                getCategoryList()
                loading.value = false
                btnLoading.value = false
                successMessage()
            })
            .catch((error: any) => {
                messageBox.error('An issue have occurred please inform technicial support.')
            })
        } 
    }
    const deleteMany = () =>{
        if(!selectCategory.value.length) return

        confirmDelete(
            async () => {
                loading.value = true
                const userIds = selectCategory.value.map((e: any) => e.id)
                await categoryAction.remove(userIds)
                .then( async () => {
                    await getCategoryList()
                    successMessage()
                })
                .catch((error: any) => {
                    loading.value = false
                    messageBox.error('An issue have occurred please inform technicial support.')
                })
            }
        )
    }

    onMounted(getCategoryList)
</script>