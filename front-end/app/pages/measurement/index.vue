<template>
    <div id="measurement">
        <DataTable
            removable-sort
            resizable-columns
            reorderable-columns
            row-hover
            paginator
            size="small"
            :value="measurementList"
            v-model:selection="selectMeasurement"
            v-model:filter="filters"
            :global-filter-fields="['name', 'description', 'code', 'status']"
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
                <Button :label="t('btnDelete')" icon="pi pi-trash" class="mx-2" @click="removeMeasurement"></Button>
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
        
        <Column :header="t('status')" field="status" sortable style="min-width: 200px">
            <template #body="{ data }">
                    <i class="pi" :class="{ 'pi-check-circle text-green-500': data.status, 'pi-times-circle text-red-400': !data.status }"></i>
            </template>
            <template #filter="{ filterModel }">
                <label for="verified-filter" class="font-bold"> Verified </label>
                <Checkbox v-model="filterModel.value" :indeterminate="filterModel.value === null" binary inputId="verified-filter" />
            </template>
        </Column>
       
        
        <Column :header="t('remark')" field="description" sortable style="min-width: 200px">
            <template #filter="{filterModel}">
                <InputText v-model="filterModel.value" type="text" :placeholder="t('search')"></InputText>
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
                    <Button icon="pi pi-wrench" size="large" variant="link"  />
                    <span v-if="!editMode" class="ml-2 text-xl">{{ t('lblHeaderCreate').replace('[0]', t('measurement')) }}</span>
                    <span v-else class="ml-2 text-xl">{{ t('lblHeaderUpdate').replace('[0]', t('measurement')) }}</span>
                </Divider>
            </template>
            
            <template #default>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-wrench" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="measurementForm.code"
                            :invalid="errors.code ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('lblCode') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.code">{{ errors.code }}</Message>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-wrench" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="measurementForm.name"
                            :invalid="errors.name ? true : false"
                        >
                            
                        </InputText>
                        <label>{{ t('lblName') }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.name">{{ errors.name }}</Message>
                <InputGroup class="my-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-comment" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            v-model="measurementForm.description"
                            class="w-full"
                        >
                            
                        </Textarea>
                        <label>{{ t('description') }}</label>
                    </FloatLabel>
                </InputGroup>
                <Checkbox binary v-model="measurementForm.status" class="mr-2">Active</Checkbox>
                <label>{{t('active')}}</label>
            </template>
            <template #footer>
                <Button icon="pi pi-check" :loading="btnLoading" :label="t('btnSave')" size="small" type="submit" @click="editMode ? updateMeasurement() : createMeasurement()"></Button>
                <Button icon="pi pi-times" :label="t('btnCancel')" @click="close" size="small"></Button>
            </template>
        </Dialog>

    </div>
</template>
<script setup lang="ts">
    definePageMeta({
        layout: 'dashboard',
    })
    import { MeasurementService } from '~/services/measurement.service'
    import type { Measurement, MeasureError } from '~~/shared/types/measurement'
    const { create, getAll, remove, update } = useMeasurement()
    const { t } = useI18n()
    const { confirmDelete } = useConfirmDelete()
    const mesageBox = MessageBox()
    const btnLoading = ref(false)
    const loading = ref(false)
    const openDialog = ref(false)
    const editMode = ref(false)
    const close = () => { 
        openDialog.value = false
        editMode.value = false
        loading.value = false
        btnLoading.value = false
        errors.value = MeasurementService.measurementError()
        measurementForm.value = MeasurementService.createForm()
    }
    
    const errors = ref<MeasureError>(MeasurementService.measurementError())
    const measurementForm = ref<Measurement>(MeasurementService.createForm())
    const measurementList = ref<Measurement[]>([])
    
    const onOpenDialog = () => openDialog.value = true
    const selectMeasurement = ref([])
    const filters = ref()
    
    const initFilter = () => filters.value = MeasurementService.filters()
    initFilter()
    const clearFilter = () => { 
        selectMeasurement.value = []
        initFilter()
    }
    const successMessage = () => mesageBox.success(t('successMessage'))
    const errorMessage = () => mesageBox.error(t('errorMessage'))
    const warningMessage = () => mesageBox.warning(t('warningMessage'))
    const onSelectedItem = (item: any) => {
        measurementForm.value.id = item?.data?.id
        measurementForm.value.code = item?.data?.code
        measurementForm.value.name = item?.data?.name
        measurementForm.value.description = item?.data?.description
        measurementForm.value.status = item?.data?.status
        editMode.value = true
        openDialog.value = true
    }
    const getAllMeasurement = async () => {
        loading.value = true
        try{
            const res = await getAll()
            measurementList.value = res
        }catch(error){
            errorMessage()
        }
        finally{
            loading.value = false
        }
    }
    const createMeasurement = async () => { 
        loading.value = true
        btnLoading.value = true
        try{
            await create(measurementForm.value)
            successMessage()
            await getAllMeasurement()
            close()
        }catch(error: any){
            errors.value = MeasurementService.applyMeasurementValidationErrors(error?.data?.data?.detail, errors.value)
            if(!errors.value) errorMessage()
        }finally{
            btnLoading.value = false
            loading.value = false
        }
    }
    const updateMeasurement = async () => {
        loading.value = true
        btnLoading.value = true
        try{
            await update(measurementForm.value.id as number, measurementForm.value)
            successMessage()
            await getAllMeasurement()
            close()
        }
        catch(error: any){
            errors.value = MeasurementService.applyMeasurementValidationErrors(error?.data?.data?.detail, errors.value)
            if(!errors.value) errorMessage()
        }
        finally{
            loading.value = false
            btnLoading.value = false
        }
    }
    const removeMeasurement = () => {
        if(selectMeasurement.value.length == 0) return warningMessage()
        confirmDelete(
            async () => {
                try{
                    const ids = selectMeasurement.value.map((item: Measurement) => item.id) as number[]
                    await remove(ids)
                    successMessage()
                    await getAllMeasurement()
                }
                catch(error: any){
                    errors.value = MeasurementService.applyMeasurementValidationErrors(error?.data?.data?.detail, errors.value)
                    if(!errors.value) errorMessage()
                }finally{
                    selectMeasurement.value = []
                }
            }
        )
    }
    onMounted(getAllMeasurement)
</script>