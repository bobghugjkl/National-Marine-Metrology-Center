<template>
    <div>
        <div class="container">
            <div class="header">
                <h2 class="title">航前质量监督检查记录表</h2>
                <div class="task-info">
                    <span class="label">任务名称：</span>
                    <span class="value">{{ formData.task_name }}</span>
                </div>
            </div>

            <el-form :model="formData" label-width="180px" class="inspection-form">
                <!-- 基本信息 -->
                <el-divider content-position="left"><h3>基本信息</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="检查日期">
                            <el-input v-model="formData.check_date" placeholder="例如：2025/9/30"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="监督单位/监督人员">
                            <el-input v-model="formData.superintendent" placeholder="请输入监督单位/监督人员"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="被监督单位">
                            <el-input v-model="formData.superintended" placeholder="请输入被监督单位"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>

                <!-- 检查内容（11项） -->
                <el-divider content-position="left"><h3>监督检查内容</h3></el-divider>
                
                <template v-for="i in 11" :key="i">
                    <el-card class="check-item-card" shadow="hover">
                        <template #header>
                            <div class="card-header">
                                <div class="check-title">
                                    <span class="check-number">检查项 {{ i }}</span>
                                    <span class="check-content-title">{{ getCheckPlaceholder(i) }}</span>
                                </div>
                                <el-tag :type="getCheckItemStatus(i)">{{ getCheckItemText(i) }}</el-tag>
                            </div>
                        </template>
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-form-item :label="`检查内容${i}`">
                                    <el-input 
                                        v-model="formData[`check_${i}`]" 
                                        type="textarea" 
                                        :rows="2"
                                        :placeholder="getCheckPlaceholder(i)">
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item :label="`存在问题${i}`">
                                    <el-input 
                                        v-model="formData[`check_${i}_problem`]" 
                                        type="textarea" 
                                        :rows="2"
                                        placeholder="如无问题可留空">
                                    </el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-card>
                </template>

                <!-- 补充说明 -->
                <el-divider content-position="left"><h3>补充说明</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="24">
                        <el-form-item label="检查详细说明">
                            <el-input 
                                v-model="formData.check_detail" 
                                type="textarea" 
                                :rows="4"
                                placeholder="请输入详细说明（可选）">
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="24">
                        <el-form-item label="检查结果">
                            <el-input 
                                v-model="formData.check_result" 
                                type="textarea" 
                                :rows="3"
                                placeholder="请输入检查结果（可选）">
                            </el-input>
                        </el-form-item>
                    </el-col>
                </el-row>

                <!-- 签名信息 -->
                <el-divider content-position="left"><h3>签名确认</h3></el-divider>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="组长签字">
                            <el-input v-model="formData.chief_scientist_sign" placeholder="请输入组长签名"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="组长签字日期">
                            <el-date-picker 
                                v-model="formData.chief_scientist_signdate" 
                                type="date" 
                                placeholder="选择日期"
                                value-format="YYYY-MM-DD"
                                style="width: 100%">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="任务负责人签字">
                            <el-input v-model="formData.check_leader_sign" placeholder="请输入任务负责人签名"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="任务负责人签字日期">
                            <el-date-picker 
                                v-model="formData.check_leader_signdate" 
                                type="date" 
                                placeholder="选择日期"
                                value-format="YYYY-MM-DD"
                                style="width: 100%">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                </el-row>

                <!-- 操作按钮 -->
                <el-form-item>
                    <el-button type="primary" size="large" @click="saveData">保存</el-button>
                    <el-button size="large" @click="cancel">取消</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, defineProps, defineEmits } from 'vue';
import { ElMessage } from 'element-plus';
import { fetchInspectionByTask, updateInspection } from '@/api/inspection';

const props = defineProps({
    taskName: {
        type: String,
        required: true
    }
});

const emit = defineEmits(['save-success', 'cancel']);

const formData = reactive<any>({
    task_name: props.taskName,
    check_date: '',
    superintendent: '',
    superintended: '',
    check_1: '',
    check_1_problem: '',
    check_2: '',
    check_2_problem: '',
    check_3: '',
    check_3_problem: '',
    check_4: '',
    check_4_problem: '',
    check_5: '',
    check_5_problem: '',
    check_6: '',
    check_6_problem: '',
    check_7: '',
    check_7_problem: '',
    check_8: '',
    check_8_problem: '',
    check_9: '',
    check_9_problem: '',
    check_10: '',
    check_10_problem: '',
    check_11: '',
    check_11_problem: '',
    check_detail: '',
    check_result: '',
    chief_scientist_sign: '',
    check_leader_sign: '',
    chief_scientist_signdate: '',
    check_leader_signdate: '',
});

// 获取检查项占位符文本
const getCheckPlaceholder = (index: number): string => {
    const placeholders = [
        '是否有证了解航企安全方面、指定了替代性备选项',
        '调查人员是否持有上岗证或培训证明',
        '航次主管仪器设备是否齐备有效',
        '航次所用仪器设备是否都在检定后规定有效期',
        '航次所用仪器设备检定/校准/检测费',
        '不具备检定/校准/检测条件的仪器设备是否经过了相应的比对方法记录',
        '所使用检定等数据是否备齐',
        '船运记录单或质检显示是否按其标出有效期',
        '随船内质量新格是及见效记录',
        '所有工作日志、班组、监据记录提交组织交代并签字须知',
        '海员开展检验的器体、指定案签记录起点对长期照'
    ];
    return placeholders[index - 1] || '请输入检查内容';
};

// 获取检查项状态
const getCheckItemStatus = (index: number): string => {
    const content = formData[`check_${index}`];
    const problem = formData[`check_${index}_problem`];
    
    if (!content) return 'info';
    if (problem) return 'warning';
    return 'success';
};

// 获取检查项状态文本
const getCheckItemText = (index: number): string => {
    const content = formData[`check_${index}`];
    const problem = formData[`check_${index}_problem`];
    
    if (!content) return '未填写';
    if (problem) return '存在问题';
    return '已完成';
};

// 获取检查记录数据
const getData = async () => {
    if (!props.taskName) {
        ElMessage.error('任务名称不能为空');
        return;
    }

    try {
        console.log('正在获取检查记录数据，任务名称:', props.taskName);
        const res = await fetchInspectionByTask(props.taskName);
        console.log('API响应:', res);

        if (res.data.code === 200) {
            console.log('获取数据成功:', res.data.data);
            Object.assign(formData, res.data.data);
        } else {
            console.error('API返回错误:', res.data);
            ElMessage.error(res.data.message || '获取检查记录失败');
        }
    } catch (error: any) {
        console.error('获取检查记录失败:', error);
        console.error('错误响应:', {
            status: error.response?.status,
            statusText: error.response?.statusText,
            data: error.response?.data,
            headers: error.response?.headers
        });

        if (error.response?.status === 401) {
            ElMessage.error('登录已过期，请重新登录');
        } else if (error.response?.status === 403) {
            ElMessage.error('无权限访问此检查记录');
        } else if (error.response?.status === 404) {
            ElMessage.error('检查记录不存在');
        } else if (error.response?.status === 500) {
            ElMessage.error('服务器内部错误，请联系管理员');
        } else {
            ElMessage.error(`获取检查记录失败: ${error.message || '未知错误'}`);
        }
    }
};

// 保存数据
const saveData = async () => {
    try {
        console.log('正在保存检查记录数据:', formData);
        const res = await updateInspection(formData.task_name, formData);
        console.log('保存API响应:', res);

        if (res.data.code === 200) {
            console.log('保存成功');
            ElMessage.success('保存成功');
            emit('save-success');
        } else {
            console.error('保存API返回错误:', res.data);
            ElMessage.error(res.data.message || '保存失败');
        }
    } catch (error: any) {
        console.error('保存检查记录失败:', error);
        if (error.response?.status === 401) {
            ElMessage.error('登录已过期，请重新登录');
        } else if (error.response?.status === 403) {
            ElMessage.error('无权限修改此检查记录');
        } else if (error.response?.status === 404) {
            ElMessage.error('检查记录不存在');
        } else if (error.response?.status === 500) {
            ElMessage.error('服务器内部错误，请联系管理员');
        } else {
            ElMessage.error(`保存失败: ${error.message || '未知错误'}`);
        }
    }
};

// 取消
const cancel = () => {
    emit('cancel');
};

onMounted(() => {
    getData();
});
</script>

<style scoped>
.container {
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    min-height: calc(100vh - 150px);
}

.header {
    margin-bottom: 30px;
}

.title {
    font-size: 22px;
    font-weight: 600;
    color: #303133;
    margin: 15px 0;
}

.task-info {
    font-size: 16px;
    color: #606266;
}

.task-info .label {
    font-weight: 600;
    color: #303133;
}

.task-info .value {
    color: #409EFF;
    font-weight: 500;
}

.inspection-form {
    margin-top: 20px;
}

:deep(.el-divider h3) {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
    margin: 0;
}

.check-item-card {
    margin-bottom: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.check-title {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
}

.check-number {
    font-weight: 600;
    color: #303133;
    font-size: 16px;
    min-width: 80px;
}

.check-content-title {
    color: #606266;
    font-size: 14px;
    line-height: 1.5;
}

:deep(.el-form-item__label) {
    font-weight: 500;
}

:deep(.el-button) {
    min-width: 100px;
}
</style>
