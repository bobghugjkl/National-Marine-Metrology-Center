<template>
  <div style="padding: 20px;">
    <h2 align="center">仪器设备（工作计量器具）一览表</h2>

    <!-- 操作按钮 -->

    <div class="header-buttons">
				<el-button type="success" :icon="Download" @click="downloadTemplate">
					下载excel模板
				</el-button>
				<el-button type="primary" :icon="Upload" @click="importExcel">
					导入excel文件
				</el-button>
				<el-button type="warning"  @click="addRow">
					新增
				</el-button>
        <el-button type="warning" :icon="Delete" @click="deleteSelectedRows">批量删除</el-button>
			</div>
   

    <!-- 表格 -->
    <el-table
      :data="tableData"
      border
      style="width: 100%"
      @selection-change="handleSelectionChange"
      row-key="id"
    >
      <el-table-column type="selection" width="55"></el-table-column>

      <!-- 航次任务名称 -->
      <el-table-column label="航次任务名称" width="150">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.missionName" size="mini" />
          </template>
          <span v-else>{{ row.missionName }}</span>
        </template>
      </el-table-column>

      <!-- 类别 -->
      <el-table-column label="类别" width="100">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.category" size="mini" />
          </template>
          <span v-else>{{ row.category }}</span>
        </template>
      </el-table-column>

      <!-- 仪器名称 -->
      <el-table-column label="仪器（标准物质）名称" width="180">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.instrumentName" size="mini" />
          </template>
          <span v-else>{{ row.instrumentName }}</span>
        </template>
      </el-table-column>

      <!-- 编号 -->
      <el-table-column label="编号" width="100">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.number" size="mini" />
          </template>
          <span v-else>{{ row.number }}</span>
        </template>
      </el-table-column>

      <!-- 型号 -->
      <el-table-column label="型号" width="100">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.model" size="mini" />
          </template>
          <span v-else>{{ row.model }}</span>
        </template>
      </el-table-column>

      <!-- 量值溯源方式 -->
      <el-table-column label="量值溯源方式" width="120">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.traceability" size="mini" />
          </template>
          <span v-else>{{ row.traceability }}</span>
        </template>
      </el-table-column>

      <!-- 检定/校准日期 -->
      <el-table-column label="检定/校准日期" width="120">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-date-picker
              v-model="row.calibrationDate"
              type="date"
              size="mini"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              placeholder="选择日期"
            />
          </template>
          <span v-else>{{ row.calibrationDate }}</span>
        </template>
      </el-table-column>

      <!-- 证书编号 -->
      <el-table-column label="证书编号" width="120">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.certificateNo" size="mini" />
          </template>
          <span v-else>{{ row.certificateNo }}</span>
        </template>
      </el-table-column>

      <!-- 有效期 -->
      <el-table-column label="有效期" width="100">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.validity" size="mini" />
          </template>
          <span v-else>{{ row.validity }}</span>
        </template>
      </el-table-column>

      <!-- 检定/校准机构 -->
      <el-table-column label="检定/校准机构" width="140">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.institution" size="mini" />
          </template>
          <span v-else>{{ row.institution }}</span>
        </template>
      </el-table-column>

      <!-- 备注 -->
      <el-table-column label="备注" width="150">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-input v-model="row.remark" size="mini" />
          </template>
          <span v-else>{{ row.remark }}</span>
        </template>
      </el-table-column>

      <!-- 附件 -->
      <el-table-column label="附件" width="120">
        <template #default="{ row }">
          <template v-if="row.isEditing">
            <el-upload
              :action="uploadUrl"
              :auto-upload="true"
              :file-list="row.fileList"
              :on-success="(res, file) => handleFileSuccess(res, file, row)"
              :on-remove="(file) => handleFileRemove(file, row)"
              :limit="1"
              list-type="text"
              size="mini"
              style="margin-top: 5px;"
            >
              <el-button size="mini">上传</el-button>
            </el-upload>
          </template>
          <div v-else>
            <el-tag
              v-for="file in row.fileList"
              :key="file.uid"
              size="small"
              @click="downloadFile(file)"
              style="cursor: pointer;"
            >
              {{ file.name }}
            </el-tag>
            <span v-if="row.fileList.length === 0">—</span>
          </div>
        </template>
      </el-table-column>

      <!-- 操作列 -->
      <el-table-column label="操作"  fixed="right" width="120">
        <template #default="{ row }">
           <div class="operator-buttons">
          <el-button
            v-if="!row.isEditing"
            type="primary"
            size="small"
            :icon="Edit"
            @click.stop="startEdit(row)"
          >
            
          </el-button>
          <el-button
            v-else
            type="primary"
            size="small"
            :icon="Checked"
            @click.stop="saveRow(row)"
          >
           
          </el-button>

          <el-button
            type="danger"
            size="small"
            :icon="Delete"
            
            @click.stop="deleteRow(row)"
          >
           
          </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 导入对话框 -->
    <el-dialog title="导入Excel" :visible.sync="dialogImportVisible">
      <el-upload
        ref="upload"
        action="/api/import"
        :auto-upload="false"
        :on-change="handleChange"
        :on-success="handleSuccess"
        accept=".xlsx,.xls"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或点击上传</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogImportVisible = false">取消</el-button>
        <el-button type="primary" @click="submitUpload">确认导入</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Delete, Edit, View, Refresh ,Checked, Download, Upload} from '@element-plus/icons-vue';

import XLSX from 'xlsx';
import axios from 'axios'

// 响应式数据
const tableData = ref([])
const selectedRows = ref([])
const dialogImportVisible = ref(false)
const uploadUrl = '/api/upload' // 后端上传接口

// 生命周期钩子：组件挂载后加载数据
onMounted(() => {
  loadTableData()
})

// 加载表格数据
const loadTableData = async () => {
  try {
    const res = await axios.get('/api/equipment')
    tableData.value = res.data.map(row => ({
      ...row,
      id: row.id || Date.now() + Math.random(),
      isEditing: false,
      fileList: row.fileList || []
    }))
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('数据加载失败')
  }
}

// 开始编辑
const startEdit = (row) => {
  row.isEditing = true
}

// 保存单行
const saveRow = async (row) => {
  try {
    const payload = { ...row, isEditing: false, fileList: undefined }
    //await axios.post('/api/equipment/save', payload)
    row.isEditing = false
    ElMessage.success('保存成功！')
  } catch (error) {
    ElMessage.error('保存失败：' + (error.response?.data?.message || error.message))
  }
}

// 新增行
const addRow = () => {
  const newRow = {
    id: Date.now(),
    missionName: '',
    category: '',
    instrumentName: '',
    number: '',
    model: '',
    traceability: '',
    calibrationDate: '',
    certificateNo: '',
    validity: '',
    institution: '',
    remark: '',
    fileList: [],
    isEditing: true
  }
  tableData.value.push(newRow)
}

// 删除选中行（批量）
const deleteSelectedRows = () => {
  tableData.value = tableData.value.filter(row => !selectedRows.value.includes(row))
}

// 删除单行
const deleteRow = (row) => {
  ElMessageBox.confirm('确定删除该行吗？', '提示', {
    type: 'warning'
  }).then(() => {
    tableData.value = tableData.value.filter(r => r.id !== row.id)
    ElMessage.success('删除成功！')
  }).catch(() => {})
}

// 文件上传成功
const handleFileSuccess = (res, file, row) => {
  if (!row.fileList) row.fileList = []
  file.url = res?.url || '#'
  ElMessage.success('上传成功')
}

// 文件移除
const handleFileRemove = (file, row) => {
  row.fileList = row.fileList.filter(f => f.uid !== file.uid)
}

// 下载文件
const downloadFile = (file) => {
  window.open(file.url || '#', '_blank')
}

// 下载模板
const downloadTemplate = () => {
  const worksheet = XLSX.utils.json_to_sheet([
        {
          "航次任务名称": "",
          "姓名": "",
          "性别": "",
          "出生年月": "",
          "职称": "",
          "工作单位": "",
          "从事专业": "",
          "本航次操作仪器": "",
          "培训情况": "",
          "备注": "",
          "附件": ""
        }
      ]);
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, "资质表");
      XLSX.writeFile(workbook, "外业调查人员资质模板.xlsx");
}

// 导入Excel
const importExcel = () => {
  dialogImportVisible.value = true
}

// 上传组件 change 事件
const handleChange = (file, fileList) => {
  // 清除文件列表（单文件上传）
  uploadRef.value.clearFiles()
  uploadRef.value.handleEmit('change', file, fileList)
}

// 上传成功回调
const handleSuccess = (response, file, fileList) => {
  ElMessage.success('导入成功！')
  dialogImportVisible.value = false
  loadTableData()
}

// 提交上传
const submitUpload = () => {
  uploadRef.value.submit()
}

// 表格选择变化
const handleSelectionChange = (val) => {
  selectedRows.value = val
}

// 为 el-upload 添加 ref
const uploadRef = ref()
</script>

<style scoped>
.el-table th {
  background-color: #fffacd;
}
.el-tag {
  margin-right: 5px;
}
.operator-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2px;
    flex-wrap: nowrap;
}
</style>