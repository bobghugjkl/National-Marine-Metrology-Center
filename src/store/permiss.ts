import { defineStore } from 'pinia';

interface ObjectList {
    [key: string]: string[];
}

export const usePermissStore = defineStore('permiss', {
    state: () => {
        const defaultList: ObjectList = {
            admin: [
                '0',
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
                '5',
                '7',
                '6',
                '61',
                '62',
                '63',
                '64',
                '65',
                '66',
            ],
            user: ['0', '1', '11', '12', '13'],
        };
        const username = localStorage.getItem('vuems_name');
        const userData = localStorage.getItem('vuems_user');
        let userRole = 'user'; // 默认普通用户

        if (userData) {
            try {
                const user = JSON.parse(userData);
                userRole = user.role === '管理员' || user.role === 'super_admin' ? 'admin' : 'user';
            } catch (e) {
                console.error('解析用户数据失败:', e);
            }
        }

        console.log('权限检查:', { username, userRole });
        return {
            key: (userRole === 'admin' ? defaultList.admin : defaultList.user) as string[],
            defaultList,
        };
    },
    actions: {
        handleSet(val: string[]) {
            this.key = val;
        },
    },
});
