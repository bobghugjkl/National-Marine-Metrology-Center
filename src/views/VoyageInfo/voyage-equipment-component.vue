<template>
    <div class="voyage-equipment">
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
            class="voyage-equipment-table"
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
            <el-table-column prop="name" label="仪器（标准物质）名称" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.name" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.name }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="category" label="类别" width="100" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-select v-model="row.category" size="small" @click.stop>
                            <el-option label="仪器" value="仪器"></el-option>
                            <el-option label="标准物质" value="标准物质"></el-option>
                            <el-option label="计量器具" value="计量器具"></el-option>
                        </el-select>
                    </template>
                    <span v-else>{{ row.category }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="number" label="编号" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.number" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.number }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="model" label="型号" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.model" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.model }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="traceability_method" label="量值溯源方式" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.traceability_method" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.traceability_method }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="calibration_date" label="检定/校准日期" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-date-picker
                            v-model="row.calibration_date"
                            type="date"
                            placeholder="选择日期"
                            size="small"
                            value-format="YYYY-MM-DD"
                            @click.stop
                        ></el-date-picker>
                    </template>
                    <span v-else>{{ row.calibration_date }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="certificate_number" label="证书编号" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.certificate_number" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.certificate_number }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="validity_period" label="有效期" width="100" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.validity_period" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.validity_period }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="calibration_organization" label="检定/校准机构" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.calibration_organization" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.calibration_organization }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="remarks" label="备注" width="150" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.remarks" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.remarks }}</span>
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

        <!-- 分页 -->
        <div class="pagination-wrapper">
            <el-pagination
                v-model:current-page="page.current"
                v-model:page-size="page.size"
                :total="page.total"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
        </div>

        <!-- 新增/编辑对话框 -->
        <el-dialog
            :title="dialogTitle"
            v-model="dialogVisible"
            width="800px"
            destroy-on-close
            :close-on-click-modal="false"
            @close="handleDialogClose"
        >
            <el-form
                ref="formRef"
                :model="formData"
                :rules="formRules"
                label-width="120px"
                size="small"
            >
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="航次任务名称" prop="task_name">
                            <el-input v-model="formData.task_name" placeholder="请输入航次任务名称"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="类别" prop="category">
                            <el-select v-model="formData.category" placeholder="请选择类别">
                                <el-option label="仪器" value="仪器"></el-option>
                                <el-option label="标准物质" value="标准物质"></el-option>
                                <el-option label="计量器具" value="计量器具"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="仪器名称" prop="name">
                            <el-input v-model="formData.name" placeholder="请输入仪器（标准物质）名称"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="编号" prop="number">
                            <el-input v-model="formData.number" placeholder="请输入编号"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="型号" prop="model">
                            <el-input v-model="formData.model" placeholder="请输入型号"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="量值溯源方式">
                            <el-input v-model="formData.traceability_method" placeholder="请输入量值溯源方式"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="检定/校准日期">
                            <el-date-picker
                                v-model="formData.calibration_date"
                                type="date"
                                placeholder="选择检定/校准日期"
                                value-format="YYYY-MM-DD"
                                style="width: 100%"
                            ></el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="证书编号">
                            <el-input v-model="formData.certificate_number" placeholder="请输入证书编号"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="有效期">
                            <el-input v-model="formData.validity_period" placeholder="请输入有效期"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="检定/校准机构">
                            <el-input v-model="formData.calibration_organization" placeholder="请输入检定/校准机构"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="备注">
                    <el-input
                        v-model="formData.remarks"
                        type="textarea"
                        :rows="3"
                        placeholder="请输入备注"
                    ></el-input>
                </el-form-item>
                <el-form-item label="附件上传">
                    <el-upload
                        ref="dialogUploadRef"
                        class="dialog-upload"
                        action=""
                        :http-request="handleDialogAttachmentUpload"
                        :file-list="formData.attachmentList || []"
                        :show-file-list="true"
                        list-type="text"
                        multiple
                        :limit="5"
                        :on-remove="handleDialogAttachmentRemove"
                    >
                        <el-button type="primary" size="small">选择文件</el-button>
                        <template #tip>
                            <div class="el-upload__tip">
                                支持jpg/png/pdf等格式,单个文件不超过10MB
                            </div>
                        </template>
                    </el-upload>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleDialogSubmit">确定</el-button>
                </span>
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
    fetchVoyageEquipmentList,
    createVoyageEquipment,
    updateVoyageEquipment,
    deleteVoyageEquipment,
    batchDeleteVoyageEquipment,
    uploadVoyageEquipmentAttachment
} from '@/api/voyage-equipment';
import * as XLSX from 'xlsx';

// 接口定义
interface VoyageEquipment {
    id?: number;
    task_name: string;
    category: string;
    name: string;
    number: string;
    model: string;
    traceability_method?: string;
    calibration_date?: string;
    certificate_number?: string;
    validity_period?: string;
    calibration_organization?: string;
    remarks?: string;
    attachmentList?: Array<{ name: string; url: string; uid: string }>;
    user_id?: number;
    create_time?: string;
    update_time?: string;
    isEditing?: boolean;
}

// Props定义
const props = defineProps<{
    taskName: string;
}>();

// 响应式数据
const tableData = ref<VoyageEquipment[]>([]);
const selectedRows = ref<VoyageEquipment[]>([]);
const page = reactive({
    current: 1,
    size: 10,
    total: 0
});

// 对话框相关
const dialogVisible = ref(false);
const dialogTitle = ref('新增航中仪器设备');
const isEdit = ref(false);
const editingId = ref<number | null>(null);

// 表单数据
const formData = reactive<VoyageEquipment>({
    task_name: props.taskName,
    category: '仪器',
    name: '',
    number: '',
    model: '',
    traceability_method: '',
    calibration_date: '',
    certificate_number: '',
    validity_period: '',
    calibration_organization: '',
    remarks: '',
    attachmentList: []
});

// 表单验证规则
const formRules = {
    task_name: [{ required: true, message: '请输入航次任务名称', trigger: 'blur' }],
    category: [{ required: true, message: '请选择类别', trigger: 'change' }],
    name: [{ required: true, message: '请输入仪器名称', trigger: 'blur' }],
    number: [{ required: true, message: '请输入编号', trigger: 'blur' }],
    model: [{ required: true, message: '请输入型号', trigger: 'blur' }]
};

// 表单引用
const formRef = ref();
const tableRef = ref();
const uploadRef = ref();

// 上传引用（用于附件）
const attachmentUploadRef = ref();

// 计算属性
const hasSelection = computed(() => selectedRows.value.length > 0);

// 方法定义
const loadData = async () => {
    try {
        console.log('开始加载航中仪器设备数据，任务名称:', props.taskName);

        const response = await fetchVoyageEquipmentList({ task_name: props.taskName });
        console.log('API响应:', response);

        if (response && response.code === 200) {
            console.log('数据加载成功，记录数量:', response.data?.length || 0);
            // 添加isEditing属性
            tableData.value = (response.data || []).map((item: any) => ({
                ...item,
                isEditing: false,
                attachmentList: item.attachments || []
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
        }
        ElMessage.error(`加载数据失败: ${error.message || '网络错误'}`);
    }
};

// 表格选择变化
const handleSelectionChange = (selection: VoyageEquipment[]) => {
    selectedRows.value = selection;
};

// 行点击事件
const handleRowClick = (row: VoyageEquipment) => {
    // 如果点击的是操作列，不触发跳转
    if (row.isEditing) {
        return;
    }
    // 可以在这里添加行点击的逻辑，比如查看详情
};

// 新增行
const handleAddRow = () => {
    dialogTitle.value = '新增航中仪器设备';
    isEdit.value = false;
    editingId.value = null;

    // 重置表单数据
    Object.assign(formData, {
        task_name: props.taskName,
        category: '仪器',
        name: '',
        number: '',
        model: '',
        traceability_method: '',
        calibration_date: '',
        certificate_number: '',
        validity_period: '',
        calibration_organization: '',
        remarks: '',
        attachmentList: []
    });

    dialogVisible.value = true;
};

// 编辑行
const handleEdit = (row: VoyageEquipment) => {
    // 先保存当前正在编辑的行
    const editingRow = tableData.value.find(item => item.isEditing);
    if (editingRow) {
        handleCancel(editingRow);
    }

    // 设置编辑状态
    row.isEditing = true;
};

// 保存行
const handleSave = async (row: VoyageEquipment) => {
    try {
        const updateData = {
            task_name: row.task_name,
            category: row.category,
            name: row.name,
            number: row.number,
            model: row.model,
            traceability_method: row.traceability_method,
            calibration_date: row.calibration_date,
            certificate_number: row.certificate_number,
            validity_period: row.validity_period,
            calibration_organization: row.calibration_organization,
            remarks: row.remarks,
            attachmentList: row.attachmentList || []
        };

        if (row.id) {
            // 更新现有记录
            const response = await updateVoyageEquipment(row.id, updateData);
            if (response && response.code === 200) {
                ElMessage.success('保存成功');
                row.isEditing = false;
            } else {
                ElMessage.error(response?.msg || '保存失败');
            }
        } else {
            // 创建新记录
            const response = await createVoyageEquipment(updateData);
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
        console.error('保存失败:', error);
        ElMessage.error('保存失败');
    }
};

// 取消编辑
const handleCancel = (row: VoyageEquipment) => {
    if (row.id) {
        // 如果是编辑现有记录，取消编辑状态
        row.isEditing = false;
    } else {
        // 如果是新增记录，从表格中移除
        const index = tableData.value.findIndex(item => item === row);
        if (index > -1) {
            tableData.value.splice(index, 1);
        }
    }
};

// 删除行
const handleDelete = async (row: VoyageEquipment) => {
    try {
        const confirmResult = await ElMessageBox.confirm(
            `确定要删除航中仪器设备"${row.name}"吗？此操作不可撤销。`,
            '删除确认',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }
        );

        if (confirmResult === 'confirm') {
            if (row.id) {
                const response = await deleteVoyageEquipment(row.id);
                if (response && response.code === 200) {
                    ElMessage.success('删除成功');
                    loadData(); // 重新加载数据
                } else {
                    ElMessage.error(response?.msg || '删除失败');
                }
            } else {
                // 删除新增但未保存的行
                const index = tableData.value.findIndex(item => item === row);
                if (index > -1) {
                    tableData.value.splice(index, 1);
                }
            }
        }
    } catch (error) {
        if (error !== 'cancel') {
            console.error('删除失败:', error);
            ElMessage.error('删除失败');
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
        const confirmResult = await ElMessageBox.confirm(
            `确定要删除选中的${selectedRows.value.length}条记录吗？此操作不可撤销。`,
            '批量删除确认',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }
        );

        if (confirmResult === 'confirm') {
            const ids = selectedRows.value.map(row => row.id).filter(id => id !== undefined) as number[];

            if (ids.length > 0) {
                const response = await batchDeleteVoyageEquipment(ids);
                if (response && response.code === 200) {
                    ElMessage.success('批量删除成功');
                    loadData(); // 重新加载数据
                } else {
                    ElMessage.error(response?.msg || '批量删除失败');
                }
            } else {
                // 删除本地的新增行
                selectedRows.value.forEach(row => {
                    const index = tableData.value.findIndex(item => item === row);
                    if (index > -1) {
                        tableData.value.splice(index, 1);
                    }
                });
                ElMessage.success('删除成功');
            }

            selectedRows.value = [];
        }
    } catch (error) {
        if (error !== 'cancel') {
            console.error('批量删除失败:', error);
            ElMessage.error('批量删除失败');
        }
    }
};

// 附件上传处理
const handleAttachmentUpload = async (params: any, row: VoyageEquipment) => {
    try {
        const response = await uploadVoyageEquipmentAttachment(params.file);
        if (response && response.code === 200) {
            // 初始化attachmentList
            if (!row.attachmentList) {
                row.attachmentList = [];
            }

            // 添加新附件
            row.attachmentList.push({
                name: response.data.filename,
                url: response.data.url,
                uid: response.data.size
            });

            ElMessage.success('附件上传成功');
        } else {
            ElMessage.error(response?.msg || '附件上传失败');
        }
    } catch (error) {
        console.error('附件上传失败:', error);
        ElMessage.error('附件上传失败');
    }
};

// 查看附件
const handleViewAttachment = (row: VoyageEquipment) => {
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

// 导入Excel
const handleImport = async (params: any) => {
    try {
        // 这里可以实现Excel导入逻辑
        ElMessage.info('Excel导入功能开发中...');
    } catch (error) {
        console.error('导入失败:', error);
        ElMessage.error('导入失败');
    }
};

// 导出Excel
const handleExport = () => {
    try {
        const exportData = tableData.value.map(item => ({
            '航次任务名称': item.task_name,
            '类别': item.category,
            '仪器名称': item.name,
            '编号': item.number,
            '型号': item.model,
            '量值溯源方式': item.traceability_method,
            '检定日期': item.calibration_date,
            '证书编号': item.certificate_number,
            '有效期': item.validity_period,
            '检定机构': item.calibration_organization,
            '备注': item.remarks
        }));

        const worksheet = XLSX.utils.json_to_sheet(exportData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, '航中仪器设备一览表');
        XLSX.writeFile(workbook, `航中仪器设备一览表_${props.taskName}.xlsx`);

        ElMessage.success('导出成功');
    } catch (error) {
        ElMessage.error('导出失败');
    }
};

// 保存所有
const handleSaveAll = async () => {
    try {
        const editingRows = tableData.value.filter(row => row.isEditing);

        if (editingRows.length === 0) {
            ElMessage.info('没有需要保存的数据');
            return;
        }

        let successCount = 0;
        for (const row of editingRows) {
            try {
                await handleSave(row);
                successCount++;
            } catch (error) {
                console.error('保存行失败:', error);
            }
        }

        ElMessage.success(`成功保存${successCount}条记录`);
    } catch (error) {
        console.error('保存所有失败:', error);
        ElMessage.error('保存失败');
    }
};

// 分页相关
const handleSizeChange = (size: number) => {
    page.size = size;
    page.current = 1;
    loadData();
};

const handleCurrentChange = (current: number) => {
    page.current = current;
    loadData();
};

// 对话框附件上传处理
const handleDialogAttachmentUpload = async (params: any) => {
    try {
        const response = await uploadVoyageEquipmentAttachment(params.file);
        if (response && response.code === 200) {
            // 初始化attachmentList
            if (!formData.attachmentList) {
                formData.attachmentList = [];
            }

            // 添加新附件
            formData.attachmentList.push({
                name: response.data.filename,
                url: response.data.url,
                uid: response.data.size
            });

            ElMessage.success('附件上传成功');
        } else {
            ElMessage.error(response?.msg || '附件上传失败');
        }
    } catch (error) {
        console.error('附件上传失败:', error);
        ElMessage.error('附件上传失败');
    }
};

// 对话框附件删除处理
const handleDialogAttachmentRemove = (file: any, fileList: any[]) => {
    formData.attachmentList = fileList;
};

// 对话框相关方法
const handleDialogClose = () => {
    dialogVisible.value = false;
    formRef.value?.resetFields();
    // 重置附件列表
    formData.attachmentList = [];
};

const handleDialogSubmit = async () => {
    if (!formRef.value) return;

    formRef.value.validate(async (valid: boolean) => {
        if (valid) {
            try {
                const submitData = {
                    task_name: formData.task_name,
                    category: formData.category,
                    name: formData.name,
                    number: formData.number,
                    model: formData.model,
                    traceability_method: formData.traceability_method,
                    calibration_date: formData.calibration_date,
                    certificate_number: formData.certificate_number,
                    validity_period: formData.validity_period,
                    calibration_organization: formData.calibration_organization,
                    remarks: formData.remarks,
                    attachmentList: formData.attachmentList || []
                };

                if (isEdit.value && editingId.value) {
                    // 编辑模式
                    const response = await updateVoyageEquipment(editingId.value, submitData);
                    if (response && response.code === 200) {
                        ElMessage.success('更新成功');
                        dialogVisible.value = false;
                        loadData();
                    } else {
                        ElMessage.error(response?.msg || '更新失败');
                    }
                } else {
                    // 新增模式
                    const response = await createVoyageEquipment(submitData);
                    if (response && response.code === 200) {
                        ElMessage.success('创建成功');
                        dialogVisible.value = false;
                        loadData();
                    } else {
                        ElMessage.error(response?.msg || '创建失败');
                    }
                }
            } catch (error) {
                console.error('提交失败:', error);
                ElMessage.error('提交失败');
            }
        }
    });
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
.voyage-equipment {
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

.voyage-equipment-table {
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

/* 对话框附件上传样式 */
.dialog-upload {
    width: 100%;
}

.dialog-upload .el-button {
    margin: 0;
}
</style>
