import request from '../utils/request';

/**
 * 外业调查项目管理API接口
 */

// 获取调查项目列表
export const fetchInvestigationList = (params?: any) => {
    return request({
        url: '/investigation-projects',
        method: 'get',
        params  // 传递查询参数，如分页、搜索等
    });
};

// 创建调查项目记录
export const createInvestigation = (data: any) => {
    return request({
        url: '/investigation-projects',
        method: 'post',
        data
    });
};

// 更新调查项目记录
export const updateInvestigation = (id: number, data: any) => {
    return request({
        url: `/investigation-projects/${id}`,
        method: 'put',
        data
    });
};

// 删除调查项目记录
export const deleteInvestigation = (id: number) => {
    return request({
        url: `/investigation-projects/${id}`,
        method: 'delete'
    });
};

// 获取单个调查项目详情
export const fetchInvestigationDetail = (id: number) => {
    return request({
        url: `/investigation-projects/${id}`,
        method: 'get'
    });
};

// 批量删除调查项目记录
export const batchDeleteInvestigation = (ids: number[]) => {
    return request({
        url: '/investigation-projects/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

// 下载Excel模板
export const downloadInvestigationTemplate = () => {
    return request({
        url: '/investigation-projects/template',
        method: 'get',
        responseType: 'blob'  // 返回文件流
    });
};

// 导入Excel文件
export const importInvestigationExcel = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    return request({
        url: '/investigation-projects/import',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

// 导出调查项目数据
export const exportInvestigationData = (params?: any) => {
    return request({
        url: '/investigation-projects/export',
        method: 'get',
        params,
        responseType: 'blob'  // 返回文件流
    });
};

// 获取调查项目类型选项
export const fetchInvestigationTypes = () => {
    return request({
        url: '/investigation-projects/types',
        method: 'get'
    });
};

// 获取比测单位选项
export const fetchComparisonUnits = () => {
    return request({
        url: '/investigation-projects/comparison-units',
        method: 'get'
    });
};

/**
 * 上传外业调查项目附件
 * @param formData 包含文件的FormData
 * @returns
 */
export const uploadInvestigationAttachment = (formData: FormData) => {
    return request({
        url: '/investigation-projects/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};
