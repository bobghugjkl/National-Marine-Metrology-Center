import request from '../utils/request';

/**
 * 外业调查人员资质管理API接口
 */

// 获取人员资质列表
export const fetchPersonnelQualifications = (params?: any) => {
    return request({
        url: '/personnel-qualifications',
        method: 'get',
        params  // 传递查询参数，如分页、搜索等
    });
};

// 创建人员资质记录
export const createPersonnelQualification = (data: any) => {
    return request({
        url: '/personnel-qualifications',
        method: 'post',
        data
    });
};

// 更新人员资质记录
export const updatePersonnelQualification = (id: number, data: any) => {
    return request({
        url: `/personnel-qualifications/${id}`,
        method: 'put',
        data
    });
};

// 删除人员资质记录
export const deletePersonnelQualification = (id: number) => {
    return request({
        url: `/personnel-qualifications/${id}`,
        method: 'delete'
    });
};

// 获取单个人员资质详情
export const fetchPersonnelQualificationDetail = (id: number) => {
    return request({
        url: `/personnel-qualifications/${id}`,
        method: 'get'
    });
};

// 批量删除人员资质记录
export const batchDeletePersonnelQualifications = (ids: number[]) => {
    return request({
        url: '/personnel-qualifications/batch-delete',
        method: 'post',
        data: { ids }
    });
};

// 下载Excel模板
export const downloadExcelTemplate = () => {
    return request({
        url: '/personnel-qualifications/template',
        method: 'get',
        responseType: 'blob'  // 返回文件流
    });
};

// 导入Excel文件
export const importExcelFile = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    return request({
        url: '/personnel-qualifications/import',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

// 导出Excel文件
export const exportPersonnelQualifications = (params?: any) => {
    return request({
        url: '/personnel-qualifications/export',
        method: 'get',
        params,
        responseType: 'blob'  // 返回文件流
    });
};
