<template>
    <div id="role">
        <DataTable
            paginator
            :rows="20"
            :rowsPerPageOptions="[5, 10, 20, 50, 100, 250, 500, 1000, 5000]"
            removable-sort
            resizable-columns
            reorderable-columns
            column-resize-mode="fit"
            :value="roleList"
            :lazy="loading"
            size="small"
            striped-rows
            v-model:selection="selectedRoles"
            v-model:filters="filters"
            :global-filter-fields="['role_name', 'description', 'status', 'created_at', 'updated_at']"
            filter-display="menu"
            data-key="id"
            row-hover
            @row-dblclick="onOpenDialogEdit"
            scrollable
            scroll-height="600px"
            :virtual-scroller-options="{ itemSize: 46 }"
            paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            currentPageReportTemplate="{first} to {last} of {totalRecords}"
        >
            <Toolbar>
                <template #end>
                    <Button :label="t('btnCreate')" v-if="canCreate" icon="pi pi-plus" @click="openCreateDialog"></Button>
                    <Button :label="t('btnDelete')" v-if="canDelete" icon="pi pi-trash" class="ml-2" @click="deleteMany"></Button>
                </template>
            </Toolbar>

            <template #header>
                <div class="flex justify-between">
                    <IconField>
                        <InputIcon>
                            <i class="pi pi-search"></i>
                        </InputIcon>
                        <InputText :placeholder="t('search')" v-model="filters['global'].value"></InputText>
                    </IconField>
                    <Button icon="pi pi-filter-slash" @click="clearFilter" variant="link"></Button>
                </div>
            </template>

            <Column selection-mode="multiple" header-style="width: 2rem"></Column>

            <Column :header="t('role')" field="role_name" sortable>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')" />
                </template>
            </Column>

            <Column :header="t('description')" field="description" sortable>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" :placeholder="t('search')" />
                </template>
            </Column>

            <Column :header="t('status')" field="status" sortable data-type="boolean">
                <template #body="{ data }">
                    <i
                        class="pi"
                        :class="{
                            'pi-check-circle text-green-500': data.status,
                            'pi-times-circle text-red-400': !data.status,
                        }"
                    ></i>
                    <span class="ml-2">{{ data.status ? 'Active' : 'Inactive' }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <label class="font-bold mr-2">Active</label>
                    <Checkbox
                        v-model="filterModel.value"
                        :indeterminate="filterModel.value === null"
                        binary
                    />
                </template>
            </Column>

            <Column :header="t('created_at')" field="created_at" sortable>
                <template #body="{ data }">
                    {{ data.created_at }}
                </template>
            </Column>

            <Column :header="t('updated_at')" field="updated_at" sortable>
                <template #body="{ data }">
                    {{ data.updated_at }}
                </template>
            </Column>

            <template #empty>{{ t('empty') }}</template>
        </DataTable>

        <Dialog
            style="width: 520px;"
            :visible="openDialog"
            :closable="false"
        >
            <template #header>
                <Divider>
                    <Button icon="pi pi-shield" size="large" variant="link"></Button>
                    <span class="ml-2 text-xl">
                        {{ editMode ? t('lblHeaderUpdate').replace('[0]', roleLabel) : t('lblHeaderCreate').replace('[0]', roleLabel) }}
                    </span>
                </Divider>
            </template>

            <template #default>
                <InputGroup class="mt-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-shield" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText
                            v-model="roleForm.role_name"
                            :invalid="Boolean(errors.role_name)"
                        />
                        <label>{{ roleLabel }} *</label>
                    </FloatLabel>
                </InputGroup>
                <Message severity="error" variant="simple" size="small" v-if="errors.role_name">
                    {{ errors.role_name }}
                </Message>

                <InputGroup class="my-2">
                    <InputGroupAddon>
                        <Button icon="pi pi-pencil" size="small" variant="link"></Button>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Textarea
                            v-model="roleForm.description"
                            class="w-full"
                            rows="3"
                        />
                        <label>{{ t('description') }}</label>
                    </FloatLabel>
                </InputGroup>

                <div class="flex items-center gap-3 py-2">
                    <Checkbox binary v-model="roleForm.status" inputId="role-status" />
                    <label for="role-status">{{ t('active') }}</label>
                </div>
                
                <Card>
                    <template #header>
                        <div class="ml-5 mt-2">
                            {{ t('menu') }}
                        </div>
                    </template>
                    <template #content>
                        <Tree 
                            v-model:selectionKeys="selectedMenuKeys" 
                            :value="menuList as any" 
                            selectionMode="checkbox" 
                            class="w-full md:w-30rem max-h-[250px] overflow-auto border border-gray-200 rounded-lg"
                            :meta-key-selection="false"
                        >
                            <template #default="slotProps">
                                <div class="flex items-center gap-2">
                                    <span>{{ slotProps.node.label }}</span>
                                </div>
                            </template>
                        </Tree>
                    </template>
                </Card>
            </template>

            <template #footer>
                <Button
                    icon="pi pi-check"
                    :loading="btnLoading"
                    :label="t('btnSave')"
                    size="small"
                    type="submit"
                    @click="editMode ? update() : create()"
                    
                ></Button>
                <Button
                    icon="pi pi-times"
                    :label="t('btnCancel')"
                    @click="close"
                    size="small"
                ></Button>
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
definePageMeta({
    layout: 'dashboard',
})

import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import type { role } from '~/composables/useRole'
import type { MenuNode } from '~~/store/state'

const { confirmDelete } = useConfirmDelete()
const { t } = useI18n()
const messageBox = MessageBox()
const roleAction = useRole()
const { getMenuTree } = useMenu()
const { hasPermission } = useFunction()
const roleLabel = computed(() => {
    const translated = t('role')
    return translated === 'role' ? 'Role' : translated
})
const route = useRoute()
const selectedMenuKeys = ref<any>({});
const selectedRoles = ref<role[]>([])
const roleList = ref<role[]>([])
const loading = ref(false)
const btnLoading = ref(false)
const editMode = ref(false)
const openDialog = ref(false)
const filters = ref()
const errors = ref({ role_name: '' })
const menuList = ref<MenuNode[]>([])
const canAccess = computed(() => hasPermission(route.name as string, 'access'))
const canCreate = computed(() => hasPermission(route.name as string, 'create'))
const canUpdate = computed(() => hasPermission(route.name as string, 'update'))
const canDelete = computed(() => hasPermission(route.name as string, 'delete'))

const createEmptyRole = (): role => ({
    id: 0,
    role_name: '',
    description: '',
    status: true,
    menu: []
})

const roleForm = ref<role>(createEmptyRole())

const initFilters = () => {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        role_name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
        description: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] },
        status: { value: null, matchMode: FilterMatchMode.EQUALS },
    }
}

initFilters()

const clearFilter = () => {
    initFilters()
}

const resetForm = () => {
    editMode.value = false
    openDialog.value = false
    loading.value = false
    btnLoading.value = false
    errors.value = { role_name: '' }
    roleForm.value = createEmptyRole()
    selectedMenuKeys.value = {}
}

const close = () => {
    resetForm()
}

const selectedMenuIds = computed<number[]>(() => {
    return Object.keys(selectedMenuKeys.value)
        .filter(key => selectedMenuKeys.value[key].checked === true || selectedMenuKeys.value[key].partialChecked === true)
        .map(key => parseInt(key, 10))
        .filter(id => !isNaN(id));
});

const loadMenuData = (menuTreeIds: number[]) => {
    const newSelectionMap = {} as any

    menuTreeIds.forEach((id: number) => {
        newSelectionMap[String(id)] = {
            checked: true,
            partialChecked: false
        };
    });

    selectedMenuKeys.value = newSelectionMap;
};

const openCreateDialog = () => {
    editMode.value = false
    errors.value = { role_name: '' }
    roleForm.value = createEmptyRole()
    openDialog.value = true
}
const onOpenDialogEdit = (item: any) => {
    if(canUpdate.value){
        editMode.value = true
        roleForm.value = {
            id: item.data.id,
            role_name: item.data.role_name,
            description: item.data.description ?? '',
            status: Boolean(item.data.status),
            created_at: item.data.created_at,
            updated_at: item.data.updated_at,
            menu: item.data.menu
        }
        loadMenuData(item.data.menu)
        errors.value = { role_name: '' }
        openDialog.value = true
    }
    
}

const successMessage = () => messageBox.success(t('successMessage'))

const getRoleList = async () => {
    loading.value = true
    try {
        roleList.value = await roleAction.roleList()
    } catch (error) {
        messageBox.error('Failed to load role data.')
    } finally {
        loading.value = false
    }
}

const getMenuList = async () => {
    try{
        menuList.value = await getMenuTree() as MenuNode[]
        
    }catch(e){
        messageBox.error('Failed to load menu data.')
    }finally{

    }
}

const getErrorDetail = (error: any) => {
    return error?.data?.data?.detail ?? error?.data?.detail ?? error?.response?._data?.detail ?? null
}

const applyValidationErrors = (detail: any) => {
    if (typeof detail === 'string') {
        messageBox.error(detail)
        return
    }

    if (!Array.isArray(detail)) {
        return
    }

    for (const item of detail) {
        const fieldName = item?.loc?.[1]
        if (fieldName === 'role_name') {
            errors.value.role_name = item.msg
        }
    }
}

const create = async () => {
    roleForm.value.menu = selectedMenuIds.value
    btnLoading.value = true
    loading.value = true

    try {
        await roleAction.create(roleForm.value)
        await getRoleList()
        successMessage()
        close()
    } catch (error: any) {
        applyValidationErrors(getErrorDetail(error))
    } finally {
        loading.value = false
        btnLoading.value = false
    }
}

const update = async () => {
    roleForm.value.menu = selectedMenuIds.value
    btnLoading.value = true
    loading.value = true
    console.log(roleForm.value)
    try {
        await roleAction.update(roleForm.value.id, roleForm.value)
        await getRoleList()
        successMessage()
        close()
    } catch (error: any) {
        applyValidationErrors(getErrorDetail(error))
    } finally {
        loading.value = false
        btnLoading.value = false
    }
}

const deleteMany = () => {
    if (!selectedRoles.value.length) {
        return
    }

    confirmDelete(async () => {
        loading.value = true
        try {
            const roleIds = selectedRoles.value.map((item: role) => item.id)
            await roleAction.removeMany(roleIds)
            selectedRoles.value = []
            await getRoleList()
            successMessage()
        } catch (error) {
            messageBox.error('An issue have occurred please inform technical support.')
        } finally {
            loading.value = false
        }
    })
}

onMounted(() => {
    getRoleList()
    getMenuList()
})

</script>
