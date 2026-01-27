<template>
    <div id="user">
        
        <DataTable
            paginator 
            :rows="20" 
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            removable-sort
            resizable-columns
            reorderable-columns
            column-resize-mode="fit"
            :value="userList"
            :lazy="loading"
            size="small"
            striped-rows
            v-model:selection="selectUsers"
            v-model:filters="filters"
            :global-filter-fields="['username', 'status', 'email']"
            filter-display="menu"
            data-key="id"
            @row-dblclick="onOpenDialogEdit"
            scrollable
            scroll-height="600px"
            :virtual-scroller-options="{ itemSize: 46 }"
            row-hover
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
                        <InputText placeholder="Search" v-model="filters['global'].value"></InputText>
                    </IconField>
                    <Button icon="pi pi-filter-slash" @click="clearFilter" variant="link"></Button>
                </div>
            </template>
            <Column selection-mode="multiple"  header-style="width: 2rem"></Column>
            <Column header="Name" field="username" style="min-width: 200px" sortable class="text-green-700 font-bold">
                <template #body ="{ data }">
                    <div class="text-green-700 font-bold">
                        <i class="pi pi-user"></i>
                        {{ data.username }}
                    </div>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" placeholder="Search by name" />
                </template>
            </Column>
            <Column header="Position" sortable></Column>
            <Column header="Phone" sortable></Column>
            <Column header="Email" sortable field="email" class="text-blue-700 font-bold">
                <template #body="{ data }">
                    <div class="flex items-center gap-2 text-blue-700 font-bold bg-green-100 py-2">
                        <i class="pi pi-envelope pi-spin"></i>
                        <span>{{ data.email }}</span>
                    </div>
                </template>
                <template #filter = "{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" placeholder="Search by email"></InputText>
                </template>
            </Column>
            <Column header="Active" sortable field="status" data-type="boolean">
                <template #body="{ data }">
                    <i class="pi" :class="{ 'pi-check-circle text-green-500': data.status, 'pi-times-circle text-red-400': !data.status }"></i>
                </template>
                <template #filter="{ filterModel }">
                    <label for="verified-filter" class="font-bold"> Verified </label>
                    <Checkbox v-model="filterModel.value" :indeterminate="filterModel.value === null" binary inputId="verified-filter" />
                </template>
            </Column>

            <template #empty>Data Not Found</template>
        </DataTable>

        <Dialog
            style="width: 500px;"
            :visible="openDialog"
            :closable="false"
        >
            
            <template #header>
                <Divider>
                    <i class="pi pi-user-plus" style="color: slateblue; font-size: 1.7rem;"></i>
                    <span class="ml-2 text-xl">Create new user</span>
                </Divider>
            </template>
            
            <template #default>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            <i class="pi pi-user" style="font-weight: bold; color: slateblue;"></i>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputText
                                v-model="userForm.username"
                                :invalid="errors.username ? true : false"
                            >
                                
                            </InputText>
                            <label>Username</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.username">{{ errors.username }}</Message>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            <i class="pi pi-envelope" style="font-weight: bold; color: slateblue;"></i>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputText
                                v-model="userForm.email"
                                :invalid="errors.email ? true : false"
                            >
                                
                            </InputText>
                            <label>Email</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.email">{{ errors.email }}</Message>
                    <InputGroup class="my-2">
                        <InputGroupAddon>
                            <i class="pi pi-key" style="font-weight: bold; color: slateblue;"></i>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <Password
                                v-model="userForm.password"
                                toggle-mask
                                :invalid="errors.password ? true : false"
                            >
                                
                            </Password>
                            <label>Password</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.password">{{ errors.password }}</Message>
                    <InputGroup>
                        <InputGroupAddon>
                            <i class="pi pi-key" style="font-weight: bold; color: slateblue;"></i>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <Password
                                v-model="userForm.confirm_password"
                                toggle-mask
                                :invalid="errors.confirm_password ? true : false"
                            >
                                
                            </Password>
                            <label>Comfirm Password</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.confirm_password">{{ errors.confirm_password }}</Message>

                    <Checkbox binary v-model="userForm.status" class="mr-2">Active</Checkbox>
                    <label>Active</label>
            </template>
            <template #footer>
                <Button icon="pi pi-check" :loading="btnLoading" label="Save" size="small" type="submit" @click="editMode ? update() : create()"></Button>
                <Button icon="pi pi-times" label="Cancel" @click="close" size="small"></Button>
            </template>
        </Dialog>
    </div>
</template>
<script setup lang="ts">
    definePageMeta({
        layout: 'dashboard',
        middleware: 'auth'
    })
    import type { user } from '~/composables/useUsers';
    import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
    const { confirmDelete } = useConfirmDelete()
    const { t } = useI18n()
    const messageBox = MessageBox()
    const userList = ref<user[]>([])
    const userAction = useUsers()    
    const openDialog = ref(false)
    const btnLoading = ref(false)
    const loading = ref(false)
    const editMode = ref(false)
    const selectUsers = ref([])
    const filters = ref()
    const errors = ref({username: '', email: '', password: '', confirm_password: ''})
    const userForm = ref<user>({ id: 0, username: '', email: '', password: '', confirm_password: '',status: true})
    const initFilters = () => {
        filters.value = {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            username: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },            
            status: { value: null, matchMode: FilterMatchMode.EQUALS },
            email: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH}]}
        };
    }
    initFilters()
    const clearFilter = () => {
        initFilters();
    }
        //========================Method===========================
    const close = ()=>{
        editMode.value = false
        openDialog.value = false
        loading.value = false
        btnLoading.value = false
        errors.value = {username: '', email: '', password: '', confirm_password: ''}
        userForm.value = { id: 0, username: '', email: '', password: '', confirm_password: '',status: true}
    }
    const onOpenDialogEdit = (item: any) => {
        editMode.value = true
        userForm.value.id = item.data.id
        userForm.value.username = item.data.username
        userForm.value.email = item.data.email
        userForm.value.status = item.data.status
        openDialog.value = true
    }
    const successMessage = () => messageBox.success('Your data was saved successfully.')
    const getUserList = async () => {
        loading.value = true
        userList.value = await userAction.userList()
        loading.value = false
    }
    const create = async () => {
        btnLoading.value = true
        loading.value = true
        await userAction.create(userForm.value)
        .then((res) => {
            getUserList()
            successMessage()
            btnLoading.value = false
            close()
        })
        .catch((error: any) => {
            let respondedData = error?.data?.data.detail
            if(respondedData){
                for(var i = 0; i < respondedData.length; i++){
                    let fieldName = respondedData[i].loc[1]
                    if(fieldName === 'username') errors.value.username = respondedData[i].msg
                    
                    if(fieldName === 'email') errors.value.email = respondedData[i].msg

                    if(fieldName === 'password') errors.value.password = respondedData[i].msg
                    
                    if(fieldName === 'confirm_password') errors.value.confirm_password = respondedData[i].msg
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
        await userAction.update(userForm.value.id,userForm.value)
        .then((res) =>{
            getUserList()
            close()
            loading.value = false
            btnLoading.value = false
            successMessage()
        })
        .catch((error: any) =>{
            let respondedData = error?.data?.data.detail
            if(respondedData){
                for(var i = 0; i < respondedData.length; i++){
                    let fieldName = respondedData[i].loc[1]
                    if(fieldName === 'username') errors.value.username = respondedData[i].msg
                    
                    if(fieldName === 'email') errors.value.email = respondedData[i].msg

                    if(fieldName === 'password') errors.value.password = respondedData[i].msg
                    
                    if(fieldName === 'confirm_password') errors.value.confirm_password = respondedData[i].msg
                }
            }
            loading.value = false
            btnLoading.value = false
        })
        const remove = async () =>{
            btnLoading.value = true
            loading.value = true
            await userAction.removeMany(selectUsers.value)
            .then((res) => {
                getUserList()
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
        if(!selectUsers.value.length) return

        confirmDelete(
            async () => {
                loading.value = true
                const userIds = selectUsers.value.map((e: any) => e.id)
                await userAction.removeMany(userIds)
                .then( async () => {
                    await getUserList()
                    successMessage()
                })
                .catch((error: any) => {
                    loading.value = false
                    messageBox.error('An issue have occurred please inform technicial support.')
                })
            }
        )
    }
    onMounted(() =>{
        getUserList()
    })
</script>
