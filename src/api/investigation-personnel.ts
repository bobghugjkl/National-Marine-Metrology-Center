import request from '../utils/request';

// 获取调查人员列表（只读）
export const fetchInvestigationPersonnelList = (params?: any) => {
    return request({
        url: '/investigation-personnel',
        method: 'get',
        params
    });
};

// 导出调查人员数据
export const exportInvestigationPersonnel = () => {
    return request({
        url: '/investigation-personnel/export',
        method: 'get'
    });
};
