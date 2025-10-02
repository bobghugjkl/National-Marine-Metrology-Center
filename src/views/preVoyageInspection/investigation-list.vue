<template>
	<div>
		<!-- 页面标题和操作按钮 -->
		<div class="page-header">
			<h2>外业调查项目/仪器比测统计表</h2>
			<div class="header-buttons">
				<el-button type="success" :icon="Download" @click="handleDownloadTemplate">
					下载excel模板
				</el-button>
				<el-button type="primary" :icon="Upload" @click="handleImportExcel">
					导入excel文件
				</el-button>
				<el-button type="warning" :icon="CirclePlusFilled" @click="visible = true">
					新增调查项目
				</el-button>
			</div>
		</div>

		<!-- 搜索区域 -->
		<TableSearch :query="query" :options="searchOpt" :search="handleSearch" />

		<!-- 表格区域 -->
		<div class="container">
			<TableCustom
				:columns="columns"
				:tableData="tableData"
				:total="page.total"
				:pageSize="page.size"
				:viewFunc="handleView"
				:delFunc="handleDelete"
				:editFunc="handleEdit"
				:refresh="getData"
				:currentPage="page.index"
				:changePage="changePage"
			>
				<template #toolbarBtn>
					<el-button type="primary" :icon="CirclePlusFilled" @click="handleAdd">
						增加
					</el-button>
					<el-button type="success" :icon="Download" @click="handleDownloadTemplate">
						下载模板
					</el-button>
					<el-button type="warning" :icon="Upload" @click="handleImportExcel">
						导入Excel
					</el-button>
					<el-button type="danger" @click="handleBatchDelete" :disabled="selectedRows.length === 0">
						批量删除
					</el-button>
				</template>

				<!-- 调查项目列 -->
				<template #investigation_item="{ rows }">
					<el-tag type="primary">{{ rows.investigation_item }}</el-tag>
				</template>

				<!-- 比测结果列 -->
				<template #comparison_result="{ rows }">
					<el-tag :type="getResultType(rows.comparison_result)">
						{{ rows.comparison_result || '-' }}
					</el-tag>
				</template>

				<!-- 附件列 -->
				<template #attachment="{ rows }">
					<el-button v-if="rows.attachment" type="text" size="small" @click="handleViewAttachment(rows)">
						查看附件
					</el-button>
					<span v-else class="no-attachment">无附件</span>
				</template>

				<!-- 操作列 -->
				<template #operator="{ rows }">
					<el-button type="primary" size="small" @click="handleEdit(rows)">编辑</el-button>
					<el-button type="info" size="small" @click="handleView(rows)">查看</el-button>
					<el-button type="danger" size="small" @click="handleDelete(rows)">删除</el-button>
				</template>
			</TableCustom>
		</div>

		<!-- 新增/编辑弹窗 -->
		<el-dialog
			:title="isEdit ? '编辑调查项目' : '新增调查项目'"
			v-model="visible"
			width="900px"
			destroy-on-close
			:close-on-click-modal="false"
			@close="closeDialog"
		>
			<el-form
				ref="formRef"
				:model="formData"
				:rules="formRules"
				label-width="140px"
				:label-position="'right'"
			>
				<el-form-item label="航次任务名称" prop="task_name">
					<el-input v-model="formData.task_name" placeholder="请输入航次任务名称" />
				</el-form-item>

				<el-form-item label="调查项目/仪器" prop="investigation_item">
					<el-input v-model="formData.investigation_item" placeholder="请输入调查项目或仪器名称" />
				</el-form-item>

				<el-row :gutter="20">
					<el-col :span="12">
						<el-form-item label="比测单位甲仪器" prop="unit_a_equipment">
							<el-input v-model="formData.unit_a_equipment" placeholder="请输入比测单位甲仪器" />
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="比测单位乙仪器" prop="unit_b_equipment">
							<el-input v-model="formData.unit_b_equipment" placeholder="请输入比测单位乙仪器" />
						</el-form-item>
					</el-col>
				</el-row>

				<el-row :gutter="20">
					<el-col :span="8">
						<el-form-item label="比测时间" prop="comparison_time">
							<el-date-picker
								v-model="formData.comparison_time"
								type="datetime"
								placeholder="选择比测时间"
								value-format="YYYY-MM-DD HH:mm:ss"
								style="width: 100%"
							/>
						</el-form-item>
					</el-col>
					<el-col :span="8">
						<el-form-item label="比测地点" prop="comparison_location">
							<el-input v-model="formData.comparison_location" placeholder="请输入比测地点" />
						</el-form-item>
					</el-col>
					<el-col :span="8">
						<el-form-item label="比测结果" prop="comparison_result">
							<el-select v-model="formData.comparison_result" placeholder="请选择比测结果" style="width: 100%">
								<el-option label="一致" value="一致" />
								<el-option label="基本一致" value="基本一致" />
								<el-option label="差异较大" value="差异较大" />
								<el-option label="需要进一步验证" value="需要进一步验证" />
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>

				<el-form-item label="备注" prop="remarks">
					<el-input
						v-model="formData.remarks"
						type="textarea"
						:rows="3"
						placeholder="请输入备注信息"
					/>
				</el-form-item>

				<el-form-item label="附件">
					<el-upload
						ref="uploadRef"
						:action="uploadUrl"
						:headers="uploadHeaders"
						:multiple="true"
						:limit="5"
						:on-success="handleUploadSuccess"
						:on-error="handleUploadError"
						:on-remove="handleFileRemove"
						:file-list="fileList"
					>
						<el-button slot="trigger" size="small" type="primary">选择文件</el-button>
						<div slot="tip" class="el-upload__tip">
							只能上传jpg/png/pdf文件，且不超过10MB
						</div>
					</el-upload>
				</el-form-item>
			</el-form>

			<template #footer>
				<span class="dialog-footer">
					<el-button @click="closeDialog">取消</el-button>
					<el-button type="primary" @click="handleSubmit">确定</el-button>
				</span>
			</template>
		</el-dialog>

		<!-- 查看详情弹窗 -->
		<el-dialog title="调查项目详情" v-model="visible1" width="900px" destroy-on-close>
			<el-descriptions :column="2" border>
				<el-descriptions-item label="航次任务名称">{{ viewData.task_name }}</el-descriptions-item>
				<el-descriptions-item label="调查项目/仪器">{{ viewData.investigation_item }}</el-descriptions-item>
				<el-descriptions-item label="比测单位甲仪器">{{ viewData.unit_a_equipment }}</el-descriptions-item>
				<el-descriptions-item label="比测单位乙仪器">{{ viewData.unit_b_equipment }}</el-descriptions-item>
				<el-descriptions-item label="比测时间">{{ viewData.comparison_time }}</el-descriptions-item>
				<el-descriptions-item label="比测地点">{{ viewData.comparison_location }}</el-descriptions-item>
				<el-descriptions-item label="比测结果">{{ viewData.comparison_result }}</el-descriptions-item>
				<el-descriptions-item label="备注" :span="2">{{ viewData.remarks }}</el-descriptions-item>
				<el-descriptions-item label="附件" :span="2">
					<div v-if="viewData.attachments && viewData.attachments.length > 0">
						<el-button
							v-for="(file, index) in viewData.attachments"
							:key="index"
							type="text"
							size="small"
							@click="handleDownloadFile(file)"
						>
							{{ file.name }}
						</el-button>
					</div>
					<span v-else>无附件</span>
				</el-descriptions-item>
			</el-descriptions>
		</el-dialog>

		<!-- Excel导入弹窗 -->
		<el-dialog title="导入Excel文件" v-model="importVisible" width="500px">
			<el-upload
				ref="importUploadRef"
				drag
				:action="importUrl"
				:headers="uploadHeaders"
				:multiple="false"
				:accept="'.xlsx,.xls'"
				:on-success="handleImportSuccess"
				:on-error="handleImportError"
				:before-upload="beforeImportUpload"
			>
				<i class="el-icon-upload"></i>
				<div class="el-upload__text">将Excel文件拖到此处，或<em>点击上传</em></div>
				<div class="el-upload__tip">只能上传.xlsx或.xls文件，且不超过10MB</div>
			</el-upload>
		</el-dialog>
	</div>
</template>

<script setup lang="ts" name="InvestigationList">
import { ref, reactive, computed } from 'vue';
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus';
import { CirclePlusFilled, Download, Upload } from '@element-plus/icons-vue';
import {
	fetchInvestigationList,
	createInvestigation,
	updateInvestigation,
	deleteInvestigation,
	batchDeleteInvestigation,
	downloadInvestigationTemplate,
	importInvestigationExcel,
	exportInvestigationData
} from '@/api/investigation';
import TableCustom from '@/components/table-custom.vue';
import TableSearch from '@/components/table-search.vue';
import { TableItem } from '@/types/table';
import { FormOption, FormOptionList } from '@/types/form-option';

// 查询相关
const query = reactive({
	task_name: '',
	investigation_item: '',
	unit_a_equipment: '',
	unit_b_equipment: '',
	comparison_location: ''
});

const searchOpt = ref<FormOptionList[]>([
	{ type: 'input', label: '航次任务名称：', prop: 'task_name' },
	{ type: 'input', label: '调查项目：', prop: 'investigation_item' },
	{ type: 'input', label: '比测单位甲仪器：', prop: 'unit_a_equipment' },
	{ type: 'input', label: '比测单位乙仪器：', prop: 'unit_b_equipment' },
	{ type: 'input', label: '比测地点：', prop: 'comparison_location' }
]);

const handleSearch = () => {
	changePage(1);
};

// 表格相关
const columns = ref([
	{ type: 'selection' },
	{ type: 'index', label: '序号', width: 55, align: 'center' },
	{
		prop: 'task_name',
		label: '航次任务名称',
		minWidth: 150
	},
	{
		prop: 'investigation_item',
		label: '调查项目/仪器',
		minWidth: 150,
		slot: 'investigation_item'
	},
	{
		prop: 'unit_a_equipment',
		label: '比测单位甲仪器',
		minWidth: 150
	},
	{
		prop: 'unit_b_equipment',
		label: '比测单位乙仪器',
		minWidth: 150
	},
	{
		prop: 'comparison_time',
		label: '比测时间',
		minWidth: 150
	},
	{
		prop: 'comparison_location',
		label: '比测地点',
		minWidth: 120
	},
	{
		prop: 'comparison_result',
		label: '比测结果',
		minWidth: 120,
		slot: 'comparison_result'
	},
	{
		prop: 'remarks',
		label: '备注',
		minWidth: 120
	},
	{
		prop: 'attachment',
		label: '附件',
		minWidth: 100,
		slot: 'attachment'
	},
	{
		prop: 'operator',
		label: '操作',
		width: 200,
		slot: 'operator'
	}
]);

const page = reactive({
	index: 1,
	size: 10,
	total: 0
});

const tableData = ref<TableItem[]>([]);
const selectedRows = ref<TableItem[]>([]);

// 获取数据
const getData = async () => {
	try {
		const params = {
			page: page.index,
			pageSize: page.size,
			...query
		};

		const res = await fetchInvestigationList(params);
		tableData.value = res.data.list || [];
		page.total = res.data.total || 0;
	} catch (error) {
		console.error('获取调查项目数据失败:', error);
		ElMessage.error('获取数据失败');
	}
};

// 分页
const changePage = (val: number) => {
	page.index = val;
	getData();
};

// 获取比测结果状态样式
const getResultType = (result: string) => {
	const resultMap: { [key: string]: string } = {
		'一致': 'success',
		'基本一致': 'warning',
		'差异较大': 'danger',
		'需要进一步验证': 'info'
	};
	return resultMap[result] || 'info';
};

// 新增/编辑弹窗相关
const visible = ref(false);
const isEdit = ref(false);
const formRef = ref<FormInstance>();
const fileList = ref<any[]>([]);
const uploadRef = ref();

const formData = ref({
	task_name: '',
	investigation_item: '',
	unit_a_equipment: '',
	unit_b_equipment: '',
	comparison_time: '',
	comparison_location: '',
	comparison_result: '',
	remarks: '',
	attachments: []
});

const formRules = {
	task_name: [
		{ required: true, message: '请输入航次任务名称', trigger: 'blur' }
	],
	investigation_item: [
		{ required: true, message: '请输入调查项目/仪器', trigger: 'blur' }
	],
	unit_a_equipment: [
		{ required: true, message: '请输入比测单位甲仪器', trigger: 'blur' }
	],
	unit_b_equipment: [
		{ required: true, message: '请输入比测单位乙仪器', trigger: 'blur' }
	],
	comparison_time: [
		{ required: true, message: '请选择比测时间', trigger: 'change' }
	],
	comparison_location: [
		{ required: true, message: '请输入比测地点', trigger: 'blur' }
	],
	comparison_result: [
		{ required: true, message: '请选择比测结果', trigger: 'change' }
	]
};

// 上传相关
const uploadUrl = `${import.meta.env.VITE_APP_BASE_API || 'http://localhost:5000/api'}/investigation-projects/upload`;
const importUrl = `${import.meta.env.VITE_APP_BASE_API || 'http://localhost:5000/api'}/investigation-projects/import`;

const uploadHeaders = computed(() => {
	const token = localStorage.getItem('token');
	return token ? { Authorization: `Bearer ${token}` } : {};
});

// 新增
const handleAdd = () => {
	isEdit.value = false;
	resetForm();
	visible.value = true;
};

// 编辑
const handleEdit = (row: TableItem) => {
	isEdit.value = true;
	formData.value = { ...row };
	fileList.value = row.attachments || [];
	visible.value = true;
};

// 删除
const handleDelete = async (row: TableItem) => {
	try {
		await ElMessageBox.confirm(
			`确定要删除调查项目"${row.investigation_item}"吗？此操作不可恢复！`,
			'删除确认',
			{
				confirmButtonText: '确定删除',
				cancelButtonText: '取消',
				type: 'warning'
			}
		);

		await deleteInvestigation(row.id);
		ElMessage.success('删除成功');
		getData();
	} catch (error) {
		if (error !== 'cancel') {
			ElMessage.error('删除失败');
		}
	}
};

// 批量删除
const handleBatchDelete = async () => {
	if (selectedRows.value.length === 0) {
		ElMessage.warning('请选择要删除的记录');
		return;
	}

	try {
		const investigationItems = selectedRows.value.map(row => row.investigation_item).join('、');
		await ElMessageBox.confirm(
			`确定要删除选中的 ${selectedRows.value.length} 个调查项目吗？此操作不可恢复！`,
			'批量删除确认',
			{
				confirmButtonText: '确定删除',
				cancelButtonText: '取消',
				type: 'warning'
			}
		);

		const ids = selectedRows.value.map(row => row.id);
		await batchDeleteInvestigation(ids);
		ElMessage.success('批量删除成功');
		selectedRows.value = [];
		getData();
	} catch (error) {
		if (error !== 'cancel') {
			ElMessage.error('批量删除失败');
		}
	}
};

// 提交表单
const handleSubmit = async () => {
	if (!formRef.value) return;

	try {
		await formRef.value.validate();

		const submitData = {
			...formData.value,
			attachments: fileList.value
		};

		if (isEdit.value) {
			await updateInvestigation(formData.value.id, submitData);
			ElMessage.success('更新成功');
		} else {
			await createInvestigation(submitData);
			ElMessage.success('新增成功');
		}

		closeDialog();
		getData();
	} catch (error) {
		console.error('提交失败:', error);
		ElMessage.error('提交失败');
	}
};

// 关闭弹窗
const closeDialog = () => {
	visible.value = false;
	isEdit.value = false;
	resetForm();
};

// 重置表单
const resetForm = () => {
	if (formRef.value) {
		formRef.value.resetFields();
	}
	fileList.value = [];
};

// 查看详情
const visible1 = ref(false);
const viewData = ref<any>({});

const handleView = (row: TableItem) => {
	viewData.value = { ...row };
	visible1.value = true;
};

// 下载模板
const handleDownloadTemplate = async () => {
	try {
		const response = await downloadInvestigationTemplate();
		// 处理文件下载
		const blob = new Blob([response.data]);
		const url = window.URL.createObjectURL(blob);
		const link = document.createElement('a');
		link.href = url;
		link.download = '调查项目模板.xlsx';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		window.URL.revokeObjectURL(url);

		ElMessage.success('模板下载成功');
	} catch (error) {
		console.error('下载模板失败:', error);
		ElMessage.error('下载模板失败');
	}
};

// 导入Excel
const importVisible = ref(false);
const importUploadRef = ref();

const handleImportExcel = () => {
	importVisible.value = true;
};

const beforeImportUpload = (file: File) => {
	const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
					file.type === 'application/vnd.ms-excel';
	const isLt10M = file.size / 1024 / 1024 < 10;

	if (!isExcel) {
		ElMessage.error('只能上传Excel文件!');
		return false;
	}
	if (!isLt10M) {
		ElMessage.error('文件大小不能超过10MB!');
		return false;
	}
	return true;
};

const handleImportSuccess = (response: any) => {
	importVisible.value = false;
	if (response.code === 200) {
		ElMessage.success(`成功导入 ${response.data.imported_count} 条记录`);
		getData();
	} else {
		ElMessage.error(response.message || '导入失败');
	}
};

const handleImportError = (error: any) => {
	console.error('导入失败:', error);
	ElMessage.error('导入失败');
};

// 文件上传相关
const handleUploadSuccess = (response: any, file: any) => {
	if (response.code === 200) {
		fileList.value.push({
			name: file.name,
			url: response.data.url,
			id: response.data.id
		});
		ElMessage.success('文件上传成功');
	} else {
		ElMessage.error(response.message || '上传失败');
	}
};

const handleUploadError = (error: any) => {
	console.error('上传失败:', error);
	ElMessage.error('上传失败');
};

const handleFileRemove = (file: any) => {
	const index = fileList.value.findIndex(item => item.id === file.id);
	if (index > -1) {
		fileList.value.splice(index, 1);
	}
};

// 查看附件
const handleViewAttachment = (row: TableItem) => {
	if (row.attachments && row.attachments.length > 0) {
		ElMessage.info('附件预览功能开发中...');
	}
};

// 下载文件
const handleDownloadFile = (file: any) => {
	window.open(file.url);
};

// 初始化
getData();
</script>

<style scoped>
.page-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20px;
	padding-bottom: 15px;
	border-bottom: 1px solid #e4e7ed;
}

.page-header h2 {
	margin: 0;
	color: #303133;
	font-size: 20px;
	font-weight: 600;
}

.header-buttons {
	display: flex;
	gap: 10px;
}

.no-attachment {
	color: #909399;
	font-size: 12px;
}

.dialog-footer {
	text-align: right;
}

:deep(.el-descriptions__title) {
	font-size: 16px;
	font-weight: 600;
	margin-bottom: 15px;
}

:deep(.el-descriptions__label) {
	width: 140px;
	font-weight: 500;
	color: #606266;
}
</style>
