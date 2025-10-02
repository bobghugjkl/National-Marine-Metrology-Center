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
            <el-table-column prop="attachment" label="附件" width="180" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-upload
                            ref="attachmentUploadRef"
                            class="attachment-upload"
                            action=""
                            :http-request="(params) => handleAttachmentUpload(params, row)"
                            :file-list="row.attachmentList || []"
                            :show-file-list="true"
                            list-type="text"
                            multiple
                            :limit="3"
                            size="small"
                        >
                            <el-button size="small" type="primary">选择文件</el-button>
                        </el-upload>
                    </template>
                    <el-button v-else type="text" size="small" @click.stop="handleViewAttachment(row)">
                        {{ (row.attachmentList && row.attachmentList.length > 0) ? `附件(${row.attachmentList.length})` : '无附件' }}
                    </el-button>
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
import { ref, reactive, onMounted, defineProps, watch } from 'vue';
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus';
import { Plus, Delete, Upload, Download, Edit, Document, Check, Close } from '@element-plus/icons-vue';
import * as XLSX from 'xlsx';
import { 
    getPersonnelQualifications, 
    createPersonnelQualification, 
    updatePersonnelQualification, 
    deletePersonnelQualification, 
    batchDeletePersonnelQualifications,
    uploadAttachment 
} from '../../api/personnel';

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
    // 打开新建对话框
    dialogVisible.value = true;
    isEdit.value = false;
    editingIndex.value = -1;
    
    // 重置表单数据，只保留任务名称
    Object.assign(formData, {
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
    
    // 清空附件列表
    attachmentList.value = [];
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
    const loading = ElLoading.service({
        lock: true,
        text: '保存中...',
        background: 'rgba(0, 0, 0, 0.7)'
    });
    
    try {
        // 调用后端API保存数据
        if (row.id) {
            // 更新现有记录
            const response = await updatePersonnelQualification(row.id, row);
            if (response.code === 200) {
                row.isEditing = false;
                ElMessage.success('保存成功');
                // 刷新数据
                await loadData();
            } else {
                ElMessage.error(response.msg || '保存失败');
            }
        } else {
            // 创建新记录
            const response = await createPersonnelQualification(row);
            if (response.code === 200) {
                row.isEditing = false;
                ElMessage.success('创建成功');
                // 刷新数据
                await loadData();
            } else {
                ElMessage.error(response.msg || '创建失败');
            }
        }
    } catch (error) {
        console.error('保存失败:', error);
        ElMessage.error('保存失败');
    } finally {
        loading.close();
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
    }).then(async () => {
        if (!row.id) {
            // 如果是新建的未保存记录，直接从本地数据中删除
            const index = tableData.value.indexOf(row);
            if (index > -1) {
                tableData.value.splice(index, 1);
                ElMessage.success('删除成功');
            }
            return;
        }
        
        // 调用后端API删除
        const loading = ElLoading.service({
            lock: true,
            text: '删除中...',
            background: 'rgba(0, 0, 0, 0.7)'
        });
        
        try {
            const response = await deletePersonnelQualification(row.id);
            if (response.code === 200) {
                ElMessage.success('删除成功');
                // 刷新数据
                await loadData();
            } else {
                ElMessage.error(response.msg || '删除失败');
            }
        } catch (error) {
            console.error('删除失败:', error);
            ElMessage.error('删除失败');
        } finally {
            loading.close();
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
    }).then(async () => {
        // 筛选出有ID的记录（已保存到数据库的）
        const savedRows = selectedRows.value.filter(row => row.id);
        const unsavedRows = selectedRows.value.filter(row => !row.id);
        
        // 处理未保存的记录（直接从本地数据中删除）
        unsavedRows.forEach(row => {
            const index = tableData.value.indexOf(row);
            if (index > -1) {
                tableData.value.splice(index, 1);
            }
        });
        
        if (savedRows.length > 0) {
            // 调用后端API批量删除
            const loading = ElLoading.service({
                lock: true,
                text: '删除中...',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            
            try {
                const ids = savedRows.map(row => row.id);
                const response = await batchDeletePersonnelQualifications(ids);
                if (response.code === 200) {
                    ElMessage.success('批量删除成功');
                    // 刷新数据
                    await loadData();
                } else {
                    ElMessage.error(response.msg || '批量删除失败');
                }
            } catch (error) {
                console.error('批量删除失败:', error);
                ElMessage.error('批量删除失败');
            } finally {
                loading.close();
            }
        } else if (unsavedRows.length > 0) {
            // 如果只有未保存的记录被删除
            ElMessage.success('删除成功');
        }
        
        selectedRows.value = [];
    }).catch(() => {
        // 用户取消删除
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

    // 创建自定义的附件列表内容
    const attachmentsContent = attachments.map((file, index) =>
        `<div style="margin: 8px 0; padding: 8px; background: #f5f7fa; border-radius: 4px; display: flex; justify-content: space-between; align-items: center;">
            <span>${index + 1}. ${file.name}</span>
            <a href="${file.url}" download="${file.name}" style="color: #409eff; text-decoration: none; padding: 4px 8px; background: #ecf5ff; border-radius: 4px;">下载</a>
        </div>`
    ).join('');

    ElMessageBox.alert(
        `<div style="max-height: 300px; overflow-y: auto;">${attachmentsContent}</div>`,
        '附件列表',
        {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '关闭',
            showCancelButton: false,
            customClass: 'attachment-dialog'
        }
    );
};


// 附件上传（兼容表格行与弹窗两种场景）
const handleAttachmentUpload = async (params: any, row?: Personnel) => {
    const file = params.file;

    // 目标文件列表：优先使用表格行的附件列表；若无row则使用弹窗的附件列表
    const targetList: any[] = row
        ? (row.attachmentList = row.attachmentList || [])
        : attachmentList.value;

    // 创建FormData对象
    const formData = new FormData();
    formData.append('file', file);

    try {
        // 先显示文件名，提升用户体验
        const tempFileInfo = {
            uid: Date.now(),
            name: file.name,
            status: 'uploading'
        };

        // 先添加到列表，显示上传中状态
        targetList.push(tempFileInfo);

        const loading = ElLoading.service({
            lock: true,
            text: '上传中...',
            background: 'rgba(0, 0, 0, 0.7)'
        });

        // 调用上传API
        const response = await uploadAttachment(formData);
        loading.close();

        if (response && response.code === 200) {
            // 上传成功，更新文件信息
            const index = targetList.findIndex((item: any) => item.uid === tempFileInfo.uid);
            if (index !== -1) {
                targetList[index] = {
                    uid: response.data.uid,
                    name: response.data.name,
                    url: response.data.url,
                    status: 'success'
                };
            }

            ElMessage.success('附件上传成功');

            // 自动处理上传回调
            if (params.onSuccess) {
                params.onSuccess(response, file);
            }
        } else {
            // 上传失败，从列表中移除
            const index = targetList.findIndex((item: any) => item.uid === tempFileInfo.uid);
            if (index !== -1) {
                targetList.splice(index, 1);
            }

            ElMessage.error(response?.msg || '上传失败');
            if (params.onError) {
                params.onError(new Error(response?.msg || '上传失败'));
            }
        }
    } catch (error) {
        console.error('上传失败:', error);
        ElMessage.error('上传失败，请检查网络连接或后端服务');

        if (params.onError) {
            params.onError(error);
        }
    }
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
    formRef.value?.validate(async (valid: boolean) => {
        if (valid) {
            const loading = ElLoading.service({
                lock: true,
                text: isEdit.value ? '更新中...' : '创建中...',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            
            try {
                // 准备提交的数据
                const submitData = { 
                    ...formData,
                    attachmentList: attachmentList.value
                };
                
                if (isEdit.value && editingIndex.value >= 0) {
                    // 编辑模式
                    const row = tableData.value[editingIndex.value];
                    if (row.id) {
                        // 更新现有记录
                        const response = await updatePersonnelQualification(row.id, submitData);
                        if (response.code === 200) {
                            ElMessage.success('编辑成功');
                            // 刷新数据
                            await loadData();
                        } else {
                            ElMessage.error(response.msg || '编辑失败');
                        }
                    }
                } else {
                    // 新建模式
                    const response = await createPersonnelQualification(submitData);
                    if (response.code === 200) {
                        ElMessage.success('创建成功');
                        // 刷新数据
                        await loadData();
                    } else {
                        ElMessage.error(response.msg || '创建失败');
                    }
                }
                
                // 关闭对话框
                dialogVisible.value = false;
            } catch (error) {
                console.error(isEdit.value ? '编辑失败:' : '创建失败:', error);
                ElMessage.error(isEdit.value ? '编辑失败' : '创建失败');
            } finally {
                loading.close();
            }
        }
    });
};

// 弹窗关闭
const handleDialogClose = () => {
    dialogVisible.value = false;
    formRef.value?.resetFields();
};

// 加载数据
const loadData = async () => {
    console.log('开始加载人员资质数据，任务名称:', props.taskName);

    const loading = ElLoading.service({
        lock: true,
        text: '加载中...',
        background: 'rgba(0, 0, 0, 0.7)'
    });

    try {
        // 检查认证状态
        let token = null;
        let userId = null;

        try {
            token = localStorage.getItem('token');
            userId = localStorage.getItem('userId');
        } catch (e) {
            console.warn('无法访问localStorage:', e);
        }

        console.log('当前认证状态:', {
            hasToken: !!token,
            hasUserId: !!userId,
            tokenPrefix: token ? token.substring(0, 20) + '...' : '无'
        });

        // 如果没有token，提示用户登录
        if (!token) {
            ElMessage.warning('请先登录系统');
            loading.close();
            return;
        }

        const response = await getPersonnelQualifications({ task_name: props.taskName });
        console.log('API响应:', response);

        if (response && response.code === 200) {
            console.log('数据加载成功，记录数量:', response.data?.length || 0);
            // 添加isEditing属性
            tableData.value = (response.data || []).map((item: any) => ({
                ...item,
                isEditing: false
            }));
        } else {
            console.error('API返回错误:', response);
            ElMessage.error(response?.msg || '加载数据失败');
        }
    } catch (error) {
        console.error('加载数据失败，错误详情:', error);
        if (error.response) {
            console.error('响应状态:', error.response.status);
            console.error('响应数据:', error.response.data);

            // 如果是401错误，提示重新登录
            if (error.response.status === 401) {
                ElMessage.error('登录已过期，请重新登录');
            } else {
                ElMessage.error(`加载数据失败: ${error.response.data?.msg || '网络错误'}`);
            }
        } else {
            ElMessage.error(`加载数据失败: ${error.message || '网络错误'}`);
        }
    } finally {
        loading.close();
    }
};

// 监听任务名称变化，自动重新加载数据
watch(() => props.taskName, (newVal, oldVal) => {
    if (newVal && newVal !== oldVal) {
        console.log(`任务名称从 ${oldVal} 变更为 ${newVal}，重新加载数据`);
        loadData();
    }
}, { immediate: true }); // immediate: true 确保组件挂载时也执行一次

onMounted(() => {
    // loadData() 已由 watch 的 immediate: true 处理
});
</script>

<style scoped>
.personnel-qualifications {
    padding: 20px;
    /* 确保容器不超出 */
    /* 当内容溢出时，显示水平滚动条 */
    overflow-x: auto;
    /* 设置最大宽度为100%，防止内容溢出父容器 */
    max-width: 100%;
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
    /* 设置最小宽度，确保表格有足够空间 */
    min-width: 1200px;
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

/* 附件对话框样式 */
.attachment-dialog .el-message-box__content {
    max-height: 400px;
    overflow-y: auto;
}

.attachment-dialog .el-message-box__content::-webkit-scrollbar {
    width: 6px;
}

.attachment-dialog .el-message-box__content::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.attachment-dialog .el-message-box__content::-webkit-scrollbar-thumb {
    background: #c0c4cc;
    border-radius: 3px;
}

.attachment-dialog .el-message-box__content::-webkit-scrollbar-thumb:hover {
    background: #909399;
}
</style>
