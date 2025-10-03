import request from '../utils/request';

// 获取仪器设备管理列表（只读）
export const fetchEquipmentManagementList = (params?: any) => {
    return request({
        url: '/equipment-management',
        method: 'get',
        params
    });
};

// 导出仪器设备管理数据
export const exportEquipmentManagement = () => {
    return request({
        url: '/equipment-management/export',
        method: 'get'
    });
};
