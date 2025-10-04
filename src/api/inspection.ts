/**
 * 航前质量监督检查记录 API
 */
import request from '../utils/request';

// 直接使用主请求实例，它已经配置了token拦截器
// 获取所有检查记录
export const fetchInspections = () => {
    return request({
        url: '/inspections',
        method: 'get'
    });
};

// 根据任务名称获取检查记录
export const fetchInspectionByTask = (task_name: string) => {
    return request({
        url: `/inspections/task/${encodeURIComponent(task_name)}`,
        method: 'get'
    });
};

// 更新检查记录
export const updateInspection = (task_name: string, data: any) => {
    return request({
        url: `/inspections/${encodeURIComponent(task_name)}`,
        method: 'put',
        data
    });
};

// 创建检查记录
export const createInspection = (data: any) => {
    return request({
        url: '/inspections',
        method: 'post',
        data
    });
};

// 删除检查记录
export const deleteInspection = (task_name: string) => {
    return request({
        url: `/inspections/${encodeURIComponent(task_name)}`,
        method: 'delete'
    });
};
