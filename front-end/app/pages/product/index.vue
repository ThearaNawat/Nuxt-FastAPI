<template>
    <div id="product">
        <DataTable
            removable-sort
            resizable-columns
            reorderable-columns
            row-hover
            paginator
            size="small"
            :value="productList"
            v-model:selection="selectProduct"
            v-model:filters="filters"
            :global-filter-fields="['name', 'description', 'code', 'package', 'stock', 'category_id', 'measurement_id']"
            filter-display="menu"
            :sort-order="-1"
            data-key="id"
            @row-dblclick="onSelectedItem"
            :rows="10" 
            sort-mode="multiple"
            scrollable
            striped-rows
            scroll-height="500px"
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            :loading="loading"
            style="max-width: 1320px"
        >
        <Toolbar>
            <template #end>
                <Button :label="t('btnCreate')" icon="pi pi-plus" @click="onOpenDialog"></Button>
                <Button :label="t('btnDelete')" icon="pi pi-trash" class="mx-2" @click="remove"></Button>
                <Button :label="t('btnExport')" icon="pi pi-file-excel"></Button>
            </template>
        </Toolbar>
        <template #header>
            <div class="flex justify-between">
                <Button icon="pi pi-filter-slash" @click="clearFilter" variant="link"></Button>
            </div>
        </template>
        <template #empty>{{ t('empty') }}</template>
        <Column selection-mode="multiple"  :exportable="false" header-style="width: 2rem"></Column>
        <Column :header="t('lblCode')" field="code" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('lblName')" field="name" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('expire')" field="expire_date" filter-field="expire_date" data-type="date" sortable class="text-orange-700" style="min-width: 200px">
            <template #body ="{data}">
                <Button v-if="data.expire_date" icon="pi pi-calendar" size="small" variant="link"></Button>
                <span>{{ formatDate(data.expire_date) }}</span>
            </template>

            <template #filter="{ filterModel }">
                <DatePicker v-model="filterModel.value" dateFormat="dd/mm/yy" :placeholder="t('search')" />
            </template>
        </Column>
        <Column :header="t('package')" field="package" sortable style="min-width: 200px">
            <template #body="{ data }">
                <Button v-if="data.package && data.measurement_code" icon="pi pi-box" size="small" variant="link"></Button>
                <span v-if="data.package && data.measurement_code">{{ `${data.package} ${data.measurement_code}` }}</span>
                <span v-else>N/A</span>
            </template>
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        
        <Column :header="t('category')" field="category_id" sortable style="min-width: 200px">
            <template #body="{data}">
                {{ data.category_name }}
            </template>
            <template #filter="{ filterModel }">
                <Select 
                    v-model="filterModel.value" 
                    :options="categoryOptions" 
                    option-label="name" 
                    option-value="id" 
                    :placeholder="t('search')" 
                    showClear
                >
                </Select>
            </template>
        </Column>
        <Column :header="t('review')" field="review" sortable style="min-width: 200px">
            <template #body="{data}">
                <Rating readonly :model-value="data.review"></Rating>
            </template>
        </Column>
        <Column :header="t('remark')" field="description" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
            </template>
        </Column>
        <Column :header="t('stock')" field="stock" sortable style="min-width: 200px">
            <template #body="{data}">
            <Tag :value="getValueStock(data.stock)" :severity="getSeverity(data.stock)" :icon="getIconStock(getValueStock(data.stock))"></Tag>
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
                    <Button icon="pi pi-briefcase" size="large" variant="link"></Button>
                    <span v-if="!editMode" class="text-xl">{{ t('lblHeaderCreate').replace('[0]', t('product')) }}</span>
                    <span v-else class="text-xl">{{ t('lblHeaderUpdate').replace('[0]', t('product')) }}</span>
                </Divider>
            </template>
            
            <template #default>

                <FileUpload 
                    @select="onFileSelect" 
                    mode="advanced"
                    accept="image/*" 
                    :maxFileSize="1000000" 
                    custom-upload
                    multiple
                    >
                    <template #header="{ chooseCallback, uploadCallback, clearCallback, files}">
                        <div class="flex flex-wrap justify-between items-center">
                            <div class="flex gap-2">
                                <Button @click="chooseCallback()" icon="pi pi-images" rounded variant="outlined" severity="secondary"></Button>
                                <Button @click="() => { clearCallback(); onFileClear() }" icon="pi pi-times" rounded variant="outlined" severity="danger" :disabled="!files || files.length === 0"></Button>
                            </div>
                        </div>
                    </template>
                    
                    <template #content ="{files, removeFileCallback}">
                        <Carousel :value="files" :numVisible="1"  :numScroll="1" orientation="horizontal" containerClass="flex items-center justify-center">
                            <template #item="{data, index}">
                                <div class="flex flex-col items-center">
                                    <Image :src="data.objectURL" preview alt="Image" width="200" height="150"></Image>
                                    <Button icon="pi pi-times" size="small" variant="text" @click="onRemoveTemplatingFile(data, removeFileCallback, index)"></Button>
                                </div>
                            </template>
                        </Carousel>
                    </template>
                    <template #empty>
                        <div class="flex items-center justify-center flex-col">
                            <i class="pi pi-cloud-upload !rounded-full !text-4xl !text-muted-color" />
                            <p class="mb-0">Drag and drop files to here to upload.</p>
                        </div>
                    </template>
                </FileUpload>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-id-card" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-briefcase" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="productForm.code"
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
                        <Button icon="pi pi-briefcase" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="productForm.name"
                            :invalid="errors.name ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('lblName') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.name">{{ errors.name }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-box" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="productForm.package"
                            :invalid="errors.package ? true : false"
                            placeholder="12 x 20"
                        >
                            
                        </InputText>
                        <label>{{ t('package') }} </label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.package">{{ errors.package }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-box" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Select
                            :options="measurementList"
                            option-label="name"
                            option-value="id"
                            show-clear
                            v-model="productForm.measurement_id"
                          
                        >
                            <template #value="{ placeholder }">
                                <div class="flex items-center gap-2" v-if="productForm.measurement_id">
                                    <template v-for="prod in measurementList" :key="prod.id">
                                        <div class="flex items-center gap-2" v-if="prod.id === productForm.measurement_id">
                                            <span>{{ prod.code }} - </span>
                                            <span>{{ prod.name }}</span>
                                        </div>
                                    </template>
                                </div>
                                <span v-else class="text-gray-400">{{ placeholder }}</span>
                            </template>

                            <template #option="{ option }">
                                <div class="flex items-center gap-2">
                                    <span>{{ option.code }} - </span>
                                    <span>{{ option.name }}</span>
                                </div>
                            </template>
                        </Select>
                        <label>{{ t('measurement') }}</label>
                    </FloatLabel>
                </InputGroup>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-calendar" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <DatePicker
                            show-clear
                            icon-display="input"
                            v-model="productForm.expire_date"
                            date-format="dd-mm-yy"
                            update-model-type="date"
                        >
                        </DatePicker>
                        <label>{{ t('expire') }} </label>
                    </FloatLabel>
                </InputGroup>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-slack" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Select
                            :options="categoryOptions"
                            option-label="name"
                            option-value="id"
                            show-clear
                            v-model="productForm.category_id"
                            :invalid="errors.category_id ? true : false"
                        >
                            
                        </Select>
                        <label>{{ t('category') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.category_id">{{ errors.category_id }}</Message>
                <InputGroup class="my-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-pencil" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            v-model="productForm.description"
                            class="w-full"
                        >
                            
                        </Textarea>
                        <label>{{ t('remark') }}</label>
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
        layout: 'dashboard',
    })
    import type { FileUploadSelectEvent } from 'primevue/fileupload'
    import type { product } from '~/composables/useProduct'
    import type { category } from '~/composables/useCategory'
    import type { Measurement } from '~~/shared/types/measurement'
    import {
        buildProductFormData,
        createEmptyProductForm,
        createProductFilters,
        formatDate,
        getIconStock,
        getSeverity,
        getValueStock,
        parseDate,
        type ProductForm
    } from '~/services/product.service'
    const measurementAction = useMeasurement()
    const productAction = useProduct()
    const { t } = useI18n()
    const { confirmDelete } = useConfirmDelete()
    const messageBox = MessageBox()
    const filters = ref()
    const loading = ref(false)
    const btnLoading = ref(false)
    const editMode = ref(false)
    const openDialog = ref(false)
    const measurementList = ref<Measurement[]>([])
    const selectProduct = ref<product[]>([])
    const productList = ref<product[]>([])
    const categoryOptions = ref<category[]>([])
    const srcFile = <any>ref([])
    const errors = reactive({code: '', name: '', expire_date: null, package: '', category_id: ''})
    const productForm = reactive<ProductForm>(createEmptyProductForm())

    const initFilters = () => {
        filters.value = createProductFilters()
    }

    const onRemoveTemplatingFile = (file: File, removeFileCallback: any, index: number) => {
        removeFileCallback(index)
        srcFile.value.splice(index, 1)
        productForm.images = [...srcFile.value]
    }
    const onFileClear = () => {
        srcFile.value = []
        productForm.images = []
    }
    function onFileSelect(event: FileUploadSelectEvent) {
        event.files.forEach((item: any) => {
            srcFile.value.push(item)
        })
        productForm.images = [...srcFile.value]
    }

    initFilters()
    const clearFilter = () => {
        initFilters();
        selectProduct.value = []
        getAllProduct()
    }
    const onSelectedItem = (item: any) => {
        openDialog.value = true
        editMode.value = true
        productForm.id = item.data.id
        productForm.code = item.data.code
        productForm.name = item.data.name
        productForm.expire_date = item.data.expire_date ? parseDate(item.data.expire_date) : null
        productForm.package = item.data.package
        productForm.description = item.data.description
        productForm.stock = item.data.stock
        productForm.category_id = item.data.category_id
        productForm.measurement_id = item.data.measurement_id
    }
    const close = ()=>{
        editMode.value = false
        openDialog.value = false
        loading.value = false
        btnLoading.value = false
        productForm.id = 0
        productForm.name = ''
        productForm.code = ''
        productForm.description = ''
        productForm.stock= 0
        productForm.expire_date = null
        productForm.category_id = null
        productForm.package = ''
        productForm.images = []
        productForm.measurement_id = null
        srcFile.value = []
        errors.category_id = ''
        errors.code = ''
        errors.name = ''
        errors.expire_date = null
        errors.package = ''
        selectProduct.value = []
    }
    const getAllMeasurement = async () => measurementList.value = await measurementAction.getAll()
    const onOpenDialog = () => {
        openDialog.value = true
    }
    const successMessage = () => messageBox.success(t('successMessage'))
    const warningMessage = () => messageBox.warning(t('warningMessage'))
    const getCategoryOption = async () => categoryOptions.value =  await productAction.category()
    const getAllProduct = async () => {
        loading.value = true;
        await productAction.getAllProduct()
        .then((res: any) => {
            productList.value = res
            loading.value = false
        })
        .catch((error: any) => {
            loading.value = false
        })
    }
    const create = async () => {
        loading.value = true;
        btnLoading.value = true;
        await productAction.create(buildProductFormData(productForm))
        .then((res: any) => {
            btnLoading.value = false;
            loading.value = false;
            successMessage();
            getAllProduct();
            close()
        })
        .catch((error: any) => {
            loading.value = false;
            btnLoading.value = false;
            let respondedData = error?.data?.data?.detail
            if(typeof respondedData == 'object'){
                for(var i = 0; i < respondedData.length; i++){
                    let fieldName = respondedData[i].loc[1]
                    if(fieldName === 'name') errors.name = respondedData[i].msg

                    if(fieldName === 'code') errors.code = respondedData[i].msg

                    if(fieldName === 'category_id') errors.category_id = respondedData[i].msg
                }
            }
        })
    }
    const update = async () => {
        loading.value = true;
        btnLoading.value = true;
        await productAction.update(productForm.id, buildProductFormData(productForm))
        .then((res: any) => {
            loading.value = false;
            btnLoading.value = false;
            getAllProduct();
            close();
            successMessage()
        })
        .catch((error: any)=> {
            loading.value = false;
            btnLoading.value = false;
            let respondedData = error?.data?.data?.detail
            if(typeof respondedData != 'string' && respondedData.length > 0){
                for(var i = 0; i < respondedData.length; i++){
                    let fieldName = respondedData[i].loc[1]
                    if(fieldName === 'name') errors.name = respondedData[i].msg

                    if(fieldName === 'code') errors.code = respondedData[i].msg

                }
            }
        })
    }
    const remove = () => {
        if(selectProduct.value.length == 0) return warningMessage();
        confirmDelete( async () => {
            loading.value = true;
            var ids = selectProduct.value.map(e => e.id);
            await productAction.remove(ids)
            .then((res: any) => {
                loading.value = false; getAllProduct();
                successMessage();
                selectProduct.value = []
            })
            .catch((error: any)=> {
                loading.value = false
            })
        })
    }

    onMounted(() => {
        if(categoryOptions.value.length == 0 || categoryOptions.value == null) getCategoryOption()
        getAllProduct()
        if(measurementList.value.length == 0 || measurementList.value == null) getAllMeasurement()
    })
</script>