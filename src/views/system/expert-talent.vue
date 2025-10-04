<template>
    <div class="expert-talent">
        <!-- 筛选区域 -->
        <div class="filter-section">
            <el-form :model="filterForm" inline class="filter-form">
                <el-form-item label="姓名:">
                    <el-input v-model="filterForm.name" placeholder="请输入姓名" clearable style="width: 150px"></el-input>
                </el-form-item>
                <el-form-item label="性别:">
                    <el-select v-model="filterForm.gender" placeholder="请选择性别" clearable style="width: 120px">
                        <el-option label="男" value="男"></el-option>
                        <el-option label="女" value="女"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="职称:">
                    <el-select v-model="filterForm.job_title" placeholder="请选择职称" clearable style="width: 150px">
                        <el-option label="教授" value="教授"></el-option>
                        <el-option label="副教授" value="副教授"></el-option>
                        <el-option label="研究员" value="研究员"></el-option>
                        <el-option label="副研究员" value="副研究员"></el-option>
                        <el-option label="助理研究员" value="助理研究员"></el-option>
                        <el-option label="高级工程师" value="高级工程师"></el-option>
                        <el-option label="工程师" value="工程师"></el-option>
                        <el-option label="其他" value="其他"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="工作单位:">
                    <el-input v-model="filterForm.work_unit" placeholder="请输入工作单位" clearable style="width: 200px"></el-input>
                </el-form-item>
                <el-form-item label="从事专业:">
                    <el-select v-model="filterForm.specialty" placeholder="请选择专业" clearable style="width: 150px">
                        <el-option label="海洋科学" value="海洋科学"></el-option>
                        <el-option label="海洋工程" value="海洋工程"></el-option>
                        <el-option label="海洋技术" value="海洋技术"></el-option>
                        <el-option label="海洋生物" value="海洋生物"></el-option>
                        <el-option label="海洋化学" value="海洋化学"></el-option>
                        <el-option label="海洋物理" value="海洋物理"></el-option>
                        <el-option label="其他" value="其他"></el-option>
                    </el-select>
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
            class="expert-talent-table"
            @selection-change="handleSelectionChange"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
            <el-table-column prop="name" label="姓名" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.name" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="gender" label="性别" width="80" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-select v-model="row.gender" size="small" @click.stop>
                            <el-option label="男" value="男"></el-option>
                            <el-option label="女" value="女"></el-option>
                        </el-select>
                    </template>
                    <span v-else>{{ row.gender }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="birth_date" label="出生年月" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-date-picker
                            v-model="row.birth_date"
                            type="date"
                            placeholder="选择日期"
                            size="small"
                            value-format="YYYY-MM-DD"
                            @click.stop
                        ></el-date-picker>
                    </template>
                    <span v-else>{{ row.birth_date }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="job_title" label="职称" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-select v-model="row.job_title" size="small" @click.stop>
                            <el-option label="教授" value="教授"></el-option>
                            <el-option label="副教授" value="副教授"></el-option>
                            <el-option label="研究员" value="研究员"></el-option>
                            <el-option label="副研究员" value="副研究员"></el-option>
                            <el-option label="助理研究员" value="助理研究员"></el-option>
                            <el-option label="高级工程师" value="高级工程师"></el-option>
                            <el-option label="工程师" value="工程师"></el-option>
                            <el-option label="其他" value="其他"></el-option>
                        </el-select>
                    </template>
                    <span v-else>{{ row.job_title }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="work_unit" label="工作单位" min-width="150">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.work_unit" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.work_unit }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="specialty" label="从事专业" min-width="120">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-select v-model="row.specialty" size="small" @click.stop>
                            <el-option label="海洋科学" value="海洋科学"></el-option>
                            <el-option label="海洋工程" value="海洋工程"></el-option>
                            <el-option label="海洋技术" value="海洋技术"></el-option>
                            <el-option label="海洋生物" value="海洋生物"></el-option>
                            <el-option label="海洋化学" value="海洋化学"></el-option>
                            <el-option label="海洋物理" value="海洋物理"></el-option>
                            <el-option label="其他" value="其他"></el-option>
                        </el-select>
                    </template>
                    <span v-else>{{ row.specialty }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="contact_info" label="联系方式" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.contact_info" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.contact_info }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="id_number" label="身份证号" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.id_number" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.id_number }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="bank_card_number" label="银行卡号" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.bank_card_number" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.bank_card_number }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="opening_bank" label="开户行" min-width="150">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.opening_bank" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.opening_bank }}</span>
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
import { fetchExpertTalentList, createExpertTalent, updateExpertTalent, deleteExpertTalent, batchDeleteExpertTalent } from '@/api/expert-talent';
import * as XLSX from 'xlsx';

// 筛选表单
const filterForm = reactive({
    name: '',
    gender: '',
    job_title: '',
    work_unit: '',
    specialty: ''
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
        
        const res = await fetchExpertTalentList(params);
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
        console.error('获取专家人才列表失败:', error);
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
        gender: '',
        job_title: '',
        work_unit: '',
        specialty: ''
    });
    handleSearch();
};

// 新增行
const handleAddRow = () => {
    const newRow = {
        id: null,
        name: '',
        gender: '',
        birth_date: '',
        job_title: '',
        work_unit: '',
        specialty: '',
        contact_info: '',
        id_number: '',
        bank_card_number: '',
        opening_bank: '',
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
            const res = await createExpertTalent(row);
            if (res.code === 200) {
                ElMessage.success('创建成功');
                row.isNew = false;
                row.isEditing = false;
                row.id = res.data.id;
            } else {
                ElMessage.error(res.message || '创建失败');
            }
        } else {
            const res = await updateExpertTalent(row.id, row);
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
        
        const res = await deleteExpertTalent(row.id);
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
        const res = await batchDeleteExpertTalent(ids);
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
            ...filterForm
        };

        const res = await fetchExpertTalentList(params);
        if (res.code !== 200) {
            ElMessage.error(res.message || '导出失败');
            return;
        }

        const rows = (res.data.list || []).map((row: any) => ({
            '姓名': row.name ?? '',
            '性别': row.gender ?? '',
            '出生年月': row.birth_date ?? '',
            '职称': row.job_title ?? '',
            '工作单位': row.work_unit ?? '',
            '从事专业': row.specialty ?? '',
            '联系方式': row.contact_info ?? '',
            '身份证号': row.id_number ?? '',
            '银行卡号': row.bank_card_number ?? '',
            '开户行': row.opening_bank ?? '',
            '备注': row.remarks ?? ''
        }));

        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(rows);
        XLSX.utils.book_append_sheet(wb, ws, '专家人才');

        const ts = new Date();
        const pad = (n: number) => String(n).padStart(2, '0');
        const fileName = `专家人才_${ts.getFullYear()}-${pad(ts.getMonth()+1)}-${pad(ts.getDate())}_${pad(ts.getHours())}${pad(ts.getMinutes())}${pad(ts.getSeconds())}.xlsx`;
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
.expert-talent {
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

.expert-talent-table {
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
