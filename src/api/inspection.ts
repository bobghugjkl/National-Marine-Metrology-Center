/**
 * 航前质量监督检查记录 API
 */
import request from '../utils/request';

const inspectionRequest = request.create({
    baseURL: 'http://localhost:5000/api', // 统一后端端口5000
    timeout: 5000
});

// 获取所有检查记录
export const fetchInspections = () => {
    return inspectionRequest({
        url: '/inspections',
        method: 'get'
    });
};

// 根据任务名称获取检查记录
export const fetchInspectionByTask = (task_name: string) => {
    return inspectionRequest({
        url: `/inspections/${encodeURIComponent(task_name)}`,
        method: 'get'
    });
};

// 更新检查记录
export const updateInspection = (task_name: string, data: any) => {
    return inspectionRequest({
        url: `/inspections/${encodeURIComponent(task_name)}`,
        method: 'put',
        data
    });
};

// 创建检查记录
export const createInspection = (data: any) => {
    return inspectionRequest({
        url: '/inspections',
        method: 'post',
        data
    });
};

// 删除检查记录
export const deleteInspection = (task_name: string) => {
    return inspectionRequest({
        url: `/inspections/${encodeURIComponent(task_name)}`,
        method: 'delete'
    });
};
