import request from '../utils/request';

/**
 * 航中仪器设备（工作计量器具）管理API接口
 */

// 获取航中设备列表
export const fetchVoyageEquipmentList = (params?: any) => {
    return request({
        url: '/voyage-equipment',
        method: 'get',
        params  // 传递查询参数，如分页、搜索等
    });
};

// 创建航中设备记录
export const createVoyageEquipment = (data: any) => {
    return request({
        url: '/voyage-equipment',
        method: 'post',
        data
    });
};

// 更新航中设备记录
export const updateVoyageEquipment = (id: number, data: any) => {
    return request({
        url: `/voyage-equipment/${id}`,
        method: 'put',
        data
    });
};

// 删除航中设备记录
export const deleteVoyageEquipment = (id: number) => {
    return request({
        url: `/voyage-equipment/${id}`,
        method: 'delete'
    });
};

// 获取单个航中设备详情
export const fetchVoyageEquipmentDetail = (id: number) => {
    return request({
        url: `/voyage-equipment/${id}`,
        method: 'get'
    });
};

// 批量删除航中设备记录
export const batchDeleteVoyageEquipment = (ids: number[]) => {
    return request({
        url: '/voyage-equipment/batch-delete',
        method: 'delete',
        data: { ids }
    });
};

// 下载Excel模板
export const downloadVoyageEquipmentTemplate = () => {
    return request({
        url: '/voyage-equipment/template',
        method: 'get',
        responseType: 'blob'  // 返回文件流
    });
};

// 导入Excel文件
export const importVoyageEquipmentExcel = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    return request({
        url: '/voyage-equipment/import',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

// 导出航中设备数据
export const exportVoyageEquipmentData = (params?: any) => {
    return request({
        url: '/voyage-equipment/export',
        method: 'get',
        params,
        responseType: 'blob'  // 返回文件流
    });
};

// 获取航中设备类别选项
export const fetchVoyageEquipmentCategories = () => {
    return request({
        url: '/voyage-equipment/categories',
        method: 'get'
    });
};

// 获取检定/校准机构选项
export const fetchVoyageCalibrationOrganizations = () => {
    return request({
        url: '/voyage-equipment/organizations',
        method: 'get'
    });
};

/**
 * 上传航中仪器设备附件
 * @param file 文件对象
 * @returns
 */
export const uploadVoyageEquipmentAttachment = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return request({
        url: '/voyage-equipment/upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
    });
};
