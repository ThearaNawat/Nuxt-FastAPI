<template>
    <div id="line-bot">
        <DataTable
            removable-sort
            resizable-columns
            reorderable-columns
            row-hover
            :value="data"
            paginator
            size="small"
            :global-filter-fields="['user_name', 'group_name', 'question', 'answer', 'date_time']"
            filter-display="menu"
            :rows="20" 
            :rowsPerPageOptions="[5, 10, 20, 50,100,250,500,1000,5000]" 
            scrollable
            scroll-height="600px"
            paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            currentPageReportTemplate="{first} to {last} of {totalRecords}"
            show-gridlines
            :virtual-scroller-options="{ itemSize: 44}"
        >
            <Toolbar>
                <template #end>
                    <Button :label="t('btnCreate')" icon="pi pi-plus"></Button>
                    <Button :label="t('btnDelete')" icon="pi pi-trash" class="mx-2"></Button>
                    <Button :label="t('btnExport')" icon="pi pi-file-excel"></Button>
                </template>
            </Toolbar>
            <template #header>
                <div class="flex justify-between">
                    <Button icon="pi pi-filter-slash" variant="link"></Button>
                </div>
            </template>
            <template #empty>{{ t('empty') }}</template>
            <Column field="user_name" header="User Name" frozen sortable style="width: 20%; height: 44px"></Column>
            <Column field="group_name" header="Group Name" frozen sortable style="width: 20%; height: 44px"></Column>
            <Column field="chat_type" header="Chat Type" frozen sortable style="width: 20%; height: 44px"></Column>
            <Column field="date_time" header="Date Time" sortable style="width: 20%; height: 44px"></Column>
            <Column field="question" header="Question" sortable style="width: 20%; height: 44px"></Column>
            <Column field="answer" header="Answer" sortable style="width: 20%; height: 44px"></Column>
            
            
        </DataTable>
        
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        middleware: 'auth',
        layout: 'dashboard',
    });
    import type { LineMessage } from '~/composables/useLineSocket';
    const { messages, connect } = useLineSocket();
    const { t } = useI18n();
    const formatDate = (date: Date) => {}
    const data = ref<LineMessage[]>([]);
    
    onMounted(() => {
        connect();
        data.value = messages.value;
    });
</script>

<style lang="scss" scoped>

</style>