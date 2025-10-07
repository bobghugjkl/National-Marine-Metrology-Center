<template>
    <div class="task-detail">
        <!-- 左侧导航栏 -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h3>{{ taskName }}</h3>
                <p>任务详情</p>
            </div>
            <el-menu
                :default-active="activeMenu"
                class="sidebar-menu"
                @select="handleMenuSelect"
                :collapse="false"
            >
                <!-- 航前检查 -->
                <el-menu-item index="pre-voyage" class="parent-menu">
                    <el-icon><DocumentChecked /></el-icon>
                    <span>航前检查</span>
                </el-menu-item>
                <el-menu-item index="pre-voyage-record" class="submenu-item">航前质量监督检查记录</el-menu-item>
                <el-menu-item index="pre-voyage-summary" class="submenu-item">航前质量监督情况汇总</el-menu-item>
                <el-menu-item index="personnel-list" class="submenu-item">外业调查人员资质一览</el-menu-item>
                <el-menu-item index="equipment-list" class="submenu-item">仪器设备(工作计量器具)一览</el-menu-item>
                <el-menu-item index="investigation-projects" class="submenu-item">外业调查项目/仪器比测统计</el-menu-item>

                <!-- 航中检查 -->
                <el-menu-item index="during-voyage" class="parent-menu">
                    <el-icon><Ship /></el-icon>
                    <span>航中检查</span>
                </el-menu-item>
                <el-menu-item index="during-personnel" class="submenu-item">外业调查人员资质一览</el-menu-item>
                <el-menu-item index="during-equipment" class="submenu-item">仪器设备(工作计量器具)一览</el-menu-item>
                <el-menu-item index="during-investigation" class="submenu-item">外业调查项目/仪器比测统计</el-menu-item>
                <el-menu-item index="supervisor-log" class="submenu-item">监督员日志</el-menu-item>
                <el-menu-item index="original-records" class="submenu-item">外业调查原始记录抽查</el-menu-item>
                <el-menu-item index="procedure-execution" class="submenu-item">外业调查操作规程执行统计</el-menu-item>
                <el-menu-item index="work-log" class="submenu-item">外业调查工作日志抽查</el-menu-item>
                <el-menu-item index="sample-storage" class="submenu-item">外业调查样品储存记录抽查</el-menu-item>
                <el-menu-item index="ship-quality" class="submenu-item">随船质量监督检查</el-menu-item>

                <!-- 航后检查表 -->
                <el-menu-item index="post-voyage" class="parent-menu">
                    <el-icon><DocumentCopy /></el-icon>
                    <span>航后检查</span>
                </el-menu-item>
                <el-menu-item index="post-voyage-record" class="submenu-item">航后检查记录</el-menu-item>

                <!-- 导入导出 -->
                <el-menu-item index="import-export" class="parent-menu">
                    <el-icon><Upload /></el-icon>
                    <span>导入导出</span>
                </el-menu-item>
                <el-menu-item index="export-data" class="submenu-item">导出数据包</el-menu-item>
                <el-menu-item index="import-data" class="submenu-item">导入数据包</el-menu-item>
            </el-menu>
        </div>

        <!-- 右侧内容区域 -->
        <div class="main-content">
            <div class="content-header">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item>任务管理</el-breadcrumb-item>
                    <el-breadcrumb-item>{{ taskName }}</el-breadcrumb-item>
                </el-breadcrumb>
                <el-button type="primary" @click="goBack">返回任务列表</el-button>
            </div>

            <div class="content-body">
                <!-- 根据当前菜单显示不同内容 -->
                <div v-if="activeMenu === 'pre-voyage'" class="content-section">
                    <h2>航前检查</h2>
                    <p>这是航前检查模块的总览，目前包含航前质量监督检查记录表、航前质量监督情况汇总表、外业调查人员资质一览表等。</p>
                    <el-empty description="请选择具体的航前检查项目" />
                </div>

                <div v-else-if="activeMenu === 'pre-voyage-record'" class="content-section">
                    <inspection-record-component 
                        :taskName="taskName" 
                        @save-success="handleSaveSuccess" 
                        @cancel="handleCancel" 
                    />
                </div>

                <div v-else-if="activeMenu === 'pre-voyage-summary'" class="content-section">
                    <pre-summary-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'personnel-list'" class="content-section">
                    <personnel-qualifications-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'equipment-list'" class="content-section">
                    <equipment-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'investigation-projects'" class="content-section">
                    <investigation-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'during-personnel'" class="content-section">
                    <voyage-personnel-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'during-equipment'" class="content-section">
                    <voyage-equipment-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'during-investigation'" class="content-section">
                    <voyage-investigation-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'during-voyage'" class="content-section">
                    <h2>航中检查</h2>
                    <p>这是航中检查模块的总览，目前包含外业调查人员资质、仪器设备、工作日志等多个检查项目。</p>
                    <el-empty description="请选择具体的航中检查项目" />
                </div>

                <div v-else-if="activeMenu === 'import-export'" class="content-section">
                    <h2>导入导出</h2>
                    <p>这是导入导出模块的总览，可以导出数据包或导入数据包。</p>
                    <el-empty description="请选择导入或导出功能" />
                </div>

                <div v-else-if="activeMenu.startsWith('during-')" class="content-section">
                    <h2>{{ currentMenuTitle }}</h2>
                    <p>这是航中检查相关表的内容区域，目前为空。</p>
                    <el-empty :description="`暂无${currentMenuTitle}数据`" />
                </div>

                <div v-else-if="activeMenu === 'supervisor-log'" class="content-section">
                    <supervisor-log-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'original-records'" class="content-section">
                    <original-records-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'procedure-execution'" class="content-section">
                    <procedure-execution-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'work-log'" class="content-section">
                    <work-log-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'sample-storage'" class="content-section">
                    <sample-storage-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'ship-quality'" class="content-section">
                    <onboard-inspection-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'post-voyage'" class="content-section">
                   <h2>航后检查</h2>
                    <p>这是航后检查模块的总览，目前包含航后检查记录项目。</p>
                    <el-empty description="请选择具体的航后检查项目" />
                    
                    <!-- <post-inspection-component :taskName="taskName" />//-->
                </div>

                <div v-else-if="activeMenu === 'post-voyage-record'" class="content-section">
                    <post-inspection-component :taskName="taskName" />
                </div>

                <div v-else-if="activeMenu === 'import-export'" class="content-section">
                    <h2>导入导出</h2>
                    <p>这是导入导出模块的总览，可以导出数据包或导入数据包。</p>
                    <el-empty description="请选择导入或导出功能" />
                </div>

                <div v-else-if="activeMenu === 'export-data'" class="content-section">
                    <h2>导出数据包</h2>
                    <p>点击下方按钮导出当前任务的所有表单数据包，包含Excel表格和Word文档。</p>
                    
                    <div class="export-content">
                        <el-card class="export-card">
                            <template #header>
                                <div class="card-header">
                                    <el-icon><Download /></el-icon>
                                    <span>数据包导出</span>
                                </div>
                            </template>
                            
                            <div class="export-info">
                                <p><strong>任务名称：</strong>{{ taskName }}</p>
                                <p><strong>导出内容：</strong></p>
                                <ul class="export-list">
                                    <li>航前检查表单（人员资质、设备、项目统计）</li>
                                    <li>航中检查表单（人员资质、设备、项目统计、监督员日志、原始记录、操作规程、工作日志、样品储存、随船检查）</li>
                                    <li>航后检查表单</li>
                                </ul>
                                <p><strong>文件格式：</strong>Excel表格 + Word文档，打包为ZIP压缩包</p>
                            </div>
                            
                            <div class="export-actions">
                                <el-button 
                                    type="primary" 
                                    size="large"
                                    :loading="exportLoading"
                                    @click="handleExportDataPackage"
                                    :icon="Download"
                                >
                                    {{ exportLoading ? '正在生成数据包...' : '导出数据包' }}
                                </el-button>
                            </div>
                        </el-card>
                    </div>
                </div>

                <div v-else-if="activeMenu === 'import-data'" class="content-section">
                    <h2>导入数据包</h2>
                    <p>这是数据导入功能的内容区域，目前为空。</p>
                    <el-empty description="暂无导入功能" />
                </div>

                <div v-else class="content-section">
                    <h2>{{ currentMenuTitle }}</h2>
                    <p>请选择左侧菜单项查看对应内容</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts" name="task-detail">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import {
    DocumentChecked,
    Ship,
    DocumentCopy,
    User,
    Tools,
    DataBoard,
    TrendCharts,
    Document,
    Edit,
    Upload,
    Download
} from '@element-plus/icons-vue';
import InspectionRecordComponent from './inspection-record-component.vue';
import PersonnelQualificationsComponent from './personnel-qualifications-component.vue';
import EquipmentComponent from './equipment-component.vue';
import InvestigationComponent from './investigation-component.vue';
import VoyagePersonnelComponent from './voyage-personnel-component.vue';
import VoyageEquipmentComponent from './voyage-equipment-component.vue';
import VoyageInvestigationComponent from './voyage-investigation-component.vue';
import SupervisorLogComponent from './supervisor-log-component.vue';
import OriginalRecordsComponent from './original-records-component.vue';
import ProcedureExecutionComponent from './procedure-execution-component.vue';
import WorkLogComponent from './work-log-component.vue';
import SampleStorageComponent from './sample-storage-component.vue';
import PostInspectionComponent from './post-inspection-component.vue';
import PreSummaryComponent from './pre-summary-component.vue';
import OnboardInspectionComponent from './onboard-inspection-component.vue';
import { exportDataPackage } from '@/api/export';

const route = useRoute();
const router = useRouter();

// 获取任务名称
const taskName = computed(() => {
    const name = route.params.task_name as string;
    return name || '未指定任务';
});

// 当前激活的菜单
const activeMenu = ref('pre-voyage');

// 导出相关状态
const exportLoading = ref(false);

// 菜单标题映射
const menuTitles = {
    'pre-voyage': '航前检查',
    'pre-voyage-record': '航前质量监督检查记录表',
    'pre-voyage-summary': '航前质量监督情况汇总表',
    'personnel-list': '外业调查人员资质一览表',
    'equipment-list': '仪器设备(工作计量器具)一览表',
    'investigation-projects': '外业调查项目/仪器比测统计表',
    'during-voyage': '航中检查',
    'during-personnel': '外业调查人员资质一览表(航中)',
    'during-equipment': '仪器设备(工作计量器具)一览表(航中)',
    'during-investigation': '外业调查项目/仪器比测统计表(航中)',
    'supervisor-log': '监督员日志',
    'original-records': '外业调查原始记录抽查表',
    'procedure-execution': '外业调查操作规程执行统计表',
    'work-log': '外业调查工作日志抽查表',
    'sample-storage': '外业调查样品储存记录抽查表',
    'ship-quality': '随船质量监督检查表',
    'post-voyage-record': '航后检查表',
    'import-export': '导入导出',
    'export-data': '导出数据包',
    'import-data': '导入数据包'
};

// 当前菜单标题
const currentMenuTitle = computed(() => menuTitles[activeMenu.value] || '任务详情');

// 菜单选择处理
const handleMenuSelect = (index: string) => {
    // 对于父级菜单，不进行跳转，只更新激活状态
    if (['pre-voyage', 'during-voyage', 'import-export'].includes(index)) {
        activeMenu.value = index;
        return;
    }
    activeMenu.value = index;
};

// 返回任务列表
const goBack = () => {
    router.push({ name: 'task-manage' });
};

// 处理检查记录保存成功
const handleSaveSuccess = () => {
    ElMessage.success('检查记录保存成功');
};

// 处理检查记录取消
const handleCancel = () => {
    // 可以根据需要添加取消操作
};

// 处理人员资质表保存成功
const handlePersonnelSaveSuccess = () => {
    ElMessage.success('人员信息保存成功');
};

// 处理人员资质表取消
const handlePersonnelCancel = () => {
    // 可以根据需要添加取消操作
};

// 处理导出数据包
const handleExportDataPackage = async () => {
    try {
        exportLoading.value = true;
        
        console.log('开始导出数据包，任务名称:', taskName.value);
        
        // 调用导出API
        const response = await exportDataPackage(taskName.value);
        console.log('收到响应:', response);
        
        // 检查响应是否为Blob
        if (response instanceof Blob) {
            // 创建下载链接
            const url = window.URL.createObjectURL(response);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${taskName.value}_数据包_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.zip`;
            
            // 触发下载
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // 清理URL对象
            window.URL.revokeObjectURL(url);
            
            ElMessage.success('数据包导出成功！');
        } else {
            console.error('响应不是Blob类型:', response);
            ElMessage.error('导出数据格式错误');
        }
        
    } catch (error: any) {
        console.error('导出数据包失败:', error);
        ElMessage.error('导出数据包失败，请稍后重试');
    } finally {
        exportLoading.value = false;
    }
};

// 组件挂载时获取任务详情（暂时留空，后续可以添加获取任务详情的逻辑）
onMounted(() => {
    console.log('任务详情页面加载，任务名称:', taskName.value);
    console.log('路由参数:', route.params);

    // 更新页面标题
    document.title = `${taskName.value} - 海洋调查现场质量监督管理系统`;

    // 这里可以添加获取任务详情的API调用
});
</script>

<style scoped>
.task-detail {
    display: flex;
    height: calc(100vh - 84px);
    background-color: #f5f5f5;
}

.sidebar {
    width: 260px;
    background-color: #fff;
    border-right: 1px solid #e4e7ed;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
    padding: 16px 20px;
    border-bottom: 1px solid #e4e7ed;
    background-color: #f8f9fa;
}

.sidebar-header h3 {
    margin: 0 0 6px 0;
    font-size: 16px;
    font-weight: 600;
    color: #409eff;
    overflow-y: scroll;
}

.sidebar-header p {
    margin: 0;
    font-size: 12px;
    color: #909399;
    font-weight: 400;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 220px;
}

.sidebar-menu {
    flex: 1;
    border-right: none;
}

.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    
    min-width: 0;
}

.content-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid #e4e7ed;
    background-color: #f8f9fa;
}

.content-body {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    overflow-x: hidden; /* 防止横向溢出 */
    
}

.content-section {
    min-height: 400px;
         /* 确保容器不超出 */

}

.content-section h2 {
    margin: 0 0 12px 0;
    font-size: 18px;
    font-weight: 600;
    color: #303133;
}

.content-section p {
    margin: 0 0 20px 0;
    font-size: 13px;
    color: #606266;
    line-height: 1.5;
}

/* Element Plus 样式覆盖 */
:deep(.el-menu) {
    border-right: none;
}

:deep(.el-menu-item) {
    height: 40px;
    line-height: 40px;
    margin: 2px 8px;
    border-radius: 4px;
    font-size: 14px;
    padding: 0 16px;
}

:deep(.el-menu-item.parent-menu) {
    height: 48px !important;
    line-height: 48px !important;
    margin: 4px 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    color: #303133 !important;
    background-color: #f8f9fa !important;
    border-left: 3px solid #409eff !important;
    cursor: pointer !important;
}

:deep(.el-menu-item.parent-menu:hover) {
    background-color: #ecf5ff !important;
    color: #409eff !important;
    border-left-color: #337ecc !important;
}

:deep(.el-menu-item.is-active) {
    background-color: #409eff;
    color: #fff;
}

:deep(.el-menu-item:hover) {
    background-color: #ecf5ff;
    color: #409eff;
}


:deep(.submenu-item) {
    padding-left: 32px !important;
    font-size: 13px;
    color: #666;
    height: 36px;
    line-height: 36px;
}

:deep(.submenu-item:hover) {
    background-color: #ecf5ff;
    color: #409eff;
}

:deep(.el-breadcrumb) {
    font-size: 14px;
}

:deep(.el-button) {
    border-radius: 6px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
    .sidebar {
        width: 220px;
    }
}

@media (max-width: 768px) {
    .task-detail {
        flex-direction: column;
        height: auto;
    }

    .sidebar {
        width: 100%;
        height: auto;
        order: 1;
    }

    .main-content {
        order: 1;
        min-height: 400px;
    }
}

/* 导出页面样式 */
.export-content {
    max-width: 800px;
    margin: 0 auto;
}

.export-card {
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #409eff;
}

.export-info {
    margin-bottom: 24px;
}

.export-info p {
    margin: 12px 0;
    line-height: 1.6;
}

.export-list {
    margin: 12px 0;
    padding-left: 20px;
}

.export-list li {
    margin: 8px 0;
    color: #606266;
    line-height: 1.5;
}

.export-actions {
    text-align: center;
    padding: 20px 0;
}

.export-actions .el-button {
    padding: 12px 32px;
    font-size: 16px;
    border-radius: 6px;
}
</style>
