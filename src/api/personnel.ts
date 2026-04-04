import request from '../utils/request';

/**
 * 获取外业调查人员资质列表
 * @param params 查询参数
 * @returns 
 */
export const getPersonnelQualifications = (params?: any) => {
    return request({
        url: '/personnel-qualifications',
        method: 'get',
        params
    });
};

/**
 * 创建外业调查人员资质记录
 * @param data 人员资质数据
 * @returns 
 */
export const createPersonnelQualification = (data: any) => {
    return request({
        url: '/personnel-qualifications',
        method: 'post',
        data
    });
};

/**
 * 更新外业调查人员资质记录
 * @param id 记录ID
 * @param data 人员资质数据
 * @returns 
 */
export const updatePersonnelQualification = (id: number, data: any) => {
    return request({
        url: `/personnel-qualifications/${id}`,
        method: 'put',
        data
    });
};

/**
 * 删除外业调查人员资质记录
 * @param id 记录ID
 * @returns 
 */
export const deletePersonnelQualification = (id: number) => {
    return request({
        url: `/personnel-qualifications/${id}`,
        method: 'delete'
    });
};

/**
 * 批量删除外业调查人员资质记录
 * @param ids ID数组
 * @returns 
 */
export const batchDeletePersonnelQualifications = (ids: number[]) => {
    return request({
        url: '/personnel-qualifications/batch',
        method: 'delete',
        data: { ids }
    });
};

/**
 * 上传附件
 * @param formData 包含文件的FormData
 * @returns 
 */
export const uploadAttachment = (formData: FormData) => {
    return request({
        url: '/personnel-qualifications/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};