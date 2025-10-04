<template>
    <div class="sample-storage">
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
            class="sample-storage-table"
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
            <el-table-column prop="survey_item" label="调查项目" width="200" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.survey_item" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.survey_item }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="task_undertaking_unit" label="任务承担单位" width="180" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.task_undertaking_unit" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.task_undertaking_unit }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="stored_samples" label="储存样品" min-width="200">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-input v-model="row.stored_samples" type="textarea" :rows="2" size="small" @click.stop></el-input>
                    </template>
                    <span v-else>{{ row.stored_samples }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="record_time" label="记录时间" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-date-picker
                            v-model="row.record_time"
                            type="date"
                            placeholder="选择日期"
                            size="small"
                            value-format="YYYY-MM-DD"
                            @click.stop
                        ></el-date-picker>
                    </template>
                    <span v-else>{{ row.record_time }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="spot_check_time" label="抽查时间" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-date-picker
                            v-model="row.spot_check_time"
                            type="date"
                            placeholder="选择日期"
                            size="small"
                            value-format="YYYY-MM-DD"
                            @click.stop
                        ></el-date-picker>
                    </template>
                    <span v-else>{{ row.spot_check_time }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="qualified_or_not" label="合格与否" width="120" align="center">
                <template #default="{ row }">
                    <template v-if="row.isEditing">
                        <el-select v-model="row.qualified_or_not" size="small" @click.stop>
                            <el-option label="合格" value="合格"></el-option>
                            <el-option label="不合格" value="不合格"></el-option>
                        </el-select>
                    </template>
                    <span v-else>{{ row.qualified_or_not }}</span>
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
        <div class="pagination">
            <el-pagination
                v-model:current-page="page"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
        </div>

        <!-- 附件查看对话框 -->
        <el-dialog
            v-model="attachmentDialogVisible"
            title="附件列表"
            width="600px"
        >
            <div v-if="currentAttachments && currentAttachments.length > 0">
                <div v-for="(attachment, index) in currentAttachments" :key="index" class="attachment-item-dialog">
                    <div class="attachment-info">
                        <span class="attachment-name">{{ index + 1 }}. {{ attachment.filename }}</span>
                        <span class="attachment-size" v-if="attachment.size">({{ formatFileSize(attachment.size) }})</span>
                    </div>
                    <el-button type="primary" size="small" @click="downloadAttachment(attachment)">
                        下载
                    </el-button>
                </div>
            </div>
            <div v-else class="no-attachments">
                暂无附件
            </div>
            <template #footer>
                <el-button @click="attachmentDialogVisible = false">关闭</el-button>
            </template>
        </el-dialog>

        <!-- 新增对话框 -->
        <el-dialog
            v-model="dialogVisible"
            :title="dialogTitle"
            width="900px"
            @close="handleDialogClose"
        >
            <el-form :model="formData" :rules="formRules" ref="formRef" label-width="150px">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="航次任务名称" prop="task_name">
                            <el-input v-model="formData.task_name" placeholder="请输入航次任务名称" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="调查项目" prop="survey_item">
                            <el-input v-model="formData.survey_item" placeholder="请输入调查项目" />
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="任务承担单位" prop="task_undertaking_unit">
                            <el-input v-model="formData.task_undertaking_unit" placeholder="请输入任务承担单位" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="记录时间" prop="record_time">
                            <el-date-picker
                                v-model="formData.record_time"
                                type="date"
                                placeholder="选择记录时间"
                                format="YYYY-MM-DD"
                                value-format="YYYY-MM-DD"
                                style="width: 100%;"
                            />
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="抽查时间" prop="spot_check_time">
                            <el-date-picker
                                v-model="formData.spot_check_time"
                                type="date"
                                placeholder="选择抽查时间"
                                format="YYYY-MM-DD"
                                value-format="YYYY-MM-DD"
                                style="width: 100%;"
                            />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="合格与否" prop="qualified_or_not">
                            <el-select v-model="formData.qualified_or_not" placeholder="请选择" style="width: 100%;">
                                <el-option label="合格" value="合格"></el-option>
                                <el-option label="不合格" value="不合格"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-form-item label="储存样品" prop="stored_samples">
                    <el-input
                        v-model="formData.stored_samples"
                        type="textarea"
                        :rows="4"
                        placeholder="请输入储存样品信息"
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
                
                <!-- 附件上传 -->
                <el-form-item label="附件上传">
                    <div class="dialog-upload">
                        <el-upload
                            :auto-upload="false"
                            :on-change="handleDialogAttachmentUpload"
                            :before-upload="beforeUpload"
                            :show-file-list="false"
                            accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif"
                        >
                            <el-button type="primary" size="small">
                                <el-icon><Upload /></el-icon>
                                选择文件
                            </el-button>
                        </el-upload>
                        <div v-if="formData.attachmentList && formData.attachmentList.length > 0" class="attachment-list">
                            <div v-for="(attachment, index) in formData.attachmentList" :key="index" class="attachment-item">
                                <span>{{ attachment.filename }}</span>
                                <el-button type="danger" size="small" @click="handleDialogAttachmentRemove(index)">
                                    删除
                                </el-button>
                            </div>
                        </div>
                    </div>
                </el-form-item>
            </el-form>
            
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="handleDialogClose">取消</el-button>
                    <el-button type="primary" @click="handleDialogSubmit" :loading="submitLoading">
                        确定
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, Upload, Download, Document, Edit, Check, Close } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx'
import {
  fetchSampleStorageList,
  createSampleStorage,
  updateSampleStorage,
  deleteSampleStorage,
  batchDeleteSampleStorage,
  uploadSampleStorageAttachment
} from '@/api/sample-storage'

// 接收任务名称属性
const props = defineProps<{
  taskName: string
}>()

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const selectedRows = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框相关
const dialogVisible = ref(false)
const dialogTitle = ref('新增外业调查样品储存记录抽查表')
const submitLoading = ref(false)
const formRef = ref()

// 附件对话框相关
const attachmentDialogVisible = ref(false)
const currentAttachments = ref([])

// 表单数据
const formData = reactive({
  id: null,
  task_name: '',
  survey_item: '',
  task_undertaking_unit: '',
  stored_samples: '',
  record_time: '',
  spot_check_time: '',
  qualified_or_not: '',
  remarks: '',
  attachmentList: []
})

// 表单验证规则
const formRules = {
  task_name: [
    { required: true, message: '请输入航次任务名称', trigger: 'blur' }
  ],
  survey_item: [
    { required: true, message: '请输入调查项目', trigger: 'blur' }
  ],
  task_undertaking_unit: [
    { required: true, message: '请输入任务承担单位', trigger: 'blur' }
  ]
}

// 表格引用
const tableRef = ref()
const uploadRef = ref()

// 方法
const loadData = async () => {
  try {
    loading.value = true
    const params: any = {
      page: page.value,
      pageSize: pageSize.value,
      task_name: props.taskName  // 强制按当前任务名称过滤
    }
    
    const res = await fetchSampleStorageList(params)
    if (res.code === 200) {
      // 为每行数据添加编辑状态
      tableData.value = (res.data || []).map((item: any) => ({
        ...item,
        isEditing: false,
        attachmentList: item.attachments || []
      }))
      total.value = res.data?.length || 0
    } else {
      ElMessage.error(res.msg || '获取数据失败')
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const handleAddRow = () => {
  dialogTitle.value = '新增外业调查样品储存记录抽查表'
  dialogVisible.value = true
  // 重置表单数据，默认填入当前任务名称
  Object.assign(formData, {
    id: null,
    task_name: props.taskName || '',
    survey_item: '',
    task_undertaking_unit: '',
    stored_samples: '',
    record_time: '',
    spot_check_time: '',
    qualified_or_not: '',
    remarks: '',
    attachmentList: []
  })
}

const handleEdit = (row: any) => {
  row.isEditing = true
  row.attachmentList = row.attachments || []
}

const handleSave = async (row: any) => {
  try {
    const data = {
      task_name: row.task_name,
      survey_item: row.survey_item,
      task_undertaking_unit: row.task_undertaking_unit,
      stored_samples: row.stored_samples,
      record_time: row.record_time,
      spot_check_time: row.spot_check_time,
      qualified_or_not: row.qualified_or_not,
      remarks: row.remarks,
      attachmentList: row.attachmentList
    }
    
    let res
    if (row.id) {
      res = await updateSampleStorage(row.id, data)
    } else {
      res = await createSampleStorage(data)
    }
    
    if (res.code === 200) {
      ElMessage.success(row.id ? '更新成功' : '创建成功')
      row.isEditing = false
      row.attachments = row.attachmentList
      if (!row.id) {
        row.id = res.data.id
      }
    } else {
      ElMessage.error(res.msg || (row.id ? '更新失败' : '创建失败'))
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

const handleCancel = (row: any) => {
  if (row.id) {
    // 如果是编辑现有记录，恢复原始数据
    row.isEditing = false
    loadData()
  } else {
    // 如果是新增记录，删除该行
    const index = tableData.value.indexOf(row)
    if (index > -1) {
      tableData.value.splice(index, 1)
    }
  }
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条外业调查样品储存记录抽查表记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    if (row.id) {
      const res = await deleteSampleStorage(row.id)
      if (res.code === 200) {
        ElMessage.success('删除成功')
        loadData()
      } else {
        ElMessage.error(res.msg || '删除失败')
      }
    } else {
      // 如果是新增的记录，直接从表格中移除
      const index = tableData.value.indexOf(row)
      if (index > -1) {
        tableData.value.splice(index, 1)
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleDeleteBatch = async () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的记录')
    return
  }
  
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 条记录吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const ids = selectedRows.value.filter((row: any) => row.id).map((row: any) => row.id)
    if (ids.length > 0) {
      const res = await batchDeleteSampleStorage(ids)
      if (res.code === 200) {
        ElMessage.success('批量删除成功')
        loadData()
      } else {
        ElMessage.error(res.msg || '批量删除失败')
      }
    }
    
    // 删除没有ID的新增记录
    const newRows = selectedRows.value.filter((row: any) => !row.id)
    newRows.forEach((row: any) => {
      const index = tableData.value.indexOf(row)
      if (index > -1) {
        tableData.value.splice(index, 1)
      }
    })
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedRows.value = selection
}

const handleRowClick = (row: any) => {
  // 点击行时的处理逻辑
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  page.value = 1
  loadData()
}

const handleCurrentChange = (pageNum: number) => {
  page.value = pageNum
  loadData()
}

const handleViewAttachment = (row: any) => {
  if (row.attachmentList && row.attachmentList.length > 0) {
    // 显示附件列表对话框
    currentAttachments.value = row.attachmentList
    attachmentDialogVisible.value = true
  } else {
    ElMessage.info('暂无附件')
  }
}

const downloadAttachment = (attachment: any) => {
  if (attachment.url) {
    window.open(attachment.url, '_blank')
  }
}

const formatFileSize = (size: number) => {
  if (size < 1024) {
    return size + ' B'
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(1) + ' KB'
  } else {
    return (size / (1024 * 1024)).toFixed(1) + ' MB'
  }
}

const handleAttachmentUpload = async (params: any, row: any) => {
  try {
    const formData = new FormData()
    formData.append('file', params.file)
    
    const response = await uploadSampleStorageAttachment(formData)
    if (response.code === 200) {
      if (!row.attachmentList) {
        row.attachmentList = []
      }
      row.attachmentList.push({
        filename: response.data.filename,
        url: response.data.url,
        size: response.data.size
      })
      ElMessage.success('附件上传成功')
    } else {
      ElMessage.error(response.msg || '附件上传失败')
    }
  } catch (error) {
    console.error('附件上传失败:', error)
    ElMessage.error('附件上传失败')
  }
}

const handleDialogClose = () => {
  dialogVisible.value = false
  formRef.value?.resetFields()
}

const handleDialogSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitLoading.value = true
    
    const data = {
      task_name: formData.task_name,
      survey_item: formData.survey_item,
      task_undertaking_unit: formData.task_undertaking_unit,
      stored_samples: formData.stored_samples,
      record_time: formData.record_time,
      spot_check_time: formData.spot_check_time,
      qualified_or_not: formData.qualified_or_not,
      remarks: formData.remarks,
      attachmentList: formData.attachmentList
    }
    
    const res = await createSampleStorage(data)
    if (res.code === 200) {
      ElMessage.success('创建成功')
      dialogVisible.value = false
      loadData()
    } else {
      ElMessage.error(res.msg || '创建失败')
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDialogAttachmentUpload = async (file: any) => {
  try {
    const uploadFormData = new FormData()
    uploadFormData.append('file', file.raw)
    
    const response = await uploadSampleStorageAttachment(uploadFormData)
    if (response.code === 200) {
      formData.attachmentList.push({
        filename: response.data.filename,
        url: response.data.url,
        size: response.data.size
      })
      ElMessage.success('附件上传成功')
    } else {
      ElMessage.error(response.msg || '附件上传失败')
    }
  } catch (error) {
    console.error('附件上传失败:', error)
    ElMessage.error('附件上传失败')
  }
}

const handleDialogAttachmentRemove = (index: number) => {
  formData.attachmentList.splice(index, 1)
}

const beforeUpload = (file: File) => {
  const isValidType = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'image/jpeg', 'image/jpg', 'image/png', 'image/gif'].includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isValidType) {
    ElMessage.error('只能上传 PDF、Word、Excel、图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB!')
    return false
  }
  return true
}

const handleSaveAll = () => {
  ElMessage.info('保存功能待实现')
}

const handleExport = () => {
  try {
    const exportData = tableData.value.map(item => ({
      '航次任务名称': item.task_name,
      '调查项目': item.survey_item,
      '任务承担单位': item.task_undertaking_unit,
      '储存样品': item.stored_samples,
      '记录时间': item.record_time,
      '抽查时间': item.spot_check_time,
      '合格与否': item.qualified_or_not,
      '备注': item.remarks,
      '附件': item.attachmentList && item.attachmentList.length > 0 ? 
        item.attachmentList.map(att => att.filename).join('; ') : '无附件'
    }))

    const worksheet = XLSX.utils.json_to_sheet(exportData)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, '外业调查样品储存记录抽查表')
    XLSX.writeFile(workbook, `外业调查样品储存记录抽查表_${props.taskName}.xlsx`)

    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

const handleImport = () => {
  ElMessage.info('导入功能待实现')
}

// 监听任务名称变化，自动重新加载数据
watch(() => props.taskName, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal) {
    console.log(`任务名称从 ${oldVal} 变更为 ${newVal}，重新加载数据`)
    loadData()
  }
}, { immediate: true }) // immediate: true 确保组件挂载时也执行一次

// 生命周期
onMounted(() => {
  // loadData() 已由 watch 的 immediate: true 处理
})
</script>

<style scoped>
.sample-storage {
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

.sample-storage-table {
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

.pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
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

/* 附件对话框样式 */
.attachment-item-dialog {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    margin-bottom: 10px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    background: #f9f9f9;
}

.attachment-info {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.attachment-name {
    font-weight: 500;
    color: #303133;
    margin-bottom: 4px;
}

.attachment-size {
    font-size: 12px;
    color: #909399;
}

.no-attachments {
    text-align: center;
    color: #909399;
    padding: 20px;
}
</style>
