import request from '../utils/request';

// 获取外业调查工作日志抽查表列表
export const fetchWorkLogList = (params?: any) => {
    return request({
        url: '/work-log',
        method: 'get',
        params
    });
};

// 创建外业调查工作日志抽查表
export const createWorkLog = (data: any) => {
    return request({
        url: '/work-log',
        method: 'post',
        data
    });
};

// 更新外业调查工作日志抽查表
export const updateWorkLog = (id: number, data: any) => {
    return request({
        url: `/work-log/${id}`,
        method: 'put',
        data
    });
};

// 删除外业调查工作日志抽查表
export const deleteWorkLog = (id: number) => {
    return request({
        url: `/work-log/${id}`,
        method: 'delete'
    });
};

// 批量删除外业调查工作日志抽查表
export const batchDeleteWorkLog = (ids: number[]) => {
    return request({
        url: '/work-log/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

// 上传外业调查工作日志抽查表附件
export const uploadWorkLogAttachment = (formData: FormData) => {
    return request({
        url: '/work-log/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
