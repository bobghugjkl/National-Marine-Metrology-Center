<template>
    <div class="user-profile">
        <el-card class="profile-card">
            <template #header>
                <div class="card-header">
                    <span>个人信息管理</span>
                </div>
            </template>
            
            <el-form
                ref="formRef"
                :model="userInfo"
                :rules="rules"
                label-width="100px"
                class="profile-form"
            >
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="用户名" prop="name">
                            <el-input v-model="userInfo.name" disabled />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="登录名" prop="login_name">
                            <el-input v-model="userInfo.login_name" disabled />
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="性别" prop="sex">
                            <el-select v-model="userInfo.sex" placeholder="请选择性别">
                                <el-option label="男" value="男" />
                                <el-option label="女" value="女" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="部门" prop="department">
                            <el-input v-model="userInfo.department" />
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="角色" prop="role">
                            <el-input v-model="userInfo.role" disabled />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="userInfo.email" type="email" />
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="电话" prop="phone">
                            <el-input v-model="userInfo.phone" />
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-form-item>
                    <el-button type="primary" @click="updateProfile" :loading="loading">
                        保存信息
                    </el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <el-card class="signature-card">
            <template #header>
                <div class="card-header">
                    <span>手写签名</span>
                </div>
            </template>
            
            <SignaturePad 
                ref="signaturePadRef"
                @save="handleSignatureSave"
            />
        </el-card>

        <el-card class="password-card">
            <template #header>
                <div class="card-header">
                    <span>修改密码</span>
                </div>
            </template>
            
            <el-form
                ref="passwordFormRef"
                :model="passwordForm"
                :rules="passwordRules"
                label-width="100px"
                class="password-form"
            >
                <el-form-item label="当前密码" prop="currentPassword">
                    <el-input 
                        v-model="passwordForm.currentPassword" 
                        type="password" 
                        show-password 
                        placeholder="请输入当前密码"
                    />
                </el-form-item>
                
                <el-form-item label="新密码" prop="newPassword">
                    <el-input 
                        v-model="passwordForm.newPassword" 
                        type="password" 
                        show-password 
                        placeholder="请输入新密码"
                    />
                </el-form-item>
                
                <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input 
                        v-model="passwordForm.confirmPassword" 
                        type="password" 
                        show-password 
                        placeholder="请再次输入新密码"
                    />
                </el-form-item>
                
                <el-form-item>
                    <el-button type="primary" @click="updatePassword" :loading="passwordLoading">
                        修改密码
                    </el-button>
                    <el-button @click="resetPasswordForm">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup lang="ts" name="user-profile">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, FormInstance } from 'element-plus';
import { getCurrentUserProfile, updateCurrentUserProfile, changePassword } from '@/api/user-profile';
import SignaturePad from '@/components/signature-pad.vue';

// 用户信息表单
const formRef = ref<FormInstance>();
const userInfo = reactive({
    name: '',
    login_name: '',
    sex: '',
    department: '',
    role: '',
    email: '',
    phone: '',
    signature: ''
});

// 签名组件引用
const signaturePadRef = ref();

// 密码修改表单
const passwordFormRef = ref<FormInstance>();
const passwordForm = reactive({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
});

// 加载状态
const loading = ref(false);
const passwordLoading = ref(false);

// 表单验证规则
const rules = {
    name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    login_name: [{ required: true, message: '请输入登录名', trigger: 'blur' }],
    sex: [{ required: true, message: '请选择性别', trigger: 'change' }],
    department: [{ required: true, message: '请输入部门', trigger: 'blur' }],
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
    ],
    phone: [
        { required: true, message: '请输入电话', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
    ]
};

// 密码验证规则
const passwordRules = {
    currentPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
    newPassword: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
    ],
    confirmPassword: [
        { required: true, message: '请确认新密码', trigger: 'blur' },
        {
            validator: (rule: any, value: any, callback: any) => {
                if (value !== passwordForm.newPassword) {
                    callback(new Error('两次输入的密码不一致'));
                } else {
                    callback();
                }
            },
            trigger: 'blur'
        }
    ]
};

// 获取当前用户信息
const getCurrentUserInfo = async () => {
    try {
        const res = await getCurrentUserProfile();
        if (res.data) {
            Object.assign(userInfo, {
                name: res.data.name || '',
                login_name: res.data.login_name || '',
                sex: res.data.sex || '',
                department: res.data.department || '',
                role: res.data.role || '',
                email: res.data.email || '',
                phone: res.data.phone || '',
                signature: res.data.signature || ''
            });
        }
    } catch (error: any) {
        ElMessage.error('获取用户信息失败');
        console.error('获取用户信息失败:', error);
    }
};

// 更新个人信息
const updateProfile = async () => {
    if (!formRef.value) return;
    
    try {
        await formRef.value.validate();
        loading.value = true;
        
        const updateData = {
            sex: userInfo.sex,
            department: userInfo.department,
            email: userInfo.email,
            phone: userInfo.phone,
            signature: userInfo.signature
        };
        
        await updateCurrentUserProfile(updateData);
        ElMessage.success('个人信息更新成功');
    } catch (error: any) {
        if (error !== false) { // 不是表单验证错误
            ElMessage.error(error.response?.data?.message || '更新失败');
        }
    } finally {
        loading.value = false;
    }
};

// 修改密码
const updatePassword = async () => {
    if (!passwordFormRef.value) return;
    
    try {
        await passwordFormRef.value.validate();
        passwordLoading.value = true;
        
        const updateData = {
            currentPassword: passwordForm.currentPassword,
            newPassword: passwordForm.newPassword
        };
        
        await changePassword(updateData);
        ElMessage.success('密码修改成功，请重新登录');
        
        // 清空密码表单
        resetPasswordForm();
        
        // 延迟跳转到登录页
        setTimeout(() => {
            localStorage.removeItem('token');
            localStorage.removeItem('userId');
            localStorage.removeItem('vuems_name');
            localStorage.removeItem('vuems_user');
            window.location.href = '/#/login';
        }, 2000);
        
    } catch (error: any) {
        if (error !== false) { // 不是表单验证错误
            ElMessage.error(error.response?.data?.message || '密码修改失败');
        }
    } finally {
        passwordLoading.value = false;
    }
};

// 重置个人信息表单
const resetForm = () => {
    getCurrentUserInfo();
};

// 重置密码表单
const resetPasswordForm = () => {
    passwordForm.currentPassword = '';
    passwordForm.newPassword = '';
    passwordForm.confirmPassword = '';
    if (passwordFormRef.value) {
        passwordFormRef.value.clearValidate();
    }
};

// 处理签名保存
const handleSignatureSave = (signatureData: string) => {
    userInfo.signature = signatureData;
    ElMessage.success('签名已保存，请点击"保存信息"按钮完成更新');
};

// 组件挂载时获取用户信息
onMounted(() => {
    getCurrentUserInfo();
});
</script>

<style scoped>
.user-profile {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}

.profile-card,
.signature-card,
.password-card {
    margin-bottom: 20px;
}

.card-header {
    font-size: 18px;
    font-weight: bold;
    color: #303133;
}

.profile-form,
.password-form {
    padding: 20px 0;
}

.el-form-item {
    margin-bottom: 20px;
}

.el-button {
    margin-right: 10px;
}
</style>