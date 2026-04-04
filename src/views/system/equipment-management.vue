<template>
    <div class="equipment-management">
        <!-- 筛选区域 -->
        <div class="filter-section">
            <el-form :model="filterForm" inline class="filter-form">
                <el-form-item label="航次任务名称:">
                    <el-input v-model="filterForm.task_name" placeholder="请输入航次任务名称" clearable style="width: 200px"></el-input>
                </el-form-item>
                <el-form-item label="仪器类型:">
                    <el-select v-model="filterForm.instrument_type" placeholder="请选择仪器类型" clearable style="width: 150px">
                        <el-option label="仪器" value="仪器"></el-option>
                        <el-option label="标准物质" value="标准物质"></el-option>
                        <el-option label="计量器具" value="计量器具"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="仪器名称:">
                    <el-input v-model="filterForm.instrument_name" placeholder="请输入仪器名称" clearable style="width: 200px"></el-input>
                </el-form-item>
                <el-form-item label="量值溯源:">
                    <el-select v-model="filterForm.traceability" placeholder="请选择量值溯源" clearable style="width: 150px">
                        <el-option label="检定" value="检定"></el-option>
                        <el-option label="校准" value="校准"></el-option>
                        <el-option label="比对" value="比对"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="检定/校准机构:">
                    <el-input v-model="filterForm.calibration_institution" placeholder="请输入检定/校准机构" clearable style="width: 200px"></el-input>
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
                <span class="info-text">数据来源：仪器设备(工作计量器具)一览表 + 仪器设备(工作计量器具)一览表(航中)</span>
            </div>
        </div>

        <!-- 表格 -->
        <el-table
            ref="tableRef"
            :data="tableData"
            border
            stripe
            class="equipment-management-table"
            @selection-change="handleSelectionChange"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
            <el-table-column prop="task_name" label="航次名称" min-width="200">
                <template #default="{ row }">
                    <span>{{ row.task_name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="category" label="类别" width="120" align="center">
                <template #default="{ row }">
                    <span>{{ row.category }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="instrument_name" label="仪器(标准物质)名称" min-width="200">
                <template #default="{ row }">
                    <span>{{ row.instrument_name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="instrument_number" label="编号" width="120" align="center">
                <template #default="{ row }">
                    <span>{{ row.instrument_number }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="model" label="型号" width="120" align="center">
                <template #default="{ row }">
                    <span>{{ row.model }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="traceability_method" label="量值溯源方式" min-width="150">
                <template #default="{ row }">
                    <span>{{ row.traceability_method }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="calibration_date" label="检定/校准日期" width="150" align="center">
                <template #default="{ row }">
                    <span>{{ row.calibration_date }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="certificate_number" label="证书编号" width="150" align="center">
                <template #default="{ row }">
                    <span>{{ row.certificate_number }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="validity_period" label="有效期" width="120" align="center">
                <template #default="{ row }">
                    <span>{{ row.validity_period }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="calibration_institution" label="检定/校准机构" min-width="200">
                <template #default="{ row }">
                    <span>{{ row.calibration_institution }}</span>
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
import { fetchEquipmentManagementList, exportEquipmentManagement } from '@/api/equipment-management';
import * as XLSX from 'xlsx';

// 筛选表单
const filterForm = reactive({
    task_name: '',
    instrument_type: '',
    instrument_name: '',
    traceability: '',
    calibration_institution: ''
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
            task_name: filterForm.task_name,
            instrument_type: filterForm.instrument_type,
            instrument_name: filterForm.instrument_name,
            traceability: filterForm.traceability,
            calibration_institution: filterForm.calibration_institution
        };
        
        const res = await fetchEquipmentManagementList(params);
        if (res.code === 200) {
            tableData.value = res.data.list;
            pagination.total = res.data.total;
        } else {
            ElMessage.error(res.message || '获取数据失败');
        }
    } catch (error: any) {
        console.error('获取仪器设备管理列表失败:', error);
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
        task_name: '',
        instrument_type: '',
        instrument_name: '',
        traceability: '',
        calibration_institution: ''
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
            task_name: filterForm.task_name,
            instrument_type: filterForm.instrument_type,
            instrument_name: filterForm.instrument_name,
            traceability: filterForm.traceability,
            calibration_institution: filterForm.calibration_institution
        };

        const res = await fetchEquipmentManagementList(params);
        if (res.code !== 200) {
            ElMessage.error(res.message || '导出失败');
            return;
        }

        const rows = (res.data.list || []).map((row: any) => ({
            '航次名称': row.task_name ?? '',
            '类别': row.category ?? '',
            '仪器(标准物质)名称': row.instrument_name ?? '',
            '编号': row.instrument_number ?? '',
            '型号': row.model ?? '',
            '量值溯源方式': row.traceability_method ?? '',
            '检定/校准日期': row.calibration_date ?? '',
            '证书编号': row.certificate_number ?? '',
            '有效期': row.validity_period ?? '',
            '检定/校准机构': row.calibration_institution ?? '',
            '备注': row.remarks ?? '',
            '数据来源': row.source_type ?? ''
        }));

        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(rows);
        XLSX.utils.book_append_sheet(wb, ws, '仪器设备管理');

        const ts = new Date();
        const pad = (n: number) => String(n).padStart(2, '0');
        const fileName = `仪器设备管理_${ts.getFullYear()}-${pad(ts.getMonth()+1)}-${pad(ts.getDate())}_${pad(ts.getHours())}${pad(ts.getMinutes())}${pad(ts.getSeconds())}.xlsx`;
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
.equipment-management {
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

.equipment-management-table {
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
