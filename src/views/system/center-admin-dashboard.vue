<template>
    <div>
        <el-row :gutter="20">
            <!-- 上半部分：所有公司用户管理 (按公司分类) -->
            <el-col :span="24">
                <el-card shadow="hover" class="mgb20">
                    <template #header>
                        <div class="card-header">
                            <span>所有公司员工管理</span>
                            <el-button type="primary" :icon="CirclePlusFilled" @click="handleAddUser">新增员工</el-button>
                        </div>
                    </template>
                    
                    <div v-loading="loadingUsers">
                        <el-empty v-if="groupedUsers.length === 0" description="暂无用户数据"></el-empty>
                        <el-collapse v-else v-model="activeUserCompanyNames">
                            <el-collapse-item v-for="(group, index) in groupedUsers" :key="index" :name="group.companyName">
                                <template #title>
                                    <span class="collapse-title">
                                        <el-icon><OfficeBuilding /></el-icon>
                                        公司：{{ group.companyName }} (共 {{ group.users.length }} 个员工)
                                    </span>
                                </template>
                                <el-table :data="group.users" style="width: 100%" border>
                                    <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
                                    <el-table-column prop="name" label="用户名" width="120"></el-table-column>
                                    <el-table-column prop="login_name" label="登录名" width="120"></el-table-column>
                                    <el-table-column prop="role" label="角色" width="150">
                                        <template #default="scope">
                                            <el-tag :type="scope.row.role === '项目管理员' ? 'success' : (scope.row.role === '调查人员' ? 'warning' : 'info')">
                                                {{ scope.row.role }}
                                            </el-tag>
                                        </template>
                                    </el-table-column>
                                    <el-table-column prop="department" label="部门" width="150"></el-table-column>
                                    <el-table-column prop="phone" label="联系电话" width="150"></el-table-column>
                                    <el-table-column prop="email" label="邮箱"></el-table-column>
                                    <el-table-column label="操作" width="180" align="center" fixed="right">
                                        <template #default="scope">
                                            <el-button type="primary" size="small" :disabled="scope.row.id == currentUser?.id" @click="handleEditUser(scope.row)">编辑</el-button>
                                            <el-button type="danger" size="small" :disabled="scope.row.id == currentUser?.id" @click="handleDeleteUser(scope.row)">删除</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-collapse-item>
                        </el-collapse>
                    </div>
                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="20">
            <!-- 下半部分：项目列表 (按公司、创建人分组，只读) -->
            <el-col :span="24">
                <el-card shadow="hover" class="mgb20">
                    <template #header>
                        <div class="card-header">
                            <span>所有公司项目情况 (按公司及创建人分类)</span>
                        </div>
                    </template>
                    
                    <div v-loading="loadingTasks">
                        <el-empty v-if="groupedTasks.length === 0" description="暂无项目数据"></el-empty>
                        <el-collapse v-else v-model="activeTaskCompanyNames">
                            <el-collapse-item v-for="(companyGroup, index) in groupedTasks" :key="index" :name="companyGroup.companyName">
                                <template #title>
                                    <span class="collapse-title">
                                        <el-icon><OfficeBuilding /></el-icon>
                                        公司：{{ companyGroup.companyName }} (共 {{ companyGroup.totalTasks }} 个项目)
                                    </span>
                                </template>
                                
                                <el-collapse v-model="activeTaskUserNames[companyGroup.companyName]">
                                    <el-collapse-item v-for="(userGroup, uIndex) in companyGroup.userGroups" :key="uIndex" :name="userGroup.userName">
                                        <template #title>
                                            <span class="collapse-title" style="font-size: 14px; margin-left: 20px;">
                                                <el-icon><User /></el-icon>
                                                创建人：{{ userGroup.userName }} (共 {{ userGroup.tasks.length }} 个项目)
                                            </span>
                                        </template>
                                        <el-table :data="userGroup.tasks" style="width: 100%" border size="small">
                                            <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
                                            <el-table-column prop="task_name" label="航次任务名称" min-width="150"></el-table-column>
                                            <el-table-column prop="project" label="专项名称" min-width="120"></el-table-column>
                                            <el-table-column prop="task_code" label="任务编号" width="120"></el-table-column>
                                            <el-table-column prop="ship" label="调查船" width="100"></el-table-column>
                                            <el-table-column prop="leader" label="任务负责人" width="100"></el-table-column>
                                            <el-table-column prop="executiontime" label="执行时间" min-width="150"></el-table-column>
                                        </el-table>
                                    </el-collapse-item>
                                </el-collapse>
                            </el-collapse-item>
                        </el-collapse>
                    </div>
                </el-card>
            </el-col>
        </el-row>

        <!-- 员工编辑弹窗 -->
        <el-dialog :title="isEditUser ? '编辑员工' : '新增员工'" v-model="userDialogVisible" width="600px" destroy-on-close>
            <el-form ref="userFormRef" :model="userForm" :rules="userRules" label-width="100px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="用户名" prop="name">
                            <el-input v-model="userForm.name" :disabled="isEditUser" placeholder="请输入用户名"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="登录名" prop="login_name">
                            <el-input v-model="userForm.login_name" :disabled="isEditUser" placeholder="请输入登录名"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="密码" prop="password" :required="!isEditUser">
                            <el-input type="password" v-model="userForm.password" :disabled="isEditUser" placeholder="请输入密码"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="角色" prop="role">
                            <el-select v-model="userForm.role" placeholder="请选择角色" style="width: 100%;">
                                <el-option label="项目管理员" value="项目管理员"></el-option>
                                <el-option label="调查人员" value="调查人员"></el-option>
                                <el-option label="普通用户" value="普通用户"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="公司" prop="company">
                            <el-input v-model="userForm.company" :disabled="isEditUser" placeholder="请输入公司名称"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="部门" prop="department">
                            <el-input v-model="userForm.department" :disabled="isEditUser" placeholder="请输入部门"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="联系电话" prop="phone">
                            <el-input v-model="userForm.phone" :disabled="isEditUser" placeholder="请输入联系电话"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="userForm.email" :disabled="isEditUser" placeholder="请输入邮箱"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="userDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitUserForm">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts" name="center-admin-dashboard">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus';
import { CirclePlusFilled, User, OfficeBuilding } from '@element-plus/icons-vue';
import { fetchUserData, createUser, updateUser, deleteUser } from '@/api';
import { fetchTasksNew } from '@/api/task';

// 状态
const loadingUsers = ref(false);
const loadingTasks = ref(false);
const users = ref<any[]>([]);
const tasks = ref<any[]>([]);

const groupedUsers = ref<any[]>([]);
const activeUserCompanyNames = ref<string[]>([]);

const groupedTasks = ref<any[]>([]);
const activeTaskCompanyNames = ref<string[]>([]);
const activeTaskUserNames = ref<Record<string, string[]>>({});

const userMap = ref<Record<number, any>>({}); // 存储用户详细信息，包含 company

// 当前管理员信息
const currentUserStr = localStorage.getItem('vuems_user');
const currentUser = currentUserStr ? JSON.parse(currentUserStr) : null;
const adminCompany = currentUser?.company || '';

// 弹窗状态
const userDialogVisible = ref(false);
const isEditUser = ref(false);
const userFormRef = ref<FormInstance>();
const userForm = reactive<any>({
    name: '',
    login_name: '',
    password: '',
    role: '',
    company: adminCompany,
    department: '',
    phone: '',
    email: ''
});

const userRules = {
    name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    login_name: [{ required: true, message: '请输入登录名', trigger: 'blur' }],
    role: [{ required: true, message: '请选择角色', trigger: 'change' }],
    company: [{ required: true, message: '请输入公司名称', trigger: 'blur' }],
};

// 获取数据
const loadData = async () => {
    loadingUsers.value = true;
    loadingTasks.value = true;
    try {
        // 1. 获取所有用户
        const userRes = await fetchUserData({});
        if (userRes && userRes.data && userRes.data.list) {
            users.value = userRes.data.list;
        } else if (userRes && userRes.data && userRes.data.data && userRes.data.data.list) {
            users.value = userRes.data.data.list;
        } else {
            users.value = userRes?.data || [];
        }
        
        // 建立 user_id -> user 对象映射，用于获取任务的创建人信息和公司信息
        if (Array.isArray(users.value)) {
            users.value.forEach(u => {
                userMap.value[u.id] = u;
            });
        }
        
        groupUsers();

        // 2. 获取所有任务
        const taskRes = await fetchTasksNew({});
        if (taskRes && taskRes.code === 200) {
            tasks.value = taskRes.data.list;
            groupTasks();
        }
    } catch (error) {
        console.error('加载数据失败:', error);
        ElMessage.error('加载数据失败');
    } finally {
        loadingUsers.value = false;
        loadingTasks.value = false;
    }
};

// 将用户按公司分组
const groupUsers = () => {
    const groups: Record<string, any[]> = {};
    users.value.forEach(user => {
        const companyName = user.company || '未知公司';
        if (!groups[companyName]) {
            groups[companyName] = [];
        }
        groups[companyName].push(user);
    });

    const result = [];
    activeUserCompanyNames.value = [];
    for (const companyName in groups) {
        result.push({
            companyName: companyName,
            users: groups[companyName]
        });
        activeUserCompanyNames.value.push(companyName); // 默认展开所有公司
    }
    groupedUsers.value = result;
};

// 将任务按公司和创建人分组
const groupTasks = () => {
    // 结构: companyName -> { userName: tasks[], userName2: tasks[] }
    const companyGroups: Record<string, Record<string, any[]>> = {};
    
    tasks.value.forEach(task => {
        const creatorInfo = userMap.value[task.user_id];
        const companyName = creatorInfo?.company || '未知公司';
        const userName = creatorInfo?.name || `未知用户(ID:${task.user_id})`;
        
        if (!companyGroups[companyName]) {
            companyGroups[companyName] = {};
        }
        if (!companyGroups[companyName][userName]) {
            companyGroups[companyName][userName] = [];
        }
        companyGroups[companyName][userName].push(task);
    });

    const result = [];
    activeTaskCompanyNames.value = [];
    activeTaskUserNames.value = {};
    
    for (const companyName in companyGroups) {
        const userGroupsObj = companyGroups[companyName];
        const userGroupsArr = [];
        let companyTotalTasks = 0;
        
        activeTaskUserNames.value[companyName] = []; // 存储该公司的展开用户名单
        
        for (const userName in userGroupsObj) {
            const userTasks = userGroupsObj[userName];
            companyTotalTasks += userTasks.length;
            userGroupsArr.push({
                userName: userName,
                tasks: userTasks
            });
            activeTaskUserNames.value[companyName].push(userName); // 默认展开所有用户
        }
        
        result.push({
            companyName: companyName,
            totalTasks: companyTotalTasks,
            userGroups: userGroupsArr
        });
        activeTaskCompanyNames.value.push(companyName); // 默认展开所有公司
    }
    groupedTasks.value = result;
};

onMounted(() => {
    loadData();
});

// --- 用户操作 ---
const handleAddUser = () => {
    isEditUser.value = false;
    Object.assign(userForm, {
        name: '',
        login_name: '',
        password: '',
        role: '调查人员',
        company: adminCompany, // 默认当前管理员公司，但允许修改
        department: '',
        phone: '',
        email: ''
    });
    userDialogVisible.value = true;
};

const handleEditUser = (row: any) => {
    isEditUser.value = true;
    Object.assign(userForm, row);
    userForm.password = ''; // 编辑时不显示密码
    userDialogVisible.value = true;
};

const submitUserForm = () => {
    userFormRef.value?.validate(async (valid) => {
        if (!valid) return;
        
        try {
            if (isEditUser.value) {
                // 编辑时不提交空密码
                const dataToSubmit = { ...userForm };
                if (!dataToSubmit.password) {
                    delete dataToSubmit.password;
                }
                await updateUser(userForm.name, dataToSubmit);
                ElMessage.success('更新员工成功');
            } else {
                if (!userForm.password) {
                    ElMessage.error('新增用户必须填写密码');
                    return;
                }
                await createUser(userForm);
                ElMessage.success('新增员工成功');
            }
            userDialogVisible.value = false;
            loadData(); // 重新加载以更新映射和任务分组名称
        } catch (error: any) {
            ElMessage.error(error.response?.data?.message || '操作失败');
        }
    });
};

const handleDeleteUser = async (row: any) => {
    try {
        await ElMessageBox.confirm(`确定要删除员工 "${row.name}" 吗？`, '提示', {
            type: 'warning'
        });
        await deleteUser(row.name);
        ElMessage.success('删除成功');
        loadData();
    } catch (error) {
        if (error !== 'cancel') {
            ElMessage.error('删除失败');
        }
    }
};
</script>

<style scoped>
.mgb20 {
    margin-bottom: 20px;
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
}
.collapse-title {
    font-size: 15px;
    font-weight: 500;
    color: #409EFF;
    display: flex;
    align-items: center;
    gap: 8px;
}
</style>
