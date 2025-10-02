import request from '../utils/request';

// 获取外业调查操作规程执行统计表列表
export const fetchProcedureExecutionList = (params?: any) => {
    return request({
        url: '/procedure-execution',
        method: 'get',
        params
    });
};

// 创建外业调查操作规程执行统计表
export const createProcedureExecution = (data: any) => {
    return request({
        url: '/procedure-execution',
        method: 'post',
        data
    });
};

// 更新外业调查操作规程执行统计表
export const updateProcedureExecution = (id: number, data: any) => {
    return request({
        url: `/procedure-execution/${id}`,
        method: 'put',
        data
    });
};

// 删除外业调查操作规程执行统计表
export const deleteProcedureExecution = (id: number) => {
    return request({
        url: `/procedure-execution/${id}`,
        method: 'delete'
    });
};

// 批量删除外业调查操作规程执行统计表
export const batchDeleteProcedureExecution = (ids: number[]) => {
    return request({
        url: '/procedure-execution/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

// 上传外业调查操作规程执行统计表附件
export const uploadProcedureExecutionAttachment = (formData: FormData) => {
    return request({
        url: '/procedure-execution/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
