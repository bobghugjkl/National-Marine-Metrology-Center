<template>
    <div class="personnel-qualifications">
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
            class="personnel-table"
            @selection-change="handleSelectionChange"
            @row-click="handleRowClick"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
            <el-table-column prop="task_name" label="航次任务名称" min-width="180">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.task_name" size="small" @click.stop></el-input>
                    </template>
                    <span v-else class="task-name">{{ row.task_name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="name" label="姓名" width="100" align="center">
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
                            type="month"
                            placeholder="选择月份"
                            size="small"
                            value-format="YYYY-MM"
                            @click.stop
                        ></el-date-picker>
                    </template>
                    <span v-else>{{ row.birth_date }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="title" label="职称" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.title" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.title }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="work_unit" label="工作单位" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.work_unit" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.work_unit }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="major" label="从事专业" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.major" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.major }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="instruments" label="本航次操作仪器" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.instruments" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.instruments }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="training" label="培训情况" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.training" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.training }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="remark" label="备注" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.remark" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.remark }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="attachment" label="附件" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-upload
                            ref="attachmentUploadRef"
                            class="attachment-upload"
                            action=""
                            :http-request="(params) => handleAttachmentUpload(params, row)"
                            :file-list="row.attachmentList || []"
                            multiple
                            :limit="3"
                            size="small"
                        >
                            <el-button size="small" type="primary">上传</el-button>
                        </el-upload>
                    </template>
                    <el-button v-else type="text" size="small" @click.stop="handleViewAttachment(row)">查看</el-button>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center" fixed="right">
                <template #default="{ row }">
                    <div class="operation-buttons">
                        <el-button
                            v-if="!row.isEditing"
                            type="primary"
                            size="small"
                            :icon="Edit"
                            @click.stop="handleEdit(row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            v-else
                            type="success"
                            size="small"
                            :icon="Check"
                            @click.stop="handleSave(row)"
                        >
                            保存
                        </el-button>

                        <el-button
                            v-if="!row.isEditing"
                            type="danger"
                            size="small"
                            :icon="Delete"
                            @click.stop="handleDelete(row)"
                        >
                            删除
                        </el-button>
                        <el-button
                            v-else
                            type="warning"
                            size="small"
                            :icon="Close"
                            @click.stop="handleCancel(row)"
                        >
                            取消
                        </el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>

        <!-- 新建/编辑弹窗 -->
        <el-dialog
            :title="isEdit ? '编辑人员信息' : '新建人员信息'"
            v-model="dialogVisible"
            width="800px"
            :close-on-click-modal="false"
            @close="handleDialogClose"
        >
            <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="航次任务名称" prop="task_name">
                            <el-input v-model="formData.task_name" :disabled="true" placeholder="自动填充"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="姓名" prop="name">
                            <el-input v-model="formData.name" placeholder="请输入姓名"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="性别" prop="gender">
                            <el-select v-model="formData.gender" placeholder="请选择性别" style="width: 100%">
                                <el-option label="男" value="男"></el-option>
                                <el-option label="女" value="女"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="出生年月" prop="birth_date">
                            <el-date-picker
                                v-model="formData.birth_date"
                                type="month"
                                placeholder="选择出生年月"
                                value-format="YYYY-MM"
                                style="width: 100%">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="职称" prop="title">
                            <el-input v-model="formData.title" placeholder="请输入职称"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="工作单位" prop="work_unit">
                            <el-input v-model="formData.work_unit" placeholder="请输入工作单位"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="从事专业" prop="major">
                            <el-input v-model="formData.major" placeholder="请输入从事专业"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="本航次操作仪器" prop="instruments">
                            <el-input v-model="formData.instruments" placeholder="请输入操作仪器"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="培训情况" prop="training">
                            <el-input v-model="formData.training" placeholder="请输入培训情况"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="备注" prop="remark">
                            <el-input v-model="formData.remark" placeholder="请输入备注"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="附件上传">
                            <el-upload
                                ref="attachmentUploadRef"
                                class="upload-demo"
                                action=""
                                :http-request="handleAttachmentUpload"
                                :file-list="attachmentList"
                                multiple
                                :limit="5"
                            >
                                <el-button size="small" type="primary">选择文件</el-button>
                                <template #tip>
                                    <div class="el-upload__tip">支持jpg/png/pdf等格式，单个文件不超过10MB</div>
                                </template>
                            </el-upload>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleDialogClose">取消</el-button>
                    <el-button type="primary" @click="handleDialogSubmit">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, defineProps } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Delete, Upload, Download, Edit, Document, Check, Close } from '@element-plus/icons-vue';
import * as XLSX from 'xlsx';

const props = defineProps({
    taskName: {
        type: String,
        required: true
    }
});

interface Personnel {
    id?: number;
    task_name: string;
    name: string;
    gender: string;
    birth_date: string;
    title: string;
    work_unit: string;
    major: string;
    instruments: string;
    training: string;
    remark: string;
    attachment?: string;
    attachmentList?: any[];
    isEditing?: boolean;
}

// 响应式数据
const tableData = ref<Personnel[]>([]);
const selectedRows = ref<Personnel[]>([]);
const dialogVisible = ref(false);
const isEdit = ref(false);
const editingIndex = ref(-1);

// 表单引用
const formRef = ref();
const uploadRef = ref();
const attachmentUploadRef = ref();

// 表单数据
const formData = reactive<Personnel>({
    task_name: props.taskName,
    name: '',
    gender: '',
    birth_date: '',
    title: '',
    work_unit: '',
    major: '',
    instruments: '',
    training: '',
    remark: '',
    attachment: ''
});

// 附件列表
const attachmentList = ref<any[]>([]);

// 表单验证规则
const rules = {
    task_name: [{ required: true, message: '请输入航次任务名称', trigger: 'blur' }],
    name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
    gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
    birth_date: [{ required: true, message: '请选择出生年月', trigger: 'change' }],
    title: [{ required: true, message: '请输入职称', trigger: 'blur' }],
    work_unit: [{ required: true, message: '请输入工作单位', trigger: 'blur' }],
    major: [{ required: true, message: '请输入从事专业', trigger: 'blur' }],
    instruments: [{ required: true, message: '请输入操作仪器', trigger: 'blur' }],
    training: [{ required: true, message: '请输入培训情况', trigger: 'blur' }]
};

// 表格引用
const tableRef = ref();

// 新建（通过表格内联编辑）
const handleAddRow = () => {
    const newRow: Personnel = {
        id: Date.now(),
        task_name: props.taskName,
        name: '',
        gender: '',
        birth_date: '',
        title: '',
        work_unit: '',
        major: '',
        instruments: '',
        training: '',
        remark: '',
        attachment: '',
        attachmentList: [],
        isEditing: true
    };
    tableData.value.push(newRow);
};

// 编辑
const handleEdit = (row: Personnel) => {
    // 取消其他行的编辑状态
    tableData.value.forEach(item => {
        if (item !== row) {
            item.isEditing = false;
        }
    });
    row.isEditing = true;
};

// 保存编辑
const handleSave = async (row: Personnel) => {
    try {
        // TODO: 调用后端API保存数据
        row.isEditing = false;
        ElMessage.success('保存成功');
    } catch (error) {
        ElMessage.error('保存失败');
    }
};

// 取消编辑
const handleCancel = (row: Personnel) => {
    // 恢复原始数据或重新加载数据
    row.isEditing = false;
    ElMessage.info('已取消编辑');
};

// 删除单个人员
const handleDelete = (row: Personnel) => {
    ElMessageBox.confirm(`确定要删除人员 "${row.name}" 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        const index = tableData.value.indexOf(row);
        if (index > -1) {
            tableData.value.splice(index, 1);
            ElMessage.success('删除成功');
        }
    }).catch(() => {
        // 用户取消删除
    });
};

// 删除选中项
const handleDeleteBatch = () => {
    if (selectedRows.value.length === 0) {
        ElMessage.warning('请选择要删除的人员');
        return;
    }

    ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 条记录吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        selectedRows.value.forEach(row => {
            const index = tableData.value.indexOf(row);
            if (index > -1) {
                tableData.value.splice(index, 1);
            }
        });
        selectedRows.value = [];
        ElMessage.success('删除成功');
    });
};

// 保存整个表格
const handleSaveAll = async () => {
    try {
        // TODO: 调用后端API保存数据
        ElMessage.success('保存成功');
    } catch (error) {
        ElMessage.error('保存失败');
    }
};

// 导入Excel
const handleImport = (params: any) => {
    const file = params.file;
    const reader = new FileReader();

    reader.onload = (e) => {
        try {
            const data = new Uint8Array(e.target?.result as ArrayBuffer);
            const workbook = XLSX.read(data, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const jsonData = XLSX.utils.sheet_to_json(worksheet);

            // 处理导入的数据
            jsonData.forEach((item: any, index: number) => {
                const personnel: Personnel = {
                    task_name: props.taskName,
                    name: item['姓名'] || '',
                    gender: item['性别'] || '',
                    birth_date: item['出生年月'] || '',
                    title: item['职称'] || '',
                    work_unit: item['工作单位'] || '',
                    major: item['从事专业'] || '',
                    instruments: item['本航次操作仪器'] || '',
                    training: item['培训情况'] || '',
                    remark: item['备注'] || '',
                    attachment: item['附件'] || ''
                };

                tableData.value.push(personnel);
            });

            ElMessage.success(`成功导入 ${jsonData.length} 条数据`);
        } catch (error) {
            ElMessage.error('导入失败，请检查文件格式');
        }
    };

    reader.readAsArrayBuffer(file);
};

// 导出Excel
const handleExport = () => {
    try {
        const exportData = tableData.value.map(item => ({
            '航次任务名称': item.task_name,
            '姓名': item.name,
            '性别': item.gender,
            '出生年月': item.birth_date,
            '职称': item.title,
            '工作单位': item.work_unit,
            '从事专业': item.major,
            '本航次操作仪器': item.instruments,
            '培训情况': item.training,
            '备注': item.remark,
            '附件': item.attachment
        }));

        const worksheet = XLSX.utils.json_to_sheet(exportData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, '外业调查人员资质表');
        XLSX.writeFile(workbook, `外业调查人员资质表_${props.taskName}.xlsx`);

        ElMessage.success('导出成功');
    } catch (error) {
        ElMessage.error('导出失败');
    }
};

// 查看附件
const handleViewAttachment = (row: Personnel) => {
    const attachments = row.attachmentList || [];
    if (attachments.length === 0) {
        ElMessage.info('暂无附件');
        return;
    }

    // 显示附件列表（暂时用消息提示，实际可以做成弹窗）
    const fileNames = attachments.map(file => file.name).join('\n');
    ElMessage.info(`附件列表：\n${fileNames}`);
};

// 附件上传
const handleAttachmentUpload = (params: any, row: Personnel) => {
    // TODO: 实现附件上传功能
    const file = params.file;
    if (!row.attachmentList) {
        row.attachmentList = [];
    }

    // 模拟上传成功
    const fileInfo = {
        uid: Date.now(),
        name: file.name,
        url: '#', // 实际应该是上传后的URL
        status: 'success'
    };

    row.attachmentList.push(fileInfo);
    ElMessage.success('附件上传成功');
};

// 选择变化
const handleSelectionChange = (selection: Personnel[]) => {
    selectedRows.value = selection;
};

// 行点击
const handleRowClick = (row: Personnel) => {
    tableRef.value?.toggleRowSelection(row);
};

// 弹窗提交
const handleDialogSubmit = () => {
    formRef.value?.validate((valid: boolean) => {
        if (valid) {
            if (isEdit.value && editingIndex.value >= 0) {
                // 编辑模式
                tableData.value[editingIndex.value] = { ...formData };
                ElMessage.success('编辑成功');
            } else {
                // 新建模式
                tableData.value.push({ ...formData });
                ElMessage.success('新建成功');
            }
            dialogVisible.value = false;
        }
    });
};

// 弹窗关闭
const handleDialogClose = () => {
    dialogVisible.value = false;
    formRef.value?.resetFields();
};

// 模拟加载数据
const loadData = async () => {
    try {
        // TODO: 调用后端API获取数据
        // 这里暂时用模拟数据
        tableData.value = [
            {
                id: 1,
                task_name: props.taskName,
                name: '张三',
                gender: '男',
                birth_date: '1985-06',
                title: '工程师',
                work_unit: '海洋研究所',
                major: '海洋地质',
                instruments: 'CTD、多参数水质仪',
                training: '海洋调查技能培训',
                remark: '经验丰富',
                attachment: '',
                attachmentList: [],
                isEditing: false
            }
        ];
    } catch (error) {
        ElMessage.error('加载数据失败');
    }
};

onMounted(() => {
    loadData();
});
</script>

<style scoped>
.personnel-qualifications {
    padding: 20px;
         /* 确保容器不超出 */
 
  /* 防止内容横向溢出 */
  overflow-x: hidden;

}

.toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 16px;
    background-color: #f8f9fa;
    border-radius: 6px;
}

.toolbar-left, .toolbar-right {
    display: flex;
    gap: 12px;
    align-items: center;
}

.personnel-table {
    width: 70%;
}

.task-name {
    color: #409eff;
    font-weight: 500;
}

:deep(.el-table th) {
    background-color: #f5f7fa;
    color: #606266;
    font-weight: 600;
}

:deep(.el-table td) {
    padding: 8px 0;
}

:deep(.el-form-item__label) {
    font-weight: 500;
}

:deep(.el-upload__tip) {
    font-size: 12px;
    color: #909399;
    margin-top: 8px;
}

.dialog-footer {
    text-align: right;
}

:deep(.el-dialog__body) {
    max-height: 70vh;
    overflow-y: auto;
}

/* 操作按钮美化 */
.operation-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;
}

.operation-buttons .el-button {
    margin: 0 2px;
    min-width: auto;
    padding: 6px 10px;
    height: 28px;
    border-radius: 4px;
}

.operation-buttons .el-button:hover {
    transform: scale(1.05);
    transition: transform 0.2s ease;
}

/* 附件上传样式 */
.attachment-upload {
    width: 100%;
}

.attachment-upload .el-button {
    width: 100%;
    margin: 0;
}
</style>
