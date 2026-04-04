import request from '../utils/request';

// 获取外业调查样品储存记录抽查表列表
export const fetchSampleStorageList = (params?: any) => {
    return request({
        url: '/sample-storage',
        method: 'get',
        params
    });
};

// 创建外业调查样品储存记录抽查表记录
export const createSampleStorage = (data: any) => {
    return request({
        url: '/sample-storage',
        method: 'post',
        data
    });
};

// 更新外业调查样品储存记录抽查表记录
export const updateSampleStorage = (id: number, data: any) => {
    return request({
        url: `/sample-storage/${id}`,
        method: 'put',
        data
    });
};

// 删除外业调查样品储存记录抽查表记录
export const deleteSampleStorage = (id: number) => {
    return request({
        url: `/sample-storage/${id}`,
        method: 'delete'
    });
};

// 批量删除外业调查样品储存记录抽查表记录
export const batchDeleteSampleStorage = (ids: number[]) => {
    return request({
        url: '/sample-storage/batch-delete',
        method: 'post',
        data: { ids }
    });
};

// 上传外业调查样品储存记录抽查表附件
export const uploadSampleStorageAttachment = (formData: FormData) => {
    return request({
        url: '/sample-storage/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
