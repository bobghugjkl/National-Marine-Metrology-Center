import request from '../utils/request';

// 获取随船质量监督检查表
export const fetchOnboardInspection = (taskName: string) => {
    return request({
        url: `/onboard-inspection/${encodeURIComponent(taskName)}`,
        method: 'get'
    });
};

// 创建随船质量监督检查表
export const createOnboardInspection = (data: any) => {
    return request({
        url: '/onboard-inspection',
        method: 'post',
        data
    });
};

// 更新随船质量监督检查表
export const updateOnboardInspection = (taskName: string, data: any) => {
    return request({
        url: `/onboard-inspection/${encodeURIComponent(taskName)}`,
        method: 'put',
        data
    });
};

// 删除随船质量监督检查表
export const deleteOnboardInspection = (taskName: string) => {
    return request({
        url: `/onboard-inspection/${encodeURIComponent(taskName)}`,
        method: 'delete'
    });
};

// 上传随船质量监督检查表附件
export const uploadOnboardInspectionAttachment = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return request({
        url: '/onboard-inspection/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
