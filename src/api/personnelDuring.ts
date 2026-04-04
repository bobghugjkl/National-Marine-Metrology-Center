import request from '../utils/request';

/**
 * 获取航中外业调查人员资质列表
 * @param params 查询参数
 * @returns
 */
export const fetchPersonnelQualificationsDuring = (params?: any) => {
    return request({
        url: '/personnel-qualifications-during',
        method: 'get',
        params
    });
};

/**
 * 创建航中外业调查人员资质记录
 * @param data 人员资质数据
 * @returns
 */
export const createPersonnelQualificationDuring = (data: any) => {
    return request({
        url: '/personnel-qualifications-during',
        method: 'post',
        data
    });
};

/**
 * 更新航中外业调查人员资质记录
 * @param id 记录ID
 * @param data 人员资质数据
 * @returns
 */
export const updatePersonnelQualificationDuring = (id: number, data: any) => {
    return request({
        url: `/personnel-qualifications-during/${id}`,
        method: 'put',
        data
    });
};

/**
 * 删除航中外业调查人员资质记录
 * @param id 记录ID
 * @returns
 */
export const deletePersonnelQualificationDuring = (id: number) => {
    return request({
        url: `/personnel-qualifications-during/${id}`,
        method: 'delete'
    });
};

/**
 * 批量删除航中外业调查人员资质记录
 * @param ids 记录ID数组
 * @returns
 */
export const batchDeletePersonnelQualificationsDuring = (ids: number[]) => {
    return request({
        url: '/personnel-qualifications-during/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

/**
 * 下载Excel模板
 * @returns
 */
export const downloadExcelTemplate = () => {
    return request({
        url: '/personnel-qualifications-during/template',
        method: 'get',
        responseType: 'blob'
    });
};

/**
 * 导入Excel文件
 * @param file 文件对象
 * @returns
 */
export const importExcelFile = (file: FormData) => {
    return request({
        url: '/personnel-qualifications-during/import',
        method: 'post',
        data: file,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

/**
 * 导出航中外业调查人员资质数据
 * @param params 导出参数
 * @returns
 */
export const exportPersonnelQualifications = (params?: any) => {
    return request({
        url: '/personnel-qualifications-during/export',
        method: 'get',
        params,
        responseType: 'blob'
    });
};
