<template>
    <div class="container-fullscreen">
        <div class="header">
            <span class="title">数据库管理大屏 (超级管理员专属)</span>
            <div class="actions">
                <span style="margin-right: 10px; color: #fff;">选择数据表：</span>
                <el-select v-model="selectedTable" placeholder="请选择数据表" @change="handleTableChange" style="width: 250px;" :popper-append-to-body="false">
                    <el-option
                        v-for="item in tableList"
                        :key="item"
                        :label="item"
                        :value="item"
                    />
                </el-select>
                <el-button type="primary" style="margin-left: 20px;" @click="handleAdd" :disabled="!selectedTable">
                    <el-icon><Plus /></el-icon> 新增数据
                </el-button>
                <el-button type="danger" style="margin-left: 20px;" @click="logout">
                    退出登录
                </el-button>
            </div>
        </div>

        <div class="table-wrapper">
            <el-table :data="tableData" border style="width: 100%;" v-loading="loading" height="100%">
                <el-table-column v-for="col in columns" :key="col.field" :prop="col.field" :label="col.field" min-width="150" show-overflow-tooltip>
                </el-table-column>
                <el-table-column label="操作" width="180" fixed="right" v-if="columns.length > 0">
                    <template #default="scope">
                        <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 编辑/新增弹窗 -->
        <el-dialog :title="isEdit ? '编辑数据' : '新增数据'" v-model="dialogVisible" width="60%" destroy-on-close>
            <el-form :model="formData" label-width="120px">
                <el-form-item v-for="col in columns" :key="col.field" :label="col.field">
                    <el-input v-model="formData[col.field]" :disabled="isEdit && col.field === primaryKey" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitForm">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import request from '@/utils/request';

const router = useRouter();
const tableList = ref<string[]>([]);
const selectedTable = ref('');
const tableData = ref<any[]>([]);
const columns = ref<any[]>([]);
const primaryKey = ref('');
const loading = ref(false);

const dialogVisible = ref(false);
const isEdit = ref(false);
const formData = ref<any>({});

// 退出登录
const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('vuems_name');
    localStorage.removeItem('vuems_user');
    router.push('/login');
};

// 获取所有表名
const fetchTables = async () => {
    try {
        const res: any = await request.get('/db/tables');
        console.log('fetchTables res:', res);
        let targetData = res;
        // 如果外层有 data，且包含 code 属性，说明是 Axios 没剥离的数据
        if (res.data && 'code' in res.data) {
            targetData = res.data;
        }
        
        if (targetData.code === 200) {
            tableList.value = targetData.data;
        }
    } catch (error) {
        console.error('获取表名失败', error);
    }
};

// 获取选定表的数据
const fetchTableData = async () => {
    if (!selectedTable.value) return;
    loading.value = true;
    try {
        const res: any = await request.get(`/db/table/${selectedTable.value}`);
        console.log('fetchTableData res:', res);
        
        let targetData = res;
        if (res.data && res.data.code) { // 兼容 axios 原始格式
            targetData = res.data;
        }
        
        if (targetData.code === 200) {
            columns.value = targetData.data.columns;
            tableData.value = targetData.data.rows;
            primaryKey.value = targetData.data.primaryKey;
        } else {
            ElMessage.error(targetData.message || '获取数据失败');
        }
    } catch (error) {
        console.error('获取表数据失败', error);
        ElMessage.error('获取数据失败');
    } finally {
        loading.value = false;
    }
};

const handleTableChange = () => {
    fetchTableData();
};

const handleAdd = () => {
    isEdit.value = false;
    formData.value = {};
    columns.value.forEach(col => {
        formData.value[col.field] = '';
    });
    dialogVisible.value = true;
};

const handleEdit = (row: any) => {
    isEdit.value = true;
    formData.value = { ...row };
    dialogVisible.value = true;
};

const handleDelete = (row: any) => {
    if (!primaryKey.value) {
        ElMessage.warning('该表没有主键，无法删除');
        return;
    }
    
    ElMessageBox.confirm('确定要删除这条数据吗?', '提示', {
        type: 'warning'
    }).then(async () => {
        try {
            const pkValue = row[primaryKey.value];
            const res: any = await request.delete(`/db/table/${selectedTable.value}/${primaryKey.value}/${pkValue}`);
            if (res.code === 200) {
                ElMessage.success('删除成功');
                fetchTableData();
            } else {
                ElMessage.error(res.message || '删除失败');
            }
        } catch (error) {
            console.error('删除失败', error);
            ElMessage.error('删除失败');
        }
    }).catch(() => {});
};

const submitForm = async () => {
    try {
        if (isEdit.value) {
            const pkValue = formData.value[primaryKey.value];
            const res: any = await request.put(`/db/table/${selectedTable.value}/${primaryKey.value}/${pkValue}`, formData.value);
            if (res.code === 200) {
                ElMessage.success('更新成功');
                dialogVisible.value = false;
                fetchTableData();
            } else {
                ElMessage.error(res.message || '更新失败');
            }
        } else {
            const res: any = await request.post(`/db/table/${selectedTable.value}`, formData.value);
            if (res.code === 200) {
                ElMessage.success('新增成功');
                dialogVisible.value = false;
                fetchTableData();
            } else {
                ElMessage.error(res.message || '新增失败');
            }
        }
    } catch (error) {
        console.error('提交失败', error);
        ElMessage.error('提交失败');
    }
};

onMounted(() => {
    fetchTables();
});
</script>

<style scoped>
.container-fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: #f0f2f5;
    z-index: 999; /* 调低一点，不能挡住 Element Plus 的弹出层 */
    display: flex;
    flex-direction: column;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    height: 60px;
    background: #242f42; /* 深色头部 */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.title {
    font-size: 20px;
    font-weight: bold;
    color: #fff;
}
.actions {
    display: flex;
    align-items: center;
}
.table-wrapper {
    flex: 1;
    padding: 20px;
    box-sizing: border-box;
    overflow: hidden;
}
</style>