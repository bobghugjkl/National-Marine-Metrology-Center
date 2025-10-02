<template>
    <div class="task-unit-container">
        <div class="page-header">
            <h1>任务单位管理</h1>
            <p>这是任务单位页面 - 用于管理任务相关单位信息</p>
        </div>

        <div class="content-section">
            <el-card class="main-card">
                <template #header>
                    <div class="card-header">
                        <span>任务单位信息</span>
                    </div>
                </template>

                <div class="welcome-content">
                    <el-empty description="暂无任务单位数据" :image-size="200">
                        <el-button type="primary" @click="handleAddUnit">添加任务单位</el-button>
                    </el-empty>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';

const handleAddUnit = () => {
    ElMessage.info('功能开发中...');
};
</script>

<style scoped>
.task-unit-container {
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
