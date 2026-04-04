<template>
    <div class="investigation-personnel">
        <!-- 筛选区域 -->
        <div class="filter-section">
            <el-form :model="filterForm" inline class="filter-form">
                <el-form-item label="姓名:">
                    <el-input v-model="filterForm.name" placeholder="请输入姓名" clearable style="width: 150px"></el-input>
                </el-form-item>
                <el-form-item label="性别:">
                    <el-select v-model="filterForm.sex" placeholder="请选择性别" clearable style="width: 120px">
                        <el-option label="男" value="男"></el-option>
                        <el-option label="女" value="女"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="职称:">
                    <el-select v-model="filterForm.professional_title" placeholder="请选择职称" clearable style="width: 150px">
                        <el-option label="高级工程师" value="高级工程师"></el-option>
                        <el-option label="工程师" value="工程师"></el-option>
                        <el-option label="助理工程师" value="助理工程师"></el-option>
                        <el-option label="研究员" value="研究员"></el-option>
                        <el-option label="副研究员" value="副研究员"></el-option>
                        <el-option label="助理研究员" value="助理研究员"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="工作单位:">
                    <el-select v-model="filterForm.employer" placeholder="请选择工作单位" clearable style="width: 200px">
                        <el-option label="海洋研究所" value="海洋研究所"></el-option>
                        <el-option label="海洋大学" value="海洋大学"></el-option>
                        <el-option label="海洋局" value="海洋局"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="从事专业:">
                    <el-select v-model="filterForm.specialty" placeholder="请选择专业" clearable style="width: 150px">
                        <el-option label="海洋地质" value="海洋地质"></el-option>
                        <el-option label="海洋化学" value="海洋化学"></el-option>
                        <el-option label="物理海洋" value="物理海洋"></el-option>
                        <el-option label="海洋生物" value="海洋生物"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <el-form :model="filterForm" inline class="filter-form">
                <el-form-item label="操作仪器:">
                    <el-input v-model="filterForm.instruments" placeholder="请输入操作仪器" clearable style="width: 200px"></el-input>
                </el-form-item>
                <el-form-item label="航次任务名称:">
                    <el-input v-model="filterForm.task_name" placeholder="请输入航次任务名称" clearable style="width: 200px"></el-input>
                </el-form-item>
                <el-form-item label="出生年月:">
                    <el-date-picker
                        v-model="filterForm.birthdate_range"
                        type="daterange"
                        range-separator="至"
                        start-placeholder="开始日期"
                        end-placeholder="结束日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                        style="width: 240px"
                    />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">查询</el-button>
                    <el-button @click="handleReset">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 操作栏 -->
        <div class="toolbar">
            <div class="toolbar-left">
                <el-button type="warning" :icon="Download" @click="handleExport">导出Excel</el-button>
            </div>
            <div class="toolbar-right">
                <span class="info-text">数据来源：航前调查人员资质一览表 + 航中外业调查人员表</span>
            </div>
        </div>

        <!-- 表格 -->
        <el-table
            ref="tableRef"
            :data="tableData"
            border
            stripe
            class="investigation-personnel-table"
            @selection-change="handleSelectionChange"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
            <el-table-column prop="task_name" label="航次名称" min-width="200">
                <template #default="{ row }">
                    <span>{{ row.task_name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="name" label="姓名" width="120" align="center">
                <template #default="{ row }">
                    <span>{{ row.name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="sex" label="性别" width="80" align="center">
                <template #default="{ row }">
                    <span>{{ row.sex }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="birthdate" label="出生年月" width="120" align="center">
                <template #default="{ row }">
                    <span>{{ row.birthdate }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="professional_title" label="职称" width="120" align="center">
                <template #default="{ row }">
                    <span>{{ row.professional_title }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="employer" label="工作单位" min-width="200">
                <template #default="{ row }">
                    <span>{{ row.employer }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="specialty" label="从事专业" min-width="150">
                <template #default="{ row }">
                    <span>{{ row.specialty }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="instruments" label="操作仪器" min-width="200">
                <template #default="{ row }">
                    <span>{{ row.instruments }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="training" label="培训情况" min-width="150">
                <template #default="{ row }">
                    <span>{{ row.training }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="remarks" label="备注" min-width="150">
                <template #default="{ row }">
                    <span>{{ row.remarks }}</span>
                </template>
            </el-table-column>
            <el-table-column label="数据来源" width="150" align="center">
                <template #default="{ row }">
                    <el-tag 
                        :type="row.source_type === '航前+航中' ? 'warning' : (row.source_type === '航前' ? 'primary' : 'success')"
                        size="large"
                    >
                        {{ row.source_type }}
                    </el-tag>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
            <el-pagination
                v-model:current-page="pagination.page"
                v-model:page-size="pagination.pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="pagination.total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onActivated } from 'vue';
import { ElMessage } from 'element-plus';
import { Download } from '@element-plus/icons-vue';
import { fetchInvestigationPersonnelList, exportInvestigationPersonnel } from '@/api/investigation-personnel';
import * as XLSX from 'xlsx';

// 筛选表单
const filterForm = reactive({
    name: '',
    sex: '',
    professional_title: '',
    employer: '',
    specialty: '',
    instruments: '',
    task_name: '',
    birthdate_range: []
});

// 表格数据
const tableData = ref([]);
const selectedRows = ref([]);
const tableRef = ref();

// 分页
const pagination = reactive({
    page: 1,
    pageSize: 10,
    total: 0
});

// 加载数据
const loadData = async () => {
    try {
        const params = {
            page: pagination.page,
            page_size: pagination.pageSize,
            name: filterForm.name,
            sex: filterForm.sex,
            professional_title: filterForm.professional_title,
            employer: filterForm.employer,
            specialty: filterForm.specialty,
            instruments: filterForm.instruments,
            task_name: filterForm.task_name,
            birthdate_start: filterForm.birthdate_range?.[0] || '',
            birthdate_end: filterForm.birthdate_range?.[1] || ''
        };
        
        const res = await fetchInvestigationPersonnelList(params);
        if (res.code === 200) {
            tableData.value = res.data.list;
            pagination.total = res.data.total;
        } else {
            ElMessage.error(res.message || '获取数据失败');
        }
    } catch (error: any) {
        console.error('获取调查人员列表失败:', error);
        ElMessage.error('获取数据失败: ' + (error.message || '未知错误'));
    }
};

// 搜索
const handleSearch = () => {
    pagination.page = 1;
    loadData();
};

// 重置筛选
const handleReset = () => {
    Object.assign(filterForm, {
        name: '',
        sex: '',
        professional_title: '',
        employer: '',
        specialty: '',
        instruments: '',
        task_name: '',
        birthdate_range: []
    });
    handleSearch();
};

// 选择变化
const handleSelectionChange = (selection: any[]) => {
    selectedRows.value = selection;
};

// 分页变化
const handleSizeChange = (size: number) => {
    pagination.pageSize = size;
    pagination.page = 1;
    loadData();
};

const handleCurrentChange = (page: number) => {
    pagination.page = page;
    loadData();
};

// 导出Excel（导出当前筛选条件下的全部数据，不受分页限制）
const handleExport = async () => {
    try {
        const params = {
            page: 1,
            page_size: 100000,
            name: filterForm.name,
            sex: filterForm.sex,
            professional_title: filterForm.professional_title,
            employer: filterForm.employer,
            specialty: filterForm.specialty,
            instruments: filterForm.instruments,
            task_name: filterForm.task_name,
            birthdate_start: filterForm.birthdate_range?.[0] || '',
            birthdate_end: filterForm.birthdate_range?.[1] || ''
        };

        const res = await fetchInvestigationPersonnelList(params);
        if (res.code !== 200) {
            ElMessage.error(res.message || '导出失败');
            return;
        }

        const rows = (res.data.list || []).map((row: any) => ({
            '航次名称': row.task_name ?? '',
            '姓名': row.name ?? '',
            '性别': row.sex ?? '',
            '出生年月': row.birthdate ?? '',
            '职称': row.professional_title ?? '',
            '工作单位': row.employer ?? '',
            '从事专业': row.specialty ?? '',
            '操作仪器': row.instruments ?? '',
            '培训情况': row.training ?? '',
            '备注': row.remarks ?? '',
            '数据来源': row.source_type ?? ''
        }));

        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(rows);
        XLSX.utils.book_append_sheet(wb, ws, '调查人员');

        const ts = new Date();
        const pad = (n: number) => String(n).padStart(2, '0');
        const fileName = `调查人员_${ts.getFullYear()}-${pad(ts.getMonth()+1)}-${pad(ts.getDate())}_${pad(ts.getHours())}${pad(ts.getMinutes())}${pad(ts.getSeconds())}.xlsx`;
        XLSX.writeFile(wb, fileName);
        ElMessage.success('导出成功');
    } catch (error: any) {
        console.error('导出失败:', error);
        ElMessage.error('导出失败: ' + (error.message || '未知错误'));
    }
};

onMounted(() => {
    loadData();
});

// 当组件被激活时（比如从其他页面切换回来）自动刷新数据
onActivated(() => {
    loadData();
});
</script>

<style scoped>
.investigation-personnel {
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
}

.filter-section {
    margin-bottom: 20px;
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 8px;
}

.filter-form {
    margin: 0;
}

.toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 8px;
}

.toolbar-left {
    display: flex;
    gap: 10px;
}

.toolbar-right {
    display: flex;
    gap: 10px;
}

.info-text {
    color: #666;
    font-size: 14px;
}

.investigation-personnel-table {
    width: 100%;
    margin-bottom: 20px;
}

.pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

:deep(.el-table) {
    font-size: 14px;
}

:deep(.el-table th) {
    background-color: #f5f7fa;
    color: #606266;
    font-weight: 600;
}

:deep(.el-table td) {
    padding: 8px 0;
}

:deep(.el-button) {
    border-radius: 4px;
}
</style>