<template>
    <div>
        <div class="container">
            <table-search :query="query" :options="searchOpt" :search="handleSearch"></table-search>
            <table-custom
                :columns="columns"
                :tableData="tableData"
                :total="page.total"
                :viewFunc="handleDetail"
                :delFunc="handleDelete"
                :editFunc="handleEdit"
                :currentPage="page.index"
                :changePage="changePage"
            >
                <template #toolbarBtn>
                    <el-button type="primary" :icon="CirclePlus" @click="handleAdd">新增</el-button>
                </template>
            </table-custom>
            <el-dialog :title="isEdit ? '编辑任务' : '新增任务'" v-model="visible" width="900px" destroy-on-close
                :close-on-click-modal="false" @close="closeDialog">
                <table-edit :form-data="rowData" :options="options" :edit="isEdit" :update="updateData" />
            </el-dialog>
        </div>
    </div>
</template>

<script setup lang="ts" name="task-manage">
import { ref, reactive, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { CirclePlus } from '@element-plus/icons-vue';
import TableCustom from '@/components/table-custom.vue';
import TableEdit from '@/components/table-edit.vue';
import TableSearch from '@/components/table-search.vue';
import { FormOption, FormOptionList } from '@/types/form-option';
import { fetchTasksNew, createTaskNew, updateTaskNew, deleteTaskNew } from '@/api/task';

// 任务接口
interface Task {
    task_name: string;
    project?: string;
    task_code?: string;
    undertake?: string;
    participant?: string;
    ship?: string;
    leader?: string;
    chief_scientist?: string;
    superintendent?: string;
    superintended?: string;
    executiontime?: string;
    subject?: string;
}

// 查询相关
const query = reactive({
    task_name: '',
});
const searchOpt = ref<FormOptionList[]>([
    { 
        type: 'input', 
        label: '任务名称：', 
        prop: 'task_name',
        placeholder: '请输入任务名称关键词'
    }
])

// 搜索按钮
const handleSearch = () => {
    page.index = 1;
    getData();
};

// 表格相关
let columns = ref([
    { type: 'index', label: '序号', width: 80, align: 'center' },
    { prop: 'task_name', label: '航次任务名称' },
    { prop: 'project', label: '专项名称' },
    { prop: 'task_code', label: '航次任务编号', width: 150 },
    { prop: 'undertake', label: '航次承担单位' },
    { prop: 'ship', label: '调查船', width: 150 },
    { prop: 'leader', label: '任务负责人', width: 130 },
    { prop: 'operator', label: '操作', width: 220 },
])
const page = reactive({
    index: 1,
    size: 10,
    total: 0,
})
const tableData = ref<Task[]>([]);

// 获取数据
const getData = async () => {
    try {
        const params: any = {};
        
        // 携带当前用户ID（用户隔离）
        const userId = localStorage.getItem('userId');
        if (userId) {
            params.user_id = userId;
        }
        
        if (query.task_name) {
            params.task_name = query.task_name;
        }
        
        const res = await fetchTasksNew(params);
        tableData.value = res.data.data.list;
        page.total = res.data.data.pageTotal;
        
        if (tableData.value.length === 0 && query.task_name) {
            ElMessage.warning(`未找到任务名称包含"${query.task_name}"的任务`);
        }
    } catch (error: any) {
        ElMessage.error('获取数据失败');
    }
};
getData();

const changePage = (val: number) => {
    page.index = val;
    getData();
};

// 新增/编辑弹窗相关
const visible = ref(false);
const isEdit = ref(false);
const rowData = ref({});

// 动态表单配置
const options = computed<FormOption>(() => ({
    labelWidth: '130px',
    span: 12,
    list: [
        { 
            type: 'input', 
            label: '航次任务名称', 
            prop: 'task_name', 
            required: true, 
            disabled: isEdit.value,
            placeholder: '请输入航次任务名称'
        },
        { 
            type: 'input', 
            label: '专项名称', 
            prop: 'project',
            placeholder: '请输入专项名称'
        },
        { 
            type: 'input', 
            label: '航次任务编号', 
            prop: 'task_code',
            placeholder: '请输入航次任务编号'
        },
        { 
            type: 'input', 
            label: '航次承担单位', 
            prop: 'undertake',
            placeholder: '请输入承担单位'
        },
        { 
            type: 'input', 
            label: '航次参与单位', 
            prop: 'participant',
            placeholder: '请输入参与单位'
        },
        { 
            type: 'input', 
            label: '调查船', 
            prop: 'ship',
            placeholder: '请输入调查船名称'
        },
        { 
            type: 'input', 
            label: '任务负责人', 
            prop: 'leader',
            placeholder: '请输入负责人'
        },
        { 
            type: 'input', 
            label: '首席科学家', 
            prop: 'chief_scientist',
            placeholder: '请输入首席科学家'
        },
        { 
            type: 'input', 
            label: '随船监督员', 
            prop: 'superintendent',
            placeholder: '请输入随船监督员'
        },
        { 
            type: 'input', 
            label: '随船监督', 
            prop: 'superintended',
            placeholder: '请输入随船监督'
        },
        { 
            type: 'input', 
            label: '执行时间', 
            prop: 'executiontime', 
            span: 24,
            placeholder: '例如：2025-01-15 至 2025-02-20'
        },
        { 
            type: 'input', 
            label: '任务学科', 
            prop: 'subject',
            placeholder: '请输入任务学科'
        },
    ]
}))

const handleAdd = () => {
    isEdit.value = false;
    rowData.value = {};
    visible.value = true;
}

const handleEdit = (row: Task) => {
    isEdit.value = true;
    rowData.value = { ...row };
    visible.value = true;
}

const handleDetail = (row: Task) => {
    ElMessage.info('查看详情功能待实现');
}

const closeDialog = () => {
    visible.value = false;
}

const updateData = async (formData: any) => {
    try {
        // 携带当前用户ID（用户隔离）
        const userId = localStorage.getItem('userId');
        if (userId) {
            formData.user_id = parseInt(userId);
        }
        
        if (isEdit.value) {
            await updateTaskNew(formData.task_name, formData);
            ElMessage.success('更新成功');
        } else {
            await createTaskNew(formData);
            ElMessage.success('创建成功');
        }
        closeDialog();
        getData();
    } catch (error: any) {
        ElMessage.error(error.response?.data?.message || '操作失败');
    }
};

const handleDelete = async (row: Task) => {
    try {
        await ElMessageBox.confirm('确定要删除该任务吗？', '提示', { type: 'warning' });
        await deleteTaskNew(row.task_name);
        ElMessage.success('删除成功');
        getData();
    } catch (error: any) {
        if (error !== 'cancel') {
            ElMessage.error(error.response?.data?.message || '删除失败');
        }
    }
}
</script>

<style scoped>
.container {
    padding: 30px;
    background-color: #fff;
    border-radius: 8px;
}

/* 表格样式优化 */
:deep(.el-table) {
    margin-top: 20px;
}

:deep(.el-table th) {
    background-color: #f5f7fa !important;
    color: #606266;
    font-weight: 600;
    text-align: center;
}

:deep(.el-table td) {
    text-align: center;
    padding: 16px 0;
}

:deep(.el-table .cell) {
    padding: 0 12px;
    line-height: 1.8;
}

/* 按钮样式 */
:deep(.el-button) {
    margin: 0 4px;
}

/* 搜索框样式 */
:deep(.table-search) {
    margin-bottom: 25px;
}

:deep(.el-form-item) {
    margin-bottom: 18px;
}

/* 分页器样式 */
:deep(.el-pagination) {
    margin-top: 25px;
    justify-content: center;
}
</style>
