import { defineStore } from 'pinia';

interface ObjectList {
    [key: string]: string[];
}

export const usePermissStore = defineStore('permiss', {
    state: () => {
        const defaultList: ObjectList = {
            admin: [
                'admin',
                'dashboard',
                '0',
                'task_manage',
                '1',
                '11',
                '12',
                '13',
                '2',
                '21',
                '22',
                '23',
                '24',
                '25',
                '26',
                '27',
                '28',
                '29',
                '291',
                '292',
                '3',
                '31',
                '32',
                '33',
                '34',
                '4',
                '41',
                '42',
                '8',
                '9',
                '61',
                '62',
                '63',
                '64',
                '65',
                '66',
            ],
            center_admin: ['center_admin', 'center_admin_home', '0'],
            project_admin: ['dashboard', '0', 'task_manage'],
            user: ['dashboard', '0', 'task_manage', '5', '6', '7', '8', '9'],
        };
        const username = localStorage.getItem('vuems_name');
        const userData = localStorage.getItem('vuems_user');
        let userRole = 'user'; // 默认普通用户

        if (userData) {
            try {
                const user = JSON.parse(userData);
                if (user.role === '管理员' || user.role === 'super_admin') {
                    userRole = 'admin';
                } else if (user.role === '中心管理员') {
                    userRole = 'center_admin';
                } else if (user.role === '项目管理员') {
                    userRole = 'project_admin';
                } else {
                    userRole = 'user';
                }
            } catch (e) {
                console.error('解析用户数据失败:', e);
            }
        }

        console.log('权限检查:', { username, userRole });
        return {
            key: (defaultList[userRole] || defaultList.user) as string[],
            defaultList,
        };
    },
    actions: {
        handleSet(val: string[]) {
            this.key = val;
        },
    },
});
