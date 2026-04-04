import request from '../utils/request';

/**
 * 航中外业调查项目/仪器比测统计管理API接口
 */

// 获取航中调查项目列表
export const fetchVoyageInvestigationList = (params?: any) => {
    return request({
        url: '/voyage-investigation-projects',
        method: 'get',
        params  // 传递查询参数，如分页、搜索等
    });
};

// 创建航中调查项目记录
export const createVoyageInvestigation = (data: any) => {
    return request({
        url: '/voyage-investigation-projects',
        method: 'post',
        data
    });
};

// 更新航中调查项目记录
export const updateVoyageInvestigation = (id: number, data: any) => {
    return request({
        url: `/voyage-investigation-projects/${id}`,
        method: 'put',
        data
    });
};

// 删除航中调查项目记录
export const deleteVoyageInvestigation = (id: number) => {
    return request({
        url: `/voyage-investigation-projects/${id}`,
        method: 'delete'
    });
};

// 获取单个航中调查项目详情
export const fetchVoyageInvestigationDetail = (id: number) => {
    return request({
        url: `/voyage-investigation-projects/${id}`,
        method: 'get'
    });
};

// 批量删除航中调查项目记录
export const batchDeleteVoyageInvestigation = (ids: number[]) => {
    return request({
        url: '/voyage-investigation-projects/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

// 下载Excel模板
export const downloadVoyageInvestigationTemplate = () => {
    return request({
        url: '/voyage-investigation-projects/template',
        method: 'get',
        responseType: 'blob'  // 返回文件流
    });
};

// 导入Excel文件
export const importVoyageInvestigationExcel = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    return request({
        url: '/voyage-investigation-projects/import',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

// 导出航中调查项目数据
export const exportVoyageInvestigationData = (params?: any) => {
    return request({
        url: '/voyage-investigation-projects/export',
        method: 'get',
        params,
        responseType: 'blob'  // 返回文件流
    });
};

// 获取航中调查项目类型选项
export const fetchVoyageInvestigationTypes = () => {
    return request({
        url: '/voyage-investigation-projects/types',
        method: 'get'
    });
};

// 获取比测单位选项
export const fetchVoyageComparisonUnits = () => {
    return request({
        url: '/voyage-investigation-projects/comparison-units',
        method: 'get'
    });
};

/**
 * 上传航中外业调查项目附件
 * @param file 文件对象
 * @returns
 */
export const uploadVoyageInvestigationAttachment = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return request({
        url: '/voyage-investigation-projects/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
