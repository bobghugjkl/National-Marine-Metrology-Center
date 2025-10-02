import request from '../utils/request';

/**
 * 外业设备（工作计量器具）管理API接口
 */

// 获取设备列表
export const fetchEquipmentList = (params?: any) => {
    return request({
        url: '/equipment',
        method: 'get',
        params  // 传递查询参数，如分页、搜索等
    });
};

// 创建设备记录
export const createEquipment = (data: any) => {
    return request({
        url: '/equipment',
        method: 'post',
        data
    });
};

// 更新设备记录
export const updateEquipment = (id: number, data: any) => {
    return request({
        url: `/equipment/${id}`,
        method: 'put',
        data
    });
};

// 删除设备记录
export const deleteEquipment = (id: number) => {
    return request({
        url: `/equipment/${id}`,
        method: 'delete'
    });
};

// 获取单个设备详情
export const fetchEquipmentDetail = (id: number) => {
    return request({
        url: `/equipment/${id}`,
        method: 'get'
    });
};

// 批量删除设备记录
export const batchDeleteEquipment = (ids: number[]) => {
    return request({
        url: '/equipment/batch-delete',
        method: 'post',
        data: { ids }
    });
};

// 下载Excel模板
export const downloadEquipmentTemplate = () => {
    return request({
        url: '/equipment/template',
        method: 'get',
        responseType: 'blob'  // 返回文件流
    });
};

// 导入Excel文件
export const importEquipmentExcel = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    return request({
        url: '/equipment/import',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

// 导出设备数据
export const exportEquipmentData = (params?: any) => {
    return request({
        url: '/equipment/export',
        method: 'get',
        params,
        responseType: 'blob'  // 返回文件流
    });
};

// 获取设备类别选项
export const fetchEquipmentCategories = () => {
    return request({
        url: '/equipment/categories',
        method: 'get'
    });
};

// 获取检定/校准机构选项
export const fetchCalibrationOrganizations = () => {
    return request({
        url: '/equipment/organizations',
        method: 'get'
    });
};
