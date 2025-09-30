<template>
    <div>
        <div class="container">
            <h2 class="page-title">航前质量监督检查记录表</h2>
            <p class="page-desc">请选择一个任务以查看或编辑其检查记录</p>

            <el-table :data="tableData" border class="table" header-cell-class-name="table-header" @row-click="handleRowClick">
                <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
                <el-table-column prop="task_name" label="航次任务名称" min-width="180"></el-table-column>
                <el-table-column prop="project" label="专项名称" min-width="180"></el-table-column>
                <el-table-column prop="task_code" label="任务编号" width="150"></el-table-column>
                <el-table-column prop="undertake" label="承担单位" min-width="200"></el-table-column>
                <el-table-column prop="leader" label="任务负责人" width="130"></el-table-column>
                <el-table-column label="操作" width="150" align="center">
                    <template #default="{ row }">
                        <el-button type="primary" size="small" @click="goToInspection(row.task_name)">
                            查看检查记录
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            
            <div class="pagination">
                <el-pagination 
                    background 
                    layout="total, prev, pager, next" 
                    :current-page="page.index"
                    :page-size="page.size" 
                    :total="page.total" 
                    @current-change="changePage">
                </el-pagination>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts" name="inspection-task-list">
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { fetchTasksNew as fetchTasks } from '@/api/task';

const router = useRouter();

interface Task {
    task_name: string;
    project?: string;
    task_code?: string;
    undertake?: string;
    leader?: string;
}

const tableData = ref<Task[]>([]);
const page = reactive({
    index: 1,
    size: 10,
    total: 0,
});

// 获取任务列表
const getData = async () => {
    try {
        // 携带当前用户ID（用户隔离）
        const userId = localStorage.getItem('userId');
        const params: any = {};
        if (userId) {
            params.user_id = userId;
        }
        
        const res = await fetchTasks(params);
        tableData.value = res.data.data.list;
        page.total = res.data.data.pageTotal;
    } catch (error: any) {
        ElMessage.error('获取任务列表失败');
    }
};

// 翻页
const changePage = (val: number) => {
    page.index = val;
    getData();
};

// 跳转到检查记录页面
const goToInspection = (task_name: string) => {
    router.push({
        name: 'inspection-record',
        params: { task_name }
    });
};

// 行点击事件
const handleRowClick = (row: Task) => {
    goToInspection(row.task_name);
};

onMounted(() => {
    getData();
});
</script>

<style scoped>
.container {
    padding: 30px;
    background-color: #fff;
    border-radius: 8px;
}

.page-title {
    font-size: 24px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 10px;
}

.page-desc {
    font-size: 14px;
    color: #909399;
    margin-bottom: 25px;
}

.table {
    width: 100%;
    margin-top: 20px;
}

:deep(.el-table tbody tr) {
    cursor: pointer;
}

:deep(.el-table tbody tr:hover) {
    background-color: #f5f7fa;
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

.pagination {
    margin-top: 25px;
    display: flex;
    justify-content: center;
}
</style>
