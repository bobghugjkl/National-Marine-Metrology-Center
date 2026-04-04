import request from '../utils/request';

// 航中外业调查人员 API

// 获取航中外业调查人员列表
export const fetchVoyagePersonnelList = (params?: any) => {
    return request({
        url: '/voyage-personnel',
        method: 'get',
        params
    });
};

// 创建航中外业调查人员记录
export const createVoyagePersonnel = (data: any) => {
    return request({
        url: '/voyage-personnel',
        method: 'post',
        data
    });
};

// 更新航中外业调查人员记录
export const updateVoyagePersonnel = (id: number, data: any) => {
    return request({
        url: `/voyage-personnel/${id}`,
        method: 'put',
        data
    });
};

// 删除航中外业调查人员记录
export const deleteVoyagePersonnel = (id: number) => {
    return request({
        url: `/voyage-personnel/${id}`,
        method: 'delete'
    });
};

// 批量删除航中外业调查人员记录
export const batchDeleteVoyagePersonnel = (ids: number[]) => {
    return request({
        url: '/voyage-personnel/batch-delete',
        method: 'post',
        data: { ids }
    });
};

// 上传航中外业调查人员附件
export const uploadVoyagePersonnelAttachment = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return request({
        url: '/voyage-personnel/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};
