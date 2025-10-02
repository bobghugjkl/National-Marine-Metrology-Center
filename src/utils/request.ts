import axios, { AxiosInstance, AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

const service: AxiosInstance = axios.create({
    // 恢复原始baseURL配置
    baseURL: 'http://localhost:5000/api',
    timeout: 10000,
    // 移除withCredentials以避免CORS问题
    withCredentials: false
});

service.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // 从 localStorage 获取 token 并添加到请求头
        const token = localStorage.getItem('token');
        console.log('发送请求:', config.url, {
            token: token ? `${token.substring(0, 20)}...` : '无',
            method: config.method,
            hasToken: !!token
        });

        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
            console.log('已添加Authorization头');
        } else {
            console.warn('警告：未找到token，请求可能失败');
            console.log('localStorage中的所有键:', Object.keys(localStorage));
        }
        return config;
    },
    (error: AxiosError) => {
        console.log('请求拦截器错误:', error);
        return Promise.reject();
    }
);

service.interceptors.response.use(
    (response: AxiosResponse) => {
        console.log('收到响应:', response.config.url, {
            status: response.status,
            data: response.data
        });
        if (response.status === 200) {
            // 返回响应数据，前端组件需要访问response.data
            return response.data;
        } else {
            return Promise.reject(new Error('请求失败'));
        }
    },
    (error: AxiosError) => {
        console.error('响应拦截器错误:', error);
        console.error('错误详情:', {
            url: error.config?.url,
            status: error.response?.status,
            statusText: error.response?.statusText,
            data: error.response?.data,
            headers: error.response?.headers
        });

        // 处理 token 过期或无效
        if (error.response?.status === 401) {
            console.error('认证失败，清除本地存储并跳转到登录页');

            // Token 过期或无效，清除本地存储并跳转到登录页
            localStorage.removeItem('token');
            localStorage.removeItem('userId');
            localStorage.removeItem('vuems_name');
            localStorage.removeItem('vuems_user');

            // 提示用户
            let errorMessage = '登录已过期或token无效，请重新登录';
            if (error.response.data && typeof error.response.data === 'object' && 'message' in error.response.data) {
                errorMessage = error.response.data.message as string;
                console.error('认证失败原因:', errorMessage);
            }

            // 显示友好的错误提示
            import('element-plus').then(({ ElMessage }) => {
                ElMessage.error(errorMessage);
            });

            // 延迟跳转，让用户看到提示
            setTimeout(() => {
                window.location.href = '/#/login';
            }, 1500);
        }
        console.log(error);
        return Promise.reject(error);
    }
);

export default service;
