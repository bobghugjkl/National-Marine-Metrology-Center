import request from '../utils/request';

// 获取专家人才列表
export const fetchExpertTalentList = (params?: any) => {
    return request({
        url: '/expert-talent',
        method: 'get',
        params
    });
};

// 创建专家人才
export const createExpertTalent = (data: any) => {
    return request({
        url: '/expert-talent',
        method: 'post',
        data
    });
};

// 更新专家人才
export const updateExpertTalent = (expertId: number, data: any) => {
    return request({
        url: `/expert-talent/${expertId}`,
        method: 'put',
        data
    });
};

// 删除专家人才
export const deleteExpertTalent = (expertId: number) => {
    return request({
        url: `/expert-talent/${expertId}`,
        method: 'delete'
    });
};

// 批量删除专家人才
export const batchDeleteExpertTalent = (ids: number[]) => {
    return request({
        url: '/expert-talent/batch-delete',
        method: 'post',
        data: { ids }
    });
};
