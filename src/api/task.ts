import request from '../utils/request';

// 任务管理 API（直接使用主请求实例）
const taskRequest = request;

// 获取任务列表
export const fetchTasksNew = (params?: any) => {
    return taskRequest({
        url: '/tasks',
        method: 'get',
        params
    });
};

// 创建任务
export const createTaskNew = (data: any) => {
    return taskRequest({
        url: '/tasks',
        method: 'post',
        data
    });
};

// 更新任务
export const updateTaskNew = (task_name: string, data: any) => {
    return taskRequest({
        url: `/tasks/${encodeURIComponent(task_name)}`,
        method: 'put',
        data
    });
};

// 删除任务
export const deleteTaskNew = (task_name: string) => {
    return taskRequest({
        url: `/tasks/${encodeURIComponent(task_name)}`,
        method: 'delete'
    });
};
