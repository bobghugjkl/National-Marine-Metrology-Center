<template>
    <div class="clear-cache-container">
        <div class="page-header">
            <h1>清除缓存</h1>
            <p>清除浏览器缓存以应用最新的菜单配置</p>
        </div>

        <div class="content-section">
            <el-card class="main-card">
                <template #header>
                    <div class="card-header">
                        <span>缓存操作</span>
                    </div>
                </template>

                <div class="cache-actions">
                    <el-alert
                        title="如果菜单显示不正确，请尝试清除缓存并重新登录"
                        type="info"
                        :closable="false"
                        show-icon
                        style="margin-bottom: 20px;"
                    />
                    
                    <div class="button-group">
                        <el-button type="primary" @click="clearLocalStorage">清除本地存储</el-button>
                        <el-button type="warning" @click="clearAllCache">清除所有缓存</el-button>
                        <el-button type="danger" @click="logout">退出登录</el-button>
                    </div>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const router = useRouter();

const clearLocalStorage = () => {
    localStorage.clear();
    ElMessage.success('本地存储已清除，请刷新页面或重新登录');
};

const clearAllCache = () => {
    localStorage.clear();
    sessionStorage.clear();
    
    // 尝试清除应用缓存
    if ('caches' in window) {
        caches.keys().then((names) => {
            names.forEach(name => {
                caches.delete(name);
            });
        });
    }
    
    ElMessage.success('所有缓存已清除，请刷新页面或重新登录');
};

const logout = () => {
    localStorage.clear();
    sessionStorage.clear();
    ElMessage.success('已退出登录，即将跳转到登录页面');
    setTimeout(() => {
        router.push('/login');
    }, 1500);
};
</script>

<style scoped>
.clear-cache-container {
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
    min-height: 300px;
}

.card-header {
    font-weight: 600;
    color: #303133;
}

.cache-actions {
    padding: 20px;
    text-align: center;
}

.button-group {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 20px;
}
</style>
