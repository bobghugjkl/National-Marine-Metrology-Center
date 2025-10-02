<template>
    <div class="task-info-container">
        <div class="page-header">
            <h1>任务信息管理</h1>
            <p>这是任务信息页面 - 用于管理任务相关信息</p>
        </div>

        <div class="content-section">
            <el-card class="main-card">
                <template #header>
                    <div class="card-header">
                        <span>任务信息</span>
                    </div>
                </template>

                <div class="welcome-content">
                    <el-empty description="暂无任务信息数据" :image-size="200">
                        <el-button type="primary" @click="handleAddTask">添加任务信息</el-button>
                    </el-empty>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';

const handleAddTask = () => {
    ElMessage.info('功能开发中...');
};
</script>

<style scoped>
.task-info-container {
    padding: 20px;
}

.page-header {
    margin-bottom: 20px;
}

.page-header h1 {
    color: #303133;
    margin: 0 0 10px 0;
    font-size: 24px;
}

.page-header p {
    color: #606266;
    margin: 0;
    font-size: 14px;
}

.content-section {
    margin-top: 20px;
}

.main-card {
    min-height: 400px;
}

.card-header {
    font-weight: 600;
    color: #303133;
}

.welcome-content {
    text-align: center;
    padding: 60px 20px;
}
</style>
