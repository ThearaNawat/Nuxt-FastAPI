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
            :global-filter-fields="['name', 'description', 'code', 'package', 'stock', 'category_id']"
            filter-display="menu"
            data-key="id"
            @row-dblclick="onSelectedItem"
            :rows="20" 
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            :lazy="loading"
            scrollable
            scroll-height="600px"
            :virtual-scroller-options="{ itemSize: 46 }"
            paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            currentPageReportTemplate="{first} to {last} of {totalRecords}"
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
            <Column selection-mode="multiple" :exportable="false" header-style="width: 2rem"></Column>
            <Column :header="t('lblCode')" field="code" sortable>
                <template #filter="{filterModel}">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>
            <Column :header="t('lblName')" field="name" sortable>
                <template #filter="{filterModel}">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>
            <Column :header="t('expire')" field="expire_date" filter-field="expire_date" data-type="date" sortable class="text-orange-700">
                <template #body ="{data}">
                    <Button v-if="data.expire_date" icon="pi pi-calendar" size="small" variant="link"></Button>
                    {{ formatDate(data.expire_date) }}
                </template>

                <template #filter="{ filterModel }">
                    <DatePicker v-model="filterModel.value" dateFormat="dd/mm/yy" :placeholder="t('search')" />
                </template>
            </Column>
            <Column :header="t('package')" field="package" sortable>
                <template #filter="{filterModel}">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>
            <Column :header="t('image')">
                <!-- <template #filter="{filterModel}">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template> -->
            </Column>
            <Column :header="t('category')" field="category_id" sortable>
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
            <Column :header="t('review')" field="review" sortable>
                <template #body="{data}">
                    <Rating readonly :model-value="data.review"></Rating>
                </template>
            </Column>
            <Column :header="t('remark')" field="description" sortable>
                <template #filter="{filterModel}">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
                </template>
            </Column>
            <Column :header="t('stock')" field="stock" sortable>
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
                    <!-- <i class="pi pi-users" style="color: slateblue; font-size: 1.7rem;"></i> -->
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
                    >
                    <template #header="{ chooseCallback, uploadCallback, clearCallback, files}">
                        <div class="flex flex-wrap justify-between items-center">
                            <div class="flex gap-2">
                                <Button @click="chooseCallback()" icon="pi pi-images" rounded variant="outlined" severity="secondary"></Button>
                                <Button @click="clearCallback()" icon="pi pi-times" rounded variant="outlined" severity="danger" :disabled="!files || files.length === 0"></Button>
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
                        <!-- <i class="pi pi-envelope" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-box" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="productForm.package"
                            :invalid="errors.package ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('package') }} </label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.package">{{ errors.package }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-phone" style="font-weight: bold; color: slateblue;"></i> -->
                        <Button icon="pi pi-calendar" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <DatePicker
                            show-clear
                            icon-display="input"
                            v-model="productForm.expire_date"
                            date-format="dd/mm/yy"
                            update-model-type="string"
                        >
                            
                        </DatePicker>
                        <label>{{ t('expire') }} </label>
                    </FloatLabel>
                </InputGroup>
                <!-- <Message severity="error" variant="simple" size="small" v-if="errors.phone">{{ errors.phone }}</Message> -->
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <!-- <i class="pi pi-address-book" style="font-weight: bold; color: slateblue;"></i> -->
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
                        <!-- <i class="pi pi-pencil" style="font-weight: bold; color: slateblue;"></i> -->
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
        middleware: 'auth'
    })
    import { FilterMatchMode, FilterOperator} from '@primevue/core/api'
    import type { FileUploadSelectEvent } from 'primevue/fileupload'
    import type { product } from '~/composables/useProduct'
    const productAction = useProduct()
    const { t } = useI18n()
    const { confirmDelete } = useConfirmDelete()
    const messageBox = MessageBox()
    const filters = ref()
    const loading = ref(false)
    const btnLoading = ref(false)
    const editMode = ref(false)
    const openDialog = ref(false)
    const selectProduct = ref<product[]>([])
    const productList = ref<product[]>([])
    const categoryOptions = ref<any>([])
    const srcFile = <any>ref([])
    const errors = reactive({code: '', name: '', expire_date: null, package: '', category_id: ''})
    const productForm = reactive<product>({id: 0, code: '', name: '', expire_date: null, package: '', description: '', stock: Math.floor(Math.random() * 1000), review: Math.floor(Math.random() * 100), category_id: null, images: []})
    const initFilters = () => {
        filters.value = {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },            
            code: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
            description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }]},
            review: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },            
            package: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
            expire_date: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
            category_id: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]}
        };
    }
    const parseDate = (value: string | null)=> {
        if (!value) return null

        const [day, month, year] = value.split('/')
        var date = new Date(Number(year), Number(month) - 1, Number(day))
        return date
    }
    const formatDate = (value: Date) => {
        if (!value) return ''
        return value.toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }
    const onRemoveTemplatingFile = (file: File, removeFileCallback: any, index: number) => {
        removeFileCallback(index);
    };
    function onFileSelect(event: FileUploadSelectEvent) {
        event.files.forEach((item: any) => {
            debugger
            srcFile.value.push(item);
        });
        productForm.images = srcFile.value
    }
    initFilters()
    const clearFilter = () => {
        initFilters();
    }
    const onSelectedItem = (item: any) => {
        openDialog.value = true
        editMode.value = true
        productForm.id = item.data.id
        productForm.code = item.data.code
        productForm.name = item.data.name
        productForm.expire_date = item.data.expire_date
        productForm.package = item.data.package
        productForm.description = item.data.description
        productForm.stock = item.data.stock
        productForm.category_id = item.data.category_id
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
        errors.category_id = ''
        errors.code = ''
        errors.name = ''
        errors.expire_date = null
        errors.package = ''
    }
    const getValueStock = (value: number) => {
        var status = ''
        if(value <= 25){
            status = 'Low'
        }else if(value > 25 && value <= 500){
            status = 'Medium'
        }else if(value > 500){
            status = 'Hight'
        }
            
        return status
    }
    const getSeverity = (value: number) => {
        if(value <= 25){
            return 'danger'
        }else if(value > 25 && value <= 500){
            return 'info'
        }else{
            return 'success'
        }
    }
    const getIconStock = (status: string) => {
        if(status == 'Low')
            return 'pi pi-arrow-down'
        else if(status == 'Medium')
            return 'pi pi-arrows-v'

        return 'pi pi-arrow-up'
    }
    const onOpenDialog = () => {
        openDialog.value = true
    }
    const successMessage = () => messageBox.success('Your data was saved successfully.')
    const getCategoryOption = async () => categoryOptions.value =  await productAction.category() 
    const getAllProduct = async () => { 
        loading.value = true; 
        await productAction.getAllProduct()
        .then((res: any) => { 
            productList.value = res.map((item: any) => ({
                ...item, 
                expire_date: parseDate(item.expire_date)
            })); 
            loading.value = false 
        })
        .catch((error: any) => {
            loading.value = false
        }) 
    }
    const create = async () => { 
        console.log(srcFile)
        loading.value = true; 
        btnLoading.value = true; 
        await productAction.create(productForm)
        .then((res: any) => {
            btnLoading.value = false; 
            loading.value = false; 
            successMessage(); 
            getAllProduct(); 
            close()})
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
            }})}
    const update = async () => { loading.value = true; btnLoading.value = true; await productAction.update(productForm.id, productForm).then((res: any) => {loading.value = false; btnLoading.value = false; getAllProduct(); close(); successMessage()}).catch((error: any)=> {loading.value = false; btnLoading.value = false; loading.value = false; 
                btnLoading.value = false; 
                let respondedData = error?.data?.data?.detail
                if(typeof respondedData != 'string' && respondedData.length > 0){
                    for(var i = 0; i < respondedData.length; i++){
                        let fieldName = respondedData[i].loc[1]
                        if(fieldName === 'name') errors.name = respondedData[i].msg
                        
                        if(fieldName === 'code') errors.code = respondedData[i].msg

                    }
            }})}
    const remove = () => { if(selectProduct.value.length < 0) return; confirmDelete( async () => {loading.value = true; var ids = selectProduct.value.map(e => e.id); await productAction.remove(ids).then((res: any) => { loading.value = false; getAllProduct(); successMessage(); selectProduct.value = []}).catch((error: any)=> {loading.value = false})})}
    
    onMounted(() => {
        getCategoryOption()
        getAllProduct()
    })
</script>