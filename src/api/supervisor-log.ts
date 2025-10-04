import request from '../utils/request';

// 获取监督员日志列表
export const fetchSupervisorLogList = (params?: any) => {
    return request({
        url: '/supervisor-logs',
        method: 'get',
        params
    });
};

// 创建监督员日志
export const createSupervisorLog = (data: any) => {
    return request({
        url: '/supervisor-logs',
        method: 'post',
        data
    });
};

// 更新监督员日志
export const updateSupervisorLog = (id: number, data: any) => {
    return request({
        url: `/supervisor-logs/${id}`,
        method: 'put',
        data
    });
};

// 删除监督员日志
export const deleteSupervisorLog = (id: number) => {
    return request({
        url: `/supervisor-logs/${id}`,
        method: 'delete'
    });
};

// 批量删除监督员日志
export const batchDeleteSupervisorLog = (ids: number[]) => {
    return request({
        url: '/supervisor-logs/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

// 上传监督员日志附件
export const uploadSupervisorLogAttachment = (formData: FormData) => {
    return request({
        url: '/supervisor-logs/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
