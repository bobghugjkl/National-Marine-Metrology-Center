import request from '../utils/request';

// 获取外业调查原始记录抽查表列表
export const fetchOriginalRecordsList = (params?: any) => {
    return request({
        url: '/original-records',
        method: 'get',
        params
    });
};

// 创建外业调查原始记录抽查表
export const createOriginalRecord = (data: any) => {
    return request({
        url: '/original-records',
        method: 'post',
        data
    });
};

// 更新外业调查原始记录抽查表
export const updateOriginalRecord = (id: number, data: any) => {
    return request({
        url: `/original-records/${id}`,
        method: 'put',
        data
    });
};

// 删除外业调查原始记录抽查表
export const deleteOriginalRecord = (id: number) => {
    return request({
        url: `/original-records/${id}`,
        method: 'delete'
    });
};

// 批量删除外业调查原始记录抽查表
export const batchDeleteOriginalRecord = (ids: number[]) => {
    return request({
        url: '/original-records/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

// 上传外业调查原始记录抽查表附件
export const uploadOriginalRecordAttachment = (formData: FormData) => {
    return request({
        url: '/original-records/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
