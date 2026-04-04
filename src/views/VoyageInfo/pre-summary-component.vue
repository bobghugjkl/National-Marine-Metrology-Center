<template>
    <div>
        <div class="container">
            <div class="header">
                <h2 class="title">航前质量监督情况汇总表</h2>
                <div class="task-info">
                    <span class="label">任务名称：</span>
                    <span class="value">{{ formData.task_name }}</span>
                </div>
            </div>

            <el-form :model="formData" label-width="180px" class="summary-form">
                <!-- 基本信息 -->
                <el-divider content-position="left"><h3>基本信息</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="航次承担单位">
                            <el-input v-model="formData.undertaking_unit" placeholder="请输入航次承担单位"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="航次参与单位">
                            <el-input v-model="formData.participating_unit" placeholder="请输入航次参与单位"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="航次任务名称">
                            <el-input v-model="formData.task_name" placeholder="请输入航次任务名称" disabled></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="航次任务编号">
                            <el-input v-model="formData.task_code" placeholder="请输入航次任务编号"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="调查船">
                            <el-input v-model="formData.survey_vessel" placeholder="请输入调查船"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="任务负责人">
                            <el-input v-model="formData.task_leader" placeholder="请输入任务负责人"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="监督检查人员">
                            <el-input v-model="formData.supervision_personnel" placeholder="请输入监督检查人员"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="受检查单位主要参与人员">
                            <el-input v-model="formData.main_participants" placeholder="请输入受检查单位主要参与人员"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="检查日期">
                            <el-date-picker
                                v-model="formData.inspection_date"
                                type="date"
                                placeholder="选择检查日期"
                                format="YYYY-MM-DD"
                                value-format="YYYY-MM-DD"
                                style="width: 100%;"
                            />
                        </el-form-item>
                    </el-col>
                </el-row>

                <!-- 检查情况 -->
                <el-divider content-position="left"><h3>检查情况</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="24">
                        <el-form-item label="检查情况">
                            <el-input 
                                v-model="formData.inspection_details" 
                                type="textarea" 
                                :rows="6"
                                placeholder="请详细描述检查情况，包括检查项目、检查过程、发现的问题等">
                            </el-input>
                        </el-form-item>
                    </el-col>
                </el-row>

                <!-- 检查结果 -->
                <el-divider content-position="left"><h3>检查结果</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="24">
                        <el-form-item label="检查结果">
                            <el-input 
                                v-model="formData.inspection_results" 
                                type="textarea" 
                                :rows="6"
                                placeholder="请详细描述检查结果，包括合格项目、不合格项目、整改建议等">
                            </el-input>
                        </el-form-item>
                    </el-col>
                </el-row>

                <!-- 相关资料 -->
                <el-divider content-position="left"><h3>相关资料</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="24">
                        <el-form-item label="相关资料">
                            <div class="attachment-section">
                                <el-upload
                                    :auto-upload="false"
                                    :on-change="handleAttachmentUpload"
                                    :before-upload="beforeUpload"
                                    :show-file-list="false"
                                    accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif"
                                    class="upload-area"
                                >
                                    <el-button type="primary" size="small">
                                        <el-icon><Upload /></el-icon>
                                        选择文件
                                    </el-button>
                                </el-upload>
                                <div v-if="formData.relatedMaterialsList && formData.relatedMaterialsList.length > 0" class="attachment-list">
                                    <div v-for="(attachment, index) in formData.relatedMaterialsList" :key="index" class="attachment-item">
                                        <span class="attachment-name">{{ attachment.filename }}</span>
                                        <div class="attachment-actions">
                                            <el-button type="primary" size="small" @click="downloadAttachment(attachment)">
                                                下载
                                            </el-button>
                                            <el-button type="danger" size="small" @click="removeAttachment(index)">
                                                删除
                                            </el-button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </el-form-item>
                    </el-col>
                </el-row>

                <!-- 操作按钮 -->
                <el-divider content-position="left"><h3>操作</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="24" class="button-group">
                        <el-button type="primary" @click="handleSave" :loading="saveLoading">
                            <el-icon><Check /></el-icon>
                            保存
                        </el-button>
                        <el-button @click="handleReset">
                            <el-icon><Refresh /></el-icon>
                            重置
                        </el-button>
                        <el-button type="success" @click="handleExport">
                            <el-icon><Download /></el-icon>
                            导出
                        </el-button>
                    </el-col>
                </el-row>
            </el-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Upload, Check, Refresh, Download } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx'
import {
  fetchPreSummaryList,
  createPreSummary,
  updatePreSummary,
  uploadPreSummaryAttachment
} from '@/api/pre-summary'

// 接收任务名称属性
const props = defineProps<{
  taskName: string
}>()

// 响应式数据
const saveLoading = ref(false)

// 表单数据
const formData = reactive({
  id: null,
  task_name: '',
  undertaking_unit: '',
  participating_unit: '',
  task_code: '',
  survey_vessel: '',
  task_leader: '',
  supervision_personnel: '',
  main_participants: '',
  inspection_date: '',
  inspection_details: '',
  inspection_results: '',
  relatedMaterialsList: []
})

// 方法
const loadData = async () => {
  try {
    const params: any = {
      task_name: props.taskName  // 强制按当前任务名称过滤
    }
    
    const res = await fetchPreSummaryList(params)
    if (res.code === 200 && res.data && res.data.length > 0) {
      // 如果已有数据，加载第一条记录
      const record = res.data[0]
      Object.assign(formData, {
        id: record.id,
        task_name: record.task_name,
        undertaking_unit: record.undertaking_unit || '',
        participating_unit: record.participating_unit || '',
        task_code: record.task_code || '',
        survey_vessel: record.survey_vessel || '',
        task_leader: record.task_leader || '',
        supervision_personnel: record.supervision_personnel || '',
        main_participants: record.main_participants || '',
        inspection_date: record.inspection_date || '',
        inspection_details: record.inspection_details || '',
        inspection_results: record.inspection_results || '',
        relatedMaterialsList: record.related_materials || []
      })
    } else {
      // 如果没有数据，初始化表单
      formData.task_name = props.taskName || ''
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
}

const handleSave = async () => {
  try {
    saveLoading.value = true
    
    const data = {
      task_name: formData.task_name,
      undertaking_unit: formData.undertaking_unit,
      participating_unit: formData.participating_unit,
      task_code: formData.task_code,
      survey_vessel: formData.survey_vessel,
      task_leader: formData.task_leader,
      supervision_personnel: formData.supervision_personnel,
      main_participants: formData.main_participants,
      inspection_date: formData.inspection_date,
      inspection_details: formData.inspection_details,
      inspection_results: formData.inspection_results,
      relatedMaterialsList: formData.relatedMaterialsList
    }
    
    let res
    if (formData.id) {
      res = await updatePreSummary(formData.id, data)
    } else {
      res = await createPreSummary(data)
    }
    
    if (res.code === 200) {
      ElMessage.success(formData.id ? '更新成功' : '创建成功')
      if (!formData.id) {
        formData.id = res.data.id
      }
    } else {
      ElMessage.error(res.msg || (formData.id ? '更新失败' : '创建失败'))
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saveLoading.value = false
  }
}

const handleReset = () => {
  ElMessageBox.confirm('确定要重置表单吗？所有未保存的数据将丢失。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    Object.assign(formData, {
      id: null,
      task_name: props.taskName || '',
      undertaking_unit: '',
      participating_unit: '',
      task_code: '',
      survey_vessel: '',
      task_leader: '',
      supervision_personnel: '',
      main_participants: '',
      inspection_date: '',
      inspection_details: '',
      inspection_results: '',
      relatedMaterialsList: []
    })
    ElMessage.success('表单已重置')
  }).catch(() => {
    // 用户取消
  })
}

const handleExport = () => {
  try {
    const exportData = [{
      '航次承担单位': formData.undertaking_unit,
      '航次参与单位': formData.participating_unit,
      '航次任务名称': formData.task_name,
      '航次任务编号': formData.task_code,
      '调查船': formData.survey_vessel,
      '任务负责人': formData.task_leader,
      '监督检查人员': formData.supervision_personnel,
      '受检查单位主要参与人员': formData.main_participants,
      '检查日期': formData.inspection_date,
      '检查情况': formData.inspection_details,
      '检查结果': formData.inspection_results,
      '相关资料': formData.relatedMaterialsList && formData.relatedMaterialsList.length > 0 ? 
        formData.relatedMaterialsList.map(att => att.filename).join('; ') : '无'
    }]

    const worksheet = XLSX.utils.json_to_sheet(exportData)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, '航前质量监督情况汇总表')
    XLSX.writeFile(workbook, `航前质量监督情况汇总表_${props.taskName}.xlsx`)

    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

const handleAttachmentUpload = async (file: any) => {
  try {
    const uploadFormData = new FormData()
    uploadFormData.append('file', file.raw)
    
    const response = await uploadPreSummaryAttachment(uploadFormData)
    if (response.code === 200) {
      formData.relatedMaterialsList.push({
        filename: response.data.filename,
        url: response.data.url,
        size: response.data.size
      })
      ElMessage.success('文件上传成功')
    } else {
      ElMessage.error(response.msg || '文件上传失败')
    }
  } catch (error) {
    console.error('文件上传失败:', error)
    ElMessage.error('文件上传失败')
  }
}

const downloadAttachment = (attachment: any) => {
  if (attachment.url) {
    window.open(attachment.url, '_blank')
  }
}

const removeAttachment = (index: number) => {
  ElMessageBox.confirm('确定要删除这个文件吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    formData.relatedMaterialsList.splice(index, 1)
    ElMessage.success('文件已删除')
  }).catch(() => {
    // 用户取消
  })
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
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #e4e7ed;
}

.title {
    color: #303133;
    font-size: 24px;
    font-weight: 600;
    margin: 0;
}

.task-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.label {
    color: #606266;
    font-weight: 500;
}

.value {
    color: #409eff;
    font-weight: 600;
    font-size: 16px;
}

.summary-form {
    background: #fff;
}

:deep(.el-divider__text) {
    background: #fff;
    color: #409eff;
    font-weight: 600;
    font-size: 16px;
}

:deep(.el-form-item__label) {
    color: #606266;
    font-weight: 500;
}

:deep(.el-input__inner) {
    border-radius: 6px;
}

:deep(.el-textarea__inner) {
    border-radius: 6px;
}

:deep(.el-date-editor) {
    width: 100%;
}

.attachment-section {
    width: 100%;
}

.upload-area {
    margin-bottom: 15px;
}

.attachment-list {
    margin-top: 10px;
}

.attachment-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    background: #f5f7fa;
    border-radius: 6px;
    margin-bottom: 8px;
    border: 1px solid #e4e7ed;
}

.attachment-name {
    color: #303133;
    font-weight: 500;
    flex: 1;
}

.attachment-actions {
    display: flex;
    gap: 8px;
}

.button-group {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}

:deep(.el-button) {
    border-radius: 6px;
    font-weight: 500;
}

:deep(.el-button--primary) {
    background: #409eff;
    border-color: #409eff;
}

:deep(.el-button--primary:hover) {
    background: #66b1ff;
    border-color: #66b1ff;
}

:deep(.el-button--success) {
    background: #67c23a;
    border-color: #67c23a;
}

:deep(.el-button--success:hover) {
    background: #85ce61;
    border-color: #85ce61;
}

:deep(.el-card) {
    border-radius: 8px;
    border: 1px solid #e4e7ed;
    margin-bottom: 15px;
}

:deep(.el-card__header) {
    background: #f8f9fa;
    border-bottom: 1px solid #e4e7ed;
}

:deep(.el-card__body) {
    padding: 20px;
}

:deep(.el-row) {
    margin-bottom: 15px;
}

:deep(.el-form-item) {
    margin-bottom: 20px;
}

:deep(.el-textarea__inner) {
    resize: vertical;
}

:deep(.el-upload) {
    display: inline-block;
}

:deep(.el-upload .el-button) {
    border-radius: 6px;
}
</style>
