import request from '../utils/request';

// 表格数据（基础人员数据）
export const fetchData = () => {
    return request({
        url: '/masters',
        method: 'get'
    });
};

// 用户数据
export const fetchUserData = (params?: any) => {
    return request({
        url: '/users',
        method: 'get',
        params  // 传递查询参数
    });
};

// 角色数据（暂时返回空，后续可扩展）
export const fetchRoleData = () => {
    return request({
        url: '/roles',
        method: 'get'
    });
};

// 用户管理接口
export const createUser = (data: any) => {
    return request({
        url: '/users',
        method: 'post',
        data
    });
};

export const updateUser = (name: string, data: any) => {
    return request({
        url: `/users/${encodeURIComponent(name)}`,
        method: 'put',
        data
    });
};

export const deleteUser = (name: string) => {
    return request({
        url: `/users/${encodeURIComponent(name)}`,
        method: 'delete'
    });
};

// 任务管理接口
export const fetchTasks = () => {
    return request({
        url: '/tasks',
        method: 'get'
    });
};

export const createTask = (data: any) => {
    return request({
        url: '/tasks',
        method: 'post',
        data
    });
};

// 基础人员管理
export const createMaster = (data: any) => {
    return request({
        url: '/masters',
        method: 'post',
        data
    });
};

export const updateMaster = (id_card_number: string, data: any) => {
    return request({
        url: `/masters/${encodeURIComponent(id_card_number)}`,
        method: 'put',
        data
    });
};

export const deleteMaster = (id_card_number: string) => {
    return request({
        url: `/masters/${encodeURIComponent(id_card_number)}`,
        method: 'delete'
    });
};

// 任务管理完整接口
export const updateTask = (task_name: string, data: any) => {
    return request({
        url: `/tasks/${encodeURIComponent(task_name)}`,
        method: 'put',
        data
    });
};

export const deleteTask = (task_name: string) => {
    return request({
        url: `/tasks/${encodeURIComponent(task_name)}`,
        method: 'delete'
    });
};

// ==================== 登录注册接口 ====================

// 登录
export const loginUser = (data: any) => {
    return request({
        url: '/login',
        method: 'post',
        data
    });
};

// 注册
export const registerUser = (data: any) => {
    return request({
        url: '/register',
        method: 'post',
        data
    });
};
