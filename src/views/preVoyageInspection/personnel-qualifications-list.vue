<template>
	<div>
		<!-- 页面标题和操作按钮 -->
		<div class="page-header">
			<h2>外业调查人员资质一览表</h2>
			<div class="header-buttons">
				<el-button type="success" :icon="Download" @click="handleDownloadTemplate">
					下载excel模板
				</el-button>
				<el-button type="primary" :icon="Upload" @click="handleImportExcel">
					导入excel文件
				</el-button>
				<el-button type="warning" :icon="CirclePlusFilled" @click="visible = true">
					新增人员资质
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

				<!-- 性别列 -->
				<template #sex="{ rows }">
					<el-tag :type="rows.sex === '男' ? 'primary' : 'success'">
						{{ rows.sex }}
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
			:title="isEdit ? '编辑人员资质' : '新增人员资质'"
			v-model="visible"
			width="800px"
			destroy-on-close
			:close-on-click-modal="false"
			@close="closeDialog"
		>
			<el-form
				ref="formRef"
				:model="formData"
				:rules="formRules"
				label-width="120px"
				:label-position="'right'"
			>
				<el-row :gutter="20">
					<el-col :span="12">
						<el-form-item label="航次任务名称" prop="task_name">
							<el-input v-model="formData.task_name" placeholder="请输入航次任务名称" />
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="姓名" prop="name">
							<el-input v-model="formData.name" placeholder="请输入姓名" />
						</el-form-item>
					</el-col>
				</el-row>

				<el-row :gutter="20">
					<el-col :span="12">
						<el-form-item label="性别" prop="sex">
							<el-radio-group v-model="formData.sex">
								<el-radio value="男">男</el-radio>
								<el-radio value="女">女</el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="出生年月" prop="birthdate">
							<el-date-picker
								v-model="formData.birthdate"
								type="date"
								placeholder="选择出生年月"
								value-format="YYYY-MM-DD"
								style="width: 100%"
							/>
						</el-form-item>
					</el-col>
				</el-row>

				<el-row :gutter="20">
					<el-col :span="12">
						<el-form-item label="职称" prop="professional_title">
							<el-input v-model="formData.professional_title" placeholder="请输入职称" />
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="工作单位" prop="employer">
							<el-input v-model="formData.employer" placeholder="请输入工作单位" />
						</el-form-item>
					</el-col>
				</el-row>

				<el-form-item label="从事专业" prop="specialty">
					<el-input v-model="formData.specialty" placeholder="请输入从事专业" />
				</el-form-item>

				<el-form-item label="本航次操作仪器" prop="instruments">
					<el-input v-model="formData.instruments" placeholder="请输入本航次操作仪器" />
				</el-form-item>

				<el-form-item label="培训情况" prop="training">
					<el-input
						v-model="formData.training"
						type="textarea"
						:rows="3"
						placeholder="请输入培训情况"
					/>
				</el-form-item>

				<el-form-item label="备注" prop="remarks">
					<el-input
						v-model="formData.remarks"
						type="textarea"
						:rows="3"
						placeholder="请输入备注"
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
		<el-dialog title="人员资质详情" v-model="visible1" width="800px" destroy-on-close>
			<el-descriptions :column="2" border>
				<el-descriptions-item label="航次任务名称">{{ viewData.task_name }}</el-descriptions-item>
				<el-descriptions-item label="姓名">{{ viewData.name }}</el-descriptions-item>
				<el-descriptions-item label="性别">{{ viewData.sex }}</el-descriptions-item>
				<el-descriptions-item label="出生年月">{{ viewData.birthdate }}</el-descriptions-item>
				<el-descriptions-item label="职称">{{ viewData.professional_title }}</el-descriptions-item>
				<el-descriptions-item label="工作单位">{{ viewData.employer }}</el-descriptions-item>
				<el-descriptions-item label="从事专业">{{ viewData.specialty }}</el-descriptions-item>
				<el-descriptions-item label="本航次操作仪器">{{ viewData.instruments }}</el-descriptions-item>
				<el-descriptions-item label="培训情况" :span="2">{{ viewData.training }}</el-descriptions-item>
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

<script setup lang="ts" name="PersonnelQualificationsList">
import { ref, reactive, computed } from 'vue';
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus';
import { CirclePlusFilled, Download, Upload } from '@element-plus/icons-vue';
import {
	fetchPersonnelQualifications,
	createPersonnelQualification,
	updatePersonnelQualification,
	deletePersonnelQualification,
	batchDeletePersonnelQualifications,
	downloadExcelTemplate,
	importExcelFile,
	exportPersonnelQualifications
} from '@/api/personnel';
import TableCustom from '@/components/table-custom.vue';
import TableSearch from '@/components/table-search.vue';
import { TableItem } from '@/types/table';
import { FormOption, FormOptionList } from '@/types/form-option';

// 查询相关
const query = reactive({
	task_name: '',
	name: '',
	employer: ''
});

const searchOpt = ref<FormOptionList[]>([
	{ type: 'input', label: '航次任务名称：', prop: 'task_name' },
	{ type: 'input', label: '姓名：', prop: 'name' },
	{ type: 'input', label: '工作单位：', prop: 'employer' }
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
		prop: 'name',
		label: '姓名',
		minWidth: 100
	},
	{
		prop: 'sex',
		label: '性别',
		minWidth: 60,
		slot: 'sex'
	},
	{
		prop: 'birthdate',
		label: '出生年月',
		minWidth: 100
	},
	{
		prop: 'professional_title',
		label: '职称',
		minWidth: 100
	},
	{
		prop: 'employer',
		label: '工作单位',
		minWidth: 150
	},
	{
		prop: 'specialty',
		label: '从事专业',
		minWidth: 120
	},
	{
		prop: 'instruments',
		label: '本航次操作仪器',
		minWidth: 150
	},
	{
		prop: 'training',
		label: '培训情况',
		minWidth: 150
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

		const res = await fetchPersonnelQualifications(params);
		tableData.value = res.data.list || [];
		page.total = res.data.total || 0;
	} catch (error) {
		console.error('获取人员资质数据失败:', error);
		ElMessage.error('获取数据失败');
	}
};

// 分页
const changePage = (val: number) => {
	page.index = val;
	getData();
};

// 新增/编辑弹窗相关
const visible = ref(false);
const isEdit = ref(false);
const formRef = ref<FormInstance>();
const fileList = ref<any[]>([]);
const uploadRef = ref();

const formData = ref({
	task_name: '',
	name: '',
	sex: '男',
	birthdate: '',
	professional_title: '',
	employer: '',
	specialty: '',
	instruments: '',
	training: '',
	remarks: '',
	attachments: []
});

const formRules = {
	task_name: [
		{ required: true, message: '请输入航次任务名称', trigger: 'blur' }
	],
	name: [
		{ required: true, message: '请输入姓名', trigger: 'blur' }
	],
	sex: [
		{ required: true, message: '请选择性别', trigger: 'change' }
	],
	birthdate: [
		{ required: true, message: '请选择出生年月', trigger: 'change' }
	],
	professional_title: [
		{ required: true, message: '请输入职称', trigger: 'blur' }
	],
	employer: [
		{ required: true, message: '请输入工作单位', trigger: 'blur' }
	],
	specialty: [
		{ required: true, message: '请输入从事专业', trigger: 'blur' }
	]
};

// 上传相关
const uploadUrl = `${import.meta.env.VITE_APP_BASE_API || 'http://localhost:5000/api'}/personnel-qualifications/upload`;
const importUrl = `${import.meta.env.VITE_APP_BASE_API || 'http://localhost:5000/api'}/personnel-qualifications/import`;

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
			`确定要删除人员"${row.name}"的资质记录吗？此操作不可恢复！`,
			'删除确认',
			{
				confirmButtonText: '确定删除',
				cancelButtonText: '取消',
				type: 'warning'
			}
		);

		await deletePersonnelQualification(row.id);
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
		const names = selectedRows.value.map(row => row.name).join('、');
		await ElMessageBox.confirm(
			`确定要删除选中的 ${selectedRows.value.length} 条记录吗？此操作不可恢复！`,
			'批量删除确认',
			{
				confirmButtonText: '确定删除',
				cancelButtonText: '取消',
				type: 'warning'
			}
		);

		const ids = selectedRows.value.map(row => row.id);
		await batchDeletePersonnelQualifications(ids);
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
			await updatePersonnelQualification(formData.value.id, submitData);
			ElMessage.success('更新成功');
		} else {
			await createPersonnelQualification(submitData);
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
		const response = await downloadExcelTemplate();
		// 处理文件下载
		const blob = new Blob([response.data]);
		const url = window.URL.createObjectURL(blob);
		const link = document.createElement('a');
		link.href = url;
		link.download = '人员资质模板.xlsx';
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
		// 这里可以实现附件预览功能
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
	width: 120px;
	font-weight: 500;
	color: #606266;
}
</style>
