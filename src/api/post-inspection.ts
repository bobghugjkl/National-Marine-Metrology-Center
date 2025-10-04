import request from '../utils/request';

// 获取航后检查表列表
export const fetchPostInspectionList = (params?: any) => {
    return request({
        url: '/post-inspection',
        method: 'get',
        params
    });
};

// 创建航后检查表记录
export const createPostInspection = (data: any) => {
    return request({
        url: '/post-inspection',
        method: 'post',
        data
    });
};

// 更新航后检查表记录
export const updatePostInspection = (id: number, data: any) => {
    return request({
        url: `/post-inspection/${id}`,
        method: 'put',
        data
    });
};

// 删除航后检查表记录
export const deletePostInspection = (id: number) => {
    return request({
        url: `/post-inspection/${id}`,
        method: 'delete'
    });
};

// 批量删除航后检查表记录
export const batchDeletePostInspection = (ids: number[]) => {
    return request({
        url: '/post-inspection/batch-delete',
        method: 'post',
        data: { ids }
    });
};

// 上传航后检查表附件
export const uploadPostInspectionAttachment = (formData: FormData) => {
    return request({
        url: '/post-inspection/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
