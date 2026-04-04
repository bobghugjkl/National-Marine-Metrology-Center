import request from '../utils/request';

// 获取当前用户信息
export const getCurrentUserProfile = () => {
    return request({
        url: '/user/profile',
        method: 'get'
    });
};

// 更新当前用户信息
export const updateCurrentUserProfile = (data: any) => {
    return request({
        url: '/user/profile',
        method: 'put',
        data
    });
};

// 修改密码
export const changePassword = (data: any) => {
    return request({
        url: '/user/change-password',
        method: 'put',
        data
    });
};
