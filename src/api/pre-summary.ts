import request from '../utils/request';

// 获取航前质量监督情况汇总表列表
export const fetchPreSummaryList = (params?: any) => {
    return request({
        url: '/pre-summary',
        method: 'get',
        params
    });
};

// 创建航前质量监督情况汇总表记录
export const createPreSummary = (data: any) => {
    return request({
        url: '/pre-summary',
        method: 'post',
        data
    });
};

// 更新航前质量监督情况汇总表记录
export const updatePreSummary = (id: number, data: any) => {
    return request({
        url: `/pre-summary/${id}`,
        method: 'put',
        data
    });
};

// 删除航前质量监督情况汇总表记录
export const deletePreSummary = (id: number) => {
    return request({
        url: `/pre-summary/${id}`,
        method: 'delete'
    });
};

// 批量删除航前质量监督情况汇总表记录
export const batchDeletePreSummary = (ids: number[]) => {
    return request({
        url: '/pre-summary/batch-delete',
        method: 'post',
        data: { ids }
    });
};

// 上传航前质量监督情况汇总表相关资料
export const uploadPreSummaryAttachment = (formData: FormData) => {
    return request({
        url: '/pre-summary/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
