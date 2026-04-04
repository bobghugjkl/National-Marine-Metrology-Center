<template>
    <div class="task-unit">
        <!-- 筛选区域 -->
        <div class="filter-section">
            <el-form :model="filterForm" inline class="filter-form">
                <el-form-item label="单位名称:">
                    <el-input v-model="filterForm.unit_name" placeholder="请输入单位名称" clearable style="width: 200px"></el-input>
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
                <el-button type="primary" :icon="Plus" @click="handleAddRow">新建</el-button>
                <el-button type="danger" :icon="Delete" @click="handleDeleteBatch" :disabled="selectedRows.length === 0">删除</el-button>
            </div>
            <div class="toolbar-right">
                <el-upload
                    ref="uploadRef"
                    class="upload-demo"
                    action=""
                    :http-request="handleImport"
                    :show-file-list="false"
                    accept=".xlsx,.xls"
                >
                    <el-button type="success" :icon="Upload">导入Excel文件</el-button>
                </el-upload>
                <el-button type="warning" :icon="Download" @click="handleExport">导出Excel</el-button>
                <el-button type="primary" :icon="Document" @click="handleSaveAll">保存</el-button>
            </div>
        </div>

        <!-- 表格 -->
        <el-table
            ref="tableRef"
            :data="tableData"
            border
            stripe
            class="task-unit-table"
            @selection-change="handleSelectionChange"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
            <el-table-column prop="unit_name" label="单位名称" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.unit_name" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.unit_name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="specialized_person" label="专项负责人" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.specialized_person" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.specialized_person }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="quality_manager" label="质量管理负责人" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.quality_manager" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.quality_manager }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="contact_person" label="联系人" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.contact_person" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.contact_person }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="contact_info" label="联系方式" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.contact_info" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.contact_info }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="remarks" label="备注" min-width="150">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.remarks" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.remarks }}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="160" fixed="right" align="center">
                <template #default="{ row }">
                    <div v-if="!row.isEditing" class="action-buttons">
                        <el-button
                            type="primary"
                            size="default"
                            @click="handleEdit(row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            type="danger"
                            size="default"
                            @click="handleDelete(row)"
                        >
                            删除
                        </el-button>
                    </div>
                    <div v-if="row.isEditing" class="action-buttons">
                        <el-button
                            type="success"
                            size="default"
                            @click="handleSave(row)"
                        >
                            保存
                        </el-button>
                        <el-button
                            size="default"
                            @click="handleCancel(row)"
                        >
                            取消
                        </el-button>
                    </div>
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
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Delete, Upload, Download, Document } from '@element-plus/icons-vue';
import { fetchTaskUnitList, createTaskUnit, updateTaskUnit, deleteTaskUnit, batchDeleteTaskUnit } from '@/api/task-unit';
import * as XLSX from 'xlsx';

// 筛选表单
const filterForm = reactive({
    unit_name: ''
});

// 表格数据
const tableData = ref([]);
const selectedRows = ref([]);
const tableRef = ref();
const uploadRef = ref();

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
            ...filterForm
        };
        
        const res = await fetchTaskUnitList(params);
        if (res.code === 200) {
            tableData.value = res.data.list.map((item: any) => ({
                ...item,
                isEditing: false,
                isNew: false
            }));
            pagination.total = res.data.total;
        } else {
            ElMessage.error(res.message || '获取数据失败');
        }
    } catch (error: any) {
        console.error('获取任务单位列表失败:', error);
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
        unit_name: ''
    });
    handleSearch();
};

// 新增行
const handleAddRow = () => {
    const newRow = {
        id: null,
        unit_name: '',
        specialized_person: '',
        quality_manager: '',
        contact_person: '',
        contact_info: '',
        remarks: '',
        isEditing: true,
        isNew: true
    };
    tableData.value.unshift(newRow);
};

// 编辑行
const handleEdit = (row: any) => {
    row.isEditing = true;
    row.originalData = { ...row };
};

// 保存行
const handleSave = async (row: any) => {
    try {
        if (row.isNew) {
            const res = await createTaskUnit(row);
            if (res.code === 200) {
                ElMessage.success('创建成功');
                row.isNew = false;
                row.isEditing = false;
                row.id = res.data.id;
            } else {
                ElMessage.error(res.message || '创建失败');
            }
        } else {
            const res = await updateTaskUnit(row.id, row);
            if (res.code === 200) {
                ElMessage.success('更新成功');
                row.isEditing = false;
            } else {
                ElMessage.error(res.message || '更新失败');
            }
        }
    } catch (error: any) {
        console.error('保存失败:', error);
        ElMessage.error('保存失败: ' + (error.message || '未知错误'));
    }
};

// 取消编辑
const handleCancel = (row: any) => {
    if (row.isNew) {
        const index = tableData.value.indexOf(row);
        tableData.value.splice(index, 1);
    } else {
        Object.assign(row, row.originalData);
        row.isEditing = false;
    }
};

// 删除行
const handleDelete = async (row: any) => {
    try {
        await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        });
        
        const res = await deleteTaskUnit(row.id);
        if (res.code === 200) {
            ElMessage.success('删除成功');
            loadData();
        } else {
            ElMessage.error(res.message || '删除失败');
        }
    } catch (error: any) {
        if (error !== 'cancel') {
            console.error('删除失败:', error);
            ElMessage.error('删除失败: ' + (error.message || '未知错误'));
        }
    }
};

// 批量删除
const handleDeleteBatch = async () => {
    if (selectedRows.value.length === 0) {
        ElMessage.warning('请选择要删除的记录');
        return;
    }
    
    try {
        await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 条记录吗？`, '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        });
        
        const ids = selectedRows.value.map(row => row.id);
        const res = await batchDeleteTaskUnit(ids);
        if (res.code === 200) {
            ElMessage.success(res.message || '批量删除成功');
            loadData();
        } else {
            ElMessage.error(res.message || '批量删除失败');
        }
    } catch (error: any) {
        if (error !== 'cancel') {
            console.error('批量删除失败:', error);
            ElMessage.error('批量删除失败: ' + (error.message || '未知错误'));
        }
    }
};

// 选择变化
const handleSelectionChange = (selection: any[]) => {
    selectedRows.value = selection;
};

// 移除行点击自动编辑功能

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

// 导入Excel
const handleImport = (file: any) => {
    ElMessage.info('导入功能待实现');
};

// 导出Excel（导出当前筛选条件下的全部数据，不受分页限制）
const handleExport = async () => {
    try {
        const params = {
            page: 1,
            page_size: 100000,
            unit_name: filterForm.unit_name
        };

        const res = await fetchTaskUnitList(params);
        if (res.code !== 200) {
            ElMessage.error(res.message || '导出失败');
            return;
        }

        const rows = (res.data.list || []).map((row: any) => ({
            '单位名称': row.unit_name ?? '',
            '专项负责人': row.specialized_person ?? '',
            '质量管理负责人': row.quality_manager ?? '',
            '联系人': row.contact_person ?? '',
            '联系方式': row.contact_info ?? '',
            '备注': row.remarks ?? ''
        }));

        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(rows);
        XLSX.utils.book_append_sheet(wb, ws, '任务单位');

        const ts = new Date();
        const pad = (n: number) => String(n).padStart(2, '0');
        const fileName = `任务单位_${ts.getFullYear()}-${pad(ts.getMonth()+1)}-${pad(ts.getDate())}_${pad(ts.getHours())}${pad(ts.getMinutes())}${pad(ts.getSeconds())}.xlsx`;
        XLSX.writeFile(wb, fileName);
        ElMessage.success('导出成功');
    } catch (error: any) {
        console.error('导出失败:', error);
        ElMessage.error('导出失败: ' + (error.message || '未知错误'));
    }
};

// 保存所有
const handleSaveAll = () => {
    ElMessage.info('保存所有功能待实现');
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
.task-unit {
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

.task-unit-table {
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

:deep(.el-input__wrapper) {
    border-radius: 4px;
}

:deep(.el-button) {
    border-radius: 4px;
}

.action-buttons {
    display: flex;
    flex-direction: row;
    gap: 8px;
    align-items: center;
    justify-content: center;
}

.action-buttons .el-button {
    min-width: 60px;
    height: 32px;
    font-size: 14px;
    padding: 8px 16px;
}

.action-buttons .el-button + .el-button {
    margin-left: 0;
}
</style>