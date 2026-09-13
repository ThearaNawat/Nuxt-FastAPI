<template>
    <div id="category">
        <DataTable
            ref="dt"
            paginator 
            :rows="rowsPerPage"
            :first="currentPage * rowsPerPage"
            @page="onPageChange"
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            removable-sort
            resizable-columns
            reorderable-columns
            :value="categoryList"
            :loading="loading"
            size="small"
            striped-rows
            v-model:selection="selectCategory"
            v-model:filters="filters"
            :global-filter-fields="['name', 'description', 'code']"
            filter-display="menu"
            data-key="id"
            @row-dblclick="OpenDialogEdit"
            @select-all-change="onSelectAllChange"
            row-hover
            scrollable
            scroll-height="500px"
            style="max-width: 1320px"
            
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
        // middleware: 'auth',
        layout: 'dashboard'
    })
    import {
        applyCategoryValidationErrors,
        createCategoryErrors,
        createCategoryFilters,
        createEmptyCategoryForm,
        type CategoryErrors,
        type CategoryForm
    } from '~/services/category.service'
    const { confirmDelete } = useConfirmDelete()
    const { t } = useI18n()
    const messageBox = MessageBox()
    const categoryAction = useCategory()
    const selectCategory = ref([])
    const categoryList = ref<category[]>([])
    const currentPage = ref(0)
    const rowsPerPage = ref(20)
    const loading = ref(false)
    const btnLoading = ref(false)
    const editMode = ref(false)
    const openDialog = ref(false)
    const filters = ref()
    const errors = ref<CategoryErrors>(createCategoryErrors())
    const categoryForm = ref<CategoryForm>(createEmptyCategoryForm())
    const initFilters = () => {
        filters.value = createCategoryFilters()
    }
    initFilters()

    const getCurrentPageItems = () => {
        const start = currentPage.value * rowsPerPage.value
        const end = start + rowsPerPage.value
        return categoryList.value.slice(start, end)
    }

    const onSelectAllChange = (event: any) => {
        if (event.checked) {
            selectCategory.value = getCurrentPageItems() as any
        } else {
            selectCategory.value = []
        }
    }

    const onPageChange = (event: any) => {
        currentPage.value = event.page
        rowsPerPage.value = event.rows
        selectCategory.value = []
    }
    const clearFilter = () => {
        initFilters();
    }

    const close = ()=>{
        editMode.value = false
        openDialog.value = false
        loading.value = false
        btnLoading.value = false
        errors.value = createCategoryErrors()
        categoryForm.value = createEmptyCategoryForm()
    }
    const OpenDialogEdit = (item: any) => {
        editMode.value = true
        categoryForm.value.id = item.data.id
        categoryForm.value.name = item.data.name
        categoryForm.value.code = item.data.code
        categoryForm.value.description = item.data.description
        openDialog.value = true
    }
    const successMessage = () => messageBox.success(t('successMessage'))
    const getCategoryList = async () => {
        loading.value = true
        currentPage.value = 0
        selectCategory.value = []
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
            errors.value = applyCategoryValidationErrors(error?.data?.data?.detail, errors.value)
            loading.value = false
            btnLoading.value = false
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
            errors.value = applyCategoryValidationErrors(error?.data?.data?.detail, errors.value)
            loading.value = false
            btnLoading.value = false
        })
    }

    const deleteMany = () =>{
        if(!selectCategory.value || selectCategory.value.length === 0) {
            messageBox.error(t('warningMessage'))
            return
        }

        confirmDelete(
            async () => {
                try {
                    loading.value = true
                    const idsToDelete = selectCategory.value.map((e: any) => e.id).filter((id: any) => id)

                    if(idsToDelete.length === 0) {
                        messageBox.error(t('warningMessage'))
                        loading.value = false
                        return
                    }

                    await categoryAction.remove(idsToDelete)
                    .then( async () => {
                        selectCategory.value = []
                        await getCategoryList()
                        successMessage()
                    })
                    .catch((error: any) => {
                        loading.value = false
                        messageBox.error(t('errorMessage'))
                    })
                } catch (error) {
                    loading.value = false
                    messageBox.error(t('errorMessage'))
                }
            }
        )
    }

    onMounted(getCategoryList)
</script>