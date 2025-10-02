<template>
    <div class="voyage-personnel">
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
            class="voyage-personnel-table"
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
            <el-table-column prop="sex" label="性别" width="80" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-select v-model="row.sex" size="small" @click.stop>
                            <el-option label="男" value="男"></el-option>
                            <el-option label="女" value="女"></el-option>
                        </el-select>
                    </template>
                    <span v-else>{{ row.sex }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="birthdate" label="出生年月" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-date-picker
                            v-model="row.birthdate"
                            type="date"
                            size="small"
                            format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD"
                            @click.stop
                        ></el-date-picker>
                    </template>
                    <span v-else>{{ row.birthdate }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="professional_title" label="职称" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.professional_title" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.professional_title }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="employer" label="工作单位" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.employer" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.employer }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="specialty" label="从事专业" min-width="150">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.specialty" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.specialty }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="instruments" label="本航次操作仪器" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.instruments" size="small" type="textarea" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.instruments }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="training" label="培训情况" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.training" size="small" type="textarea" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.training }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="remarks" label="备注" min-width="150">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.remarks" size="small" type="textarea" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.remarks }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="attachments" label="附件" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <div class="attachment-actions">
                            <el-upload
                                :http-request="(options) => handleAttachmentUpload(options, row)"
                                :show-file-list="false"
                                accept="*/*"
                            >
                                <el-button size="small" type="primary" :icon="Upload">上传</el-button>
                            </el-upload>
                            <el-button 
                                v-if="row.attachmentList && row.attachmentList.length > 0" 
                                size="small" 
                                type="info" 
                                :icon="Document" 
                                @click.stop="handleViewAttachment(row)"
                            >查看</el-button>
                        </div>
                    </template>
                    <template v-else>
                        <el-button type="text" size="small" @click.stop="handleViewAttachment(row)">
                            {{ (row.attachmentList && row.attachmentList.length > 0) ? `附件(${row.attachmentList.length})` : '无附件' }}
                        </el-button>
                    </template>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center" fixed="right">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-button size="small" type="success" :icon="Check" @click.stop="handleSaveRow(row)">保存</el-button>
                        <el-button size="small" type="warning" :icon="Close" @click.stop="handleCancelEdit(row)">取消</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="primary" :icon="Edit" @click.stop="handleEditRow(row)">编辑</el-button>
                        <el-button size="small" type="danger" :icon="Delete" @click.stop="handleDeleteRow(row)">删除</el-button>
                    </template>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
            <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
        </div>

        <!-- 新增/编辑对话框 -->
        <el-dialog
            v-model="dialogVisible"
            :title="isEdit ? '编辑航中外业调查人员' : '新增航中外业调查人员'"
            width="800px"
            @close="handleDialogClose"
        >
            <el-form :model="formData" label-width="120px">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="航次任务名称" required>
                            <el-input v-model="formData.task_name" placeholder="请输入航次任务名称"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="姓名" required>
                            <el-input v-model="formData.name" placeholder="请输入姓名"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-form-item label="性别" required>
                            <el-select v-model="formData.sex" placeholder="请选择性别">
                                <el-option label="男" value="男"></el-option>
                                <el-option label="女" value="女"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="出生年月" required>
                            <el-date-picker
                                v-model="formData.birthdate"
                                type="date"
                                format="YYYY-MM-DD"
                                value-format="YYYY-MM-DD"
                                placeholder="请选择出生年月"
                            ></el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="职称" required>
                            <el-input v-model="formData.professional_title" placeholder="请输入职称"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="工作单位" required>
                            <el-input v-model="formData.employer" placeholder="请输入工作单位"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="从事专业" required>
                            <el-input v-model="formData.specialty" placeholder="请输入从事专业"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="本航次操作仪器">
                    <el-input v-model="formData.instruments" type="textarea" placeholder="请输入本航次操作仪器"></el-input>
                </el-form-item>
                <el-form-item label="培训情况">
                    <el-input v-model="formData.training" type="textarea" placeholder="请输入培训情况"></el-input>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="formData.remarks" type="textarea" placeholder="请输入备注"></el-input>
                </el-form-item>
                <el-form-item label="附件">
                    <div class="attachment-section">
                        <el-upload
                            :http-request="handleDialogAttachmentUpload"
                            :show-file-list="false"
                            accept="*/*"
                        >
                            <el-button type="primary" :icon="Upload">上传附件</el-button>
                        </el-upload>
                        <div v-if="formData.attachmentList && formData.attachmentList.length > 0" class="attachment-list">
                            <div v-for="(attachment, index) in formData.attachmentList" :key="index" class="attachment-item">
                                <span>{{ attachment.filename }}</span>
                                <el-button size="small" type="danger" :icon="Delete" @click="removeAttachment(index)">删除</el-button>
                            </div>
                        </div>
                    </div>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSubmit">确定</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import {
    Plus,
    Delete,
    Edit,
    Check,
    Close,
    Upload,
    Download,
    Document
} from '@element-plus/icons-vue';
import {
    fetchVoyagePersonnelList,
    createVoyagePersonnel,
    updateVoyagePersonnel,
    deleteVoyagePersonnel,
    batchDeleteVoyagePersonnel,
    uploadVoyagePersonnelAttachment
} from '@/api/voyage-personnel';
import * as XLSX from 'xlsx';

// 接口定义
interface VoyagePersonnel {
    id?: number;
    task_name: string;
    name: string;
    sex: string;
    birthdate: string;
    professional_title: string;
    employer: string;
    specialty: string;
    instruments?: string;
    training?: string;
    remarks?: string;
    attachments?: any[];
    attachmentList?: any[];
    isEditing?: boolean;
    user_id?: number;
    create_time?: string;
    update_time?: string;
}

// Props
const props = defineProps<{
    taskName: string;
}>();

// 响应式数据
const tableData = ref<VoyagePersonnel[]>([]);
const selectedRows = ref<VoyagePersonnel[]>([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 对话框相关
const dialogVisible = ref(false);
const isEdit = ref(false);
const editingId = ref<number | null>(null);
const formData = ref<VoyagePersonnel>({
    task_name: '',
    name: '',
    sex: '',
    birthdate: '',
    professional_title: '',
    employer: '',
    specialty: '',
    instruments: '',
    training: '',
    remarks: '',
    attachmentList: []
});

// 表格引用
const tableRef = ref();
const uploadRef = ref();

// 方法定义
const loadData = async () => {
    try {
        console.log('开始加载航中外业调查人员数据，任务名称:', props.taskName);

        const response = await fetchVoyagePersonnelList({ task_name: props.taskName });
        console.log('API响应:', response);

        if (response && response.code === 200) {
            console.log('数据加载成功，记录数量:', response.data?.length || 0);
            // 添加isEditing属性
            tableData.value = (response.data || []).map((item: any) => ({
                ...item,
                isEditing: false,
                attachmentList: item.attachments || []
            }));
            total.value = response.total || 0;
        } else {
            console.error('数据加载失败:', response?.msg || '未知错误');
            ElMessage.error(response?.msg || '数据加载失败');
        }
    } catch (error) {
        console.error('加载航中外业调查人员数据错误:', error);
        ElMessage.error('数据加载失败');
    }
};

// 行选择变化
const handleSelectionChange = (selection: VoyagePersonnel[]) => {
    selectedRows.value = selection;
};

// 行点击
const handleRowClick = (row: VoyagePersonnel) => {
    if (!row.isEditing) {
        // 如果不在编辑状态，可以在这里添加行点击逻辑
    }
};

// 新增行
const handleAddRow = () => {
    const newRow: VoyagePersonnel = {
        task_name: props.taskName,
        name: '',
        sex: '',
        birthdate: '',
        professional_title: '',
        employer: '',
        specialty: '',
        instruments: '',
        training: '',
        remarks: '',
        attachmentList: [],
        isEditing: true
    };
    tableData.value.unshift(newRow);
};

// 编辑行
const handleEditRow = (row: VoyagePersonnel) => {
    row.isEditing = true;
    row.attachmentList = row.attachments || [];
};

// 保存行
const handleSaveRow = async (row: VoyagePersonnel) => {
    try {
        // 验证必填字段
        if (!row.name || !row.sex || !row.birthdate || !row.professional_title || !row.employer || !row.specialty) {
            ElMessage.error('请填写所有必填字段');
            return;
        }

        const updateData = {
            task_name: row.task_name,
            name: row.name,
            sex: row.sex,
            birthdate: row.birthdate,
            professional_title: row.professional_title,
            employer: row.employer,
            specialty: row.specialty,
            instruments: row.instruments || '',
            training: row.training || '',
            remarks: row.remarks || '',
            attachmentList: row.attachmentList || []
        };

        if (row.id) {
            // 更新现有记录
            const response = await updateVoyagePersonnel(row.id, updateData);
            if (response && response.code === 200) {
                ElMessage.success('保存成功');
                row.isEditing = false;
                // 重新加载数据
                loadData();
            } else {
                ElMessage.error(response?.msg || '保存失败');
            }
        } else {
            // 创建新记录
            const response = await createVoyagePersonnel(updateData);
            if (response && response.code === 200) {
                ElMessage.success('创建成功');
                row.isEditing = false;
                // 重新加载数据
                loadData();
            } else {
                ElMessage.error(response?.msg || '创建失败');
            }
        }
    } catch (error) {
        console.error('保存航中外业调查人员记录错误:', error);
        ElMessage.error('保存失败');
    }
};

// 取消编辑
const handleCancelEdit = (row: VoyagePersonnel) => {
    if (row.id) {
        // 如果是现有记录，重新加载数据
        loadData();
    } else {
        // 如果是新记录，从表格中移除
        const index = tableData.value.indexOf(row);
        if (index > -1) {
            tableData.value.splice(index, 1);
        }
    }
};

// 删除行
const handleDeleteRow = async (row: VoyagePersonnel) => {
    try {
        const confirmResult = await ElMessageBox.confirm(
            '确定要删除这条记录吗？',
            '删除确认',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }
        );

        if (confirmResult === 'confirm') {
            if (row.id) {
                const response = await deleteVoyagePersonnel(row.id);
                if (response && response.code === 200) {
                    ElMessage.success('删除成功');
                    loadData(); // 重新加载数据
                } else {
                    ElMessage.error(response?.msg || '删除失败');
                }
            } else {
                // 如果是新记录，直接从表格中移除
                const index = tableData.value.indexOf(row);
                if (index > -1) {
                    tableData.value.splice(index, 1);
                }
            }
        }
    } catch (error) {
        console.error('删除航中外业调查人员记录错误:', error);
        ElMessage.error('删除失败');
    }
};

// 批量删除
const handleDeleteBatch = async () => {
    try {
        if (selectedRows.value.length === 0) {
            ElMessage.warning('请选择要删除的记录');
            return;
        }

        const confirmResult = await ElMessageBox.confirm(
            `确定要删除选中的 ${selectedRows.value.length} 条记录吗？`,
            '批量删除确认',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }
        );

        if (confirmResult === 'confirm') {
            const ids = selectedRows.value.filter(row => row.id).map(row => row.id!);
            if (ids.length > 0) {
                const response = await batchDeleteVoyagePersonnel(ids);
                if (response && response.code === 200) {
                    ElMessage.success('批量删除成功');
                    loadData(); // 重新加载数据
                } else {
                    ElMessage.error(response?.msg || '批量删除失败');
                }
            }
        }
    } catch (error) {
        console.error('批量删除航中外业调查人员记录错误:', error);
        ElMessage.error('批量删除失败');
    }
};

// 附件上传
const handleAttachmentUpload = async (options: any, row: VoyagePersonnel) => {
    try {
        console.log('开始处理附件上传:', options, row);
        const file = options.file;
        console.log('选择的文件:', file);
        const response = await uploadVoyagePersonnelAttachment(file);
        
        if (response && response.code === 200) {
            if (!row.attachmentList) {
                row.attachmentList = [];
            }
            row.attachmentList.push({
                filename: response.data.filename,
                url: response.data.url,
                size: response.data.size
            });
            ElMessage.success('附件上传成功');
        } else {
            ElMessage.error(response?.msg || '附件上传失败');
        }
    } catch (error) {
        console.error('上传附件错误:', error);
        ElMessage.error('附件上传失败');
    }
};

// 查看附件
const handleViewAttachment = (row: VoyagePersonnel) => {
    const attachments = row.attachmentList || [];
    if (attachments.length === 0) {
        ElMessage.info('暂无附件');
        return;
    }

    // 创建自定义的附件列表内容
    const attachmentsContent = attachments.map((file, index) =>
        `<div style="margin: 8px 0; padding: 8px; background: #f5f7fa; border-radius: 4px; display: flex; justify-content: space-between; align-items: center;">
            <span>${index + 1}. ${file.filename || file.name}</span>
            <a href="${file.url}" download="${file.filename || file.name}" style="color: #409eff; text-decoration: none; padding: 4px 8px; background: #ecf5ff; border-radius: 4px;">下载</a>
        </div>`
    ).join('');

    ElMessageBox.alert(
        `<div style="max-height: 300px; overflow-y: auto;">${attachmentsContent}</div>`,
        '附件列表',
        {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '关闭',
            type: 'info'
        }
    );
};

// 保存所有
const handleSaveAll = async () => {
    try {
        const editingRows = tableData.value.filter(row => row.isEditing);
        if (editingRows.length === 0) {
            ElMessage.info('没有需要保存的记录');
            return;
        }

        for (const row of editingRows) {
            await handleSaveRow(row);
        }
    } catch (error) {
        console.error('保存所有记录错误:', error);
        ElMessage.error('保存失败');
    }
};

// 导入Excel
const handleImport = (options: any) => {
    ElMessage.info('Excel导入功能待实现');
};

// 导出Excel
const handleExport = () => {
    ElMessage.info('Excel导出功能待实现');
};

// 分页相关
const handleSizeChange = (val: number) => {
    pageSize.value = val;
    loadData();
};

const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    loadData();
};

// 对话框相关
const handleDialogClose = () => {
    formData.value = {
        task_name: props.taskName,
        name: '',
        sex: '',
        birthdate: '',
        professional_title: '',
        employer: '',
        specialty: '',
        instruments: '',
        training: '',
        remarks: '',
        attachmentList: []
    };
    isEdit.value = false;
    editingId.value = null;
};

const handleDialogAttachmentUpload = async (options: any) => {
    try {
        const file = options.file;
        const response = await uploadVoyagePersonnelAttachment(file);
        
        if (response && response.code === 200) {
            if (!formData.value.attachmentList) {
                formData.value.attachmentList = [];
            }
            formData.value.attachmentList.push({
                filename: response.data.filename,
                url: response.data.url,
                size: response.data.size
            });
            ElMessage.success('附件上传成功');
        } else {
            ElMessage.error(response?.msg || '附件上传失败');
        }
    } catch (error) {
        console.error('上传附件错误:', error);
        ElMessage.error('附件上传失败');
    }
};

const removeAttachment = (index: number) => {
    if (formData.value.attachmentList) {
        formData.value.attachmentList.splice(index, 1);
    }
};

const handleSubmit = async () => {
    try {
        // 验证必填字段
        if (!formData.value.name || !formData.value.sex || !formData.value.birthdate || 
            !formData.value.professional_title || !formData.value.employer || !formData.value.specialty) {
            ElMessage.error('请填写所有必填字段');
            return;
        }

        const submitData = {
            task_name: formData.value.task_name,
            name: formData.value.name,
            sex: formData.value.sex,
            birthdate: formData.value.birthdate,
            professional_title: formData.value.professional_title,
            employer: formData.value.employer,
            specialty: formData.value.specialty,
            instruments: formData.value.instruments || '',
            training: formData.value.training || '',
            remarks: formData.value.remarks || '',
            attachmentList: formData.value.attachmentList || []
        };

        if (isEdit.value && editingId.value) {
            // 编辑模式
            const response = await updateVoyagePersonnel(editingId.value, submitData);
            if (response && response.code === 200) {
                ElMessage.success('更新成功');
                dialogVisible.value = false;
                loadData();
            } else {
                ElMessage.error(response?.msg || '更新失败');
            }
        } else {
            // 新增模式
            const response = await createVoyagePersonnel(submitData);
            if (response && response.code === 200) {
                ElMessage.success('创建成功');
                dialogVisible.value = false;
                loadData();
            } else {
                ElMessage.error(response?.msg || '创建失败');
            }
        }
    } catch (error) {
        console.error('提交航中外业调查人员记录错误:', error);
        ElMessage.error('提交失败');
    }
};

// 监听任务名称变化，自动重新加载数据
watch(() => props.taskName, (newVal, oldVal) => {
    if (newVal && newVal !== oldVal) {
        console.log(`任务名称从 ${oldVal} 变更为 ${newVal}，重新加载数据`);
        loadData();
    }
}, { immediate: true }); // immediate: true 确保组件挂载时也执行一次

// 生命周期
onMounted(() => {
    // loadData() 已由 watch 的 immediate: true 处理
});
</script>

<style scoped>
.voyage-personnel {
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

.voyage-personnel-table {
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

.pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
}

.attachment-section {
    width: 100%;
}

.attachment-list {
    margin-top: 10px;
}

.attachment-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 10px;
    background: #f5f7fa;
    border-radius: 4px;
    margin-bottom: 5px;
}

.attachment-actions {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.no-attachment {
    color: #999;
    font-size: 12px;
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
:deep(.attachment-dialog .el-message-box__content) {
    max-height: 400px;
    overflow-y: auto;
}

:deep(.attachment-dialog .el-message-box__content::-webkit-scrollbar) {
    width: 6px;
}

:deep(.attachment-dialog .el-message-box__content::-webkit-scrollbar-track) {
    background: #f1f1f1;
    border-radius: 3px;
}

:deep(.attachment-dialog .el-message-box__content::-webkit-scrollbar-thumb) {
    background: #c0c4cc;
    border-radius: 3px;
}

:deep(.attachment-dialog .el-message-box__content::-webkit-scrollbar-thumb:hover) {
    background: #909399;
}
</style>
