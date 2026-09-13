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
            :global-filter-fields="['username', 'status', 'email', 'created_at', 'updated_at']"
            filter-display="menu"
            data-key="id"
            @row-dblclick="onOpenDialogEdit"
            scrollable
            scroll-height="500px"
            row-hover
        >
            <Toolbar>
                <template #end>
                    <Button :label="t('btnCreate')" v-if="canCreate" icon="pi pi-plus" @click="openDialog = true"></Button>
                    <Button :label="t('btnDelete')" v-if="canDelete" icon="pi pi-trash" class="ml-2" @click="deleteMany"></Button>
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
            <Column :header="t('lblName')" field="username" style="min-width: 200px" sortable class="text-green-700 font-bold">
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
            <Column :header="t('position')" sortable></Column>
            <Column :header="t('lblPhone')" sortable></Column>
            <Column :header="t('email')" sortable field="email" class="text-blue-700 font-bold">
                <template #body="{ data }">
                    <div class="flex items-center gap-2 text-blue-700 font-bold py-2">
                        <i class="pi pi-envelope pi-spin"></i>
                        <span>{{ data.email }}</span>
                    </div>
                </template>
                <template #filter = "{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" placeholder="Search by email"></InputText>
                </template>
            </Column>
            <Column :header="t('role')" sortable field="role_id"  class="text-blue-700 font-bold">
                <template #body="{ data }">
                    <div class="">
                        <span>{{ data.role?.role_name }}</span>
                    </div>
                </template>
                <template #filter="{ filterModel }">
                    <Select 
                        v-model="filterModel.value" 
                        :options="roleList" 
                        option-label="role_name" 
                        option-value="id" 
                        :placeholder="t('search')" 
                        showClear
                    >
                    </Select>
                </template>
            </Column>
            <Column :header="t('active')" sortable field="status" data-type="boolean">
                <template #body="{ data }">
                    <i class="pi" :class="{ 'pi-check-circle text-green-500': data.status, 'pi-times-circle text-red-400': !data.status }"></i>
                </template>
                <template #filter="{ filterModel }">
                    <label for="verified-filter" class="font-bold"> Verified </label>
                    <Checkbox v-model="filterModel.value" :indeterminate="filterModel.value === null" binary inputId="verified-filter" />
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
            <template #empty>{{ t('empty') }}</template>
        </DataTable>

        <Dialog
            style="width: 500px;"
            :visible="openDialog"
            :closable="false"
        >
            
            <template #header>
                <Divider>
                    <Button icon="pi pi-user-plus" variant="link" size="large"></Button>
                    <span class="text-xl">{{ t('lblHeaderCreate').replace('[0]', t('user')) }}</span>
                </Divider>
            </template>
            
            <template #default>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            <Button icon="pi pi-user" variant="link"></Button>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputText
                                v-model="userForm.username"
                                :invalid="errors.username ? true : false"
                            >
                                
                            </InputText>
                            <label>{{ t('username') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.username">{{ errors.username }}</Message>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            <Button icon="pi pi-envelope" variant="link"></Button>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <InputText
                                v-model="userForm.email"
                                :invalid="errors.email ? true : false"
                            >
                                
                            </InputText>
                            <label>{{ t('email') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.email">{{ errors.email }}</Message>
                    <InputGroup class="mt-2">
                        <InputGroupAddon>
                            <Button icon="pi pi-shield" variant="link"></Button>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <Select
                                :options="roleList"
                                show-clear
                                v-model="userForm.role_id"
                                option-label="role_name"
                                option-value="id"
                            >
                                
                            </Select>
                            <label>{{ t('role') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <InputGroup class="my-2">
                        <InputGroupAddon>
                            <Button icon="pi pi-key" variant="link"></Button>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <Password
                                v-model="userForm.password"
                                toggle-mask
                                :invalid="errors.password ? true : false"
                            >
                                
                            </Password>
                            <label>{{ t('password') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.password">{{ errors.password }}</Message>
                    <InputGroup>
                        <InputGroupAddon>
                            <Button icon="pi pi-key" variant="link"></Button>
                        </InputGroupAddon>
                        <FloatLabel variant="on">
                            <Password
                                v-model="userForm.confirm_password"
                                toggle-mask
                                :invalid="errors.confirm_password ? true : false"
                            >
                                
                            </Password>
                            <label>{{ t('confirmPassword') }}</label>
                        </FloatLabel>
                    </InputGroup>
                    <Message severity="error" variant="simple" size="small" v-if="errors.confirm_password">{{ errors.confirm_password }}</Message>

                    <Checkbox binary v-model="userForm.status" class="mr-2">Active</Checkbox>
                    <label>{{t('active')}}</label>
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
        layout: 'dashboard',
        // middleware: 'auth'
    })
    import type { user } from '~/composables/useUsers';
    import type { role } from "~/composables/useRole";
    import {
        applyUserValidationErrors,
        createEmptyUserForm,
        createUserErrors,
        createUserFilters,
        type UserErrors,
        type UserForm
    } from '~/services/user.service'
    const { confirmDelete } = useConfirmDelete()
    const { t } = useI18n()
    const { hasPermission } = useFunction()
    const messageBox = MessageBox()
    const userList = ref<user[]>([])
    const roleList = ref<role[]>([])
    const userAction = useUsers()
    const openDialog = ref(false)
    const btnLoading = ref(false)
    const loading = ref(false)
    const editMode = ref(false)
    const selectUsers = ref([])
    const route = useRoute()
    const filters = ref()
    const canCreate = computed(() => hasPermission(route.name as string, 'create'))
    const canUpdate = computed(() => hasPermission(route.name as string, 'update'))
    const canDelete = computed(() => hasPermission(route.name as string, 'delete'))
    const canView = computed(() => hasPermission(route.name as string, 'access'))
    const errors = ref<UserErrors>(createUserErrors())
    const userForm = ref<UserForm>(createEmptyUserForm())
    const initFilters = () => {
        filters.value = createUserFilters();
    }
    initFilters()
    const clearFilter = () => {
        initFilters();
        selectUsers.value = []
    }
    const close = ()=>{
        editMode.value = false
        openDialog.value = false
        loading.value = false
        btnLoading.value = false
        errors.value = createUserErrors()
        userForm.value = createEmptyUserForm()
    }
    const onOpenDialogEdit = (item: any) => {
        if(canUpdate.value){
            editMode.value = true
            userForm.value.id = item.data.id
            userForm.value.username = item.data.username
            userForm.value.email = item.data.email
            userForm.value.status = item.data.status
            userForm.value.role_id = item.data.role_id
            openDialog.value = true
        }
    }
    const successMessage = () => messageBox.success(t('successMessage'))
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
            loading.value = false
            btnLoading.value = false
            errors.value = applyUserValidationErrors(error?.data?.data?.detail, errors.value)
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
            loading.value = false
            btnLoading.value = false
            errors.value = applyUserValidationErrors(error?.data?.data?.detail, errors.value)
        })
    }
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
                    messageBox.error(t('errorMessage'))
                })
            }
        )
    }
    const getRole = async () => {
        roleList.value = await userAction.getRoleList()
    }
    onMounted(() =>{
        if(canView.value){
            getRole()
            getUserList()
        }
    })
</script>
