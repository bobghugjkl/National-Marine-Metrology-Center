import request from '../utils/request';

// 获取任务单位列表
export const fetchTaskUnitList = (params?: any) => {
    return request({
        url: '/task-unit',
        method: 'get',
        params
    });
};

// 创建任务单位
export const createTaskUnit = (data: any) => {
    return request({
        url: '/task-unit',
        method: 'post',
        data
    });
};

// 更新任务单位
export const updateTaskUnit = (unitId: number, data: any) => {
    return request({
        url: `/task-unit/${unitId}`,
        method: 'put',
        data
    });
};

// 删除任务单位
export const deleteTaskUnit = (unitId: number) => {
    return request({
        url: `/task-unit/${unitId}`,
        method: 'delete'
    });
};

// 批量删除任务单位
export const batchDeleteTaskUnit = (ids: number[]) => {
    return request({
        url: '/task-unit/batch-delete',
        method: 'post',
        data: { ids }
    });
};
