import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { usePermissStore } from '../store/permiss';
import Home from '../views/home.vue';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                meta: {
                    title: '系统首页',
                    noAuth: true,
                },
                component: () => import(/* webpackChunkName: "dashboard" */ '../views/dashboard.vue'),
            },
            {
                path: '/system-user',
                name: 'system-user',
                meta: {
                    title: '任务管理',
                    permiss: '11',
                },
                component: () => import(/* webpackChunkName: "task-manage" */ '../views/VoyageInfo/task-manage.vue'),
            },
            {
                path: '/task-detail/:task_name',
                name: 'task-detail',
                meta: {
                    title: (route) => route.params.task_name || '任务详情',
                    permiss: '11',
                },
                component: () => import(/* webpackChunkName: "task-detail" */ '../views/VoyageInfo/task-detail.vue'),
            },
            {
                path: '/system-role',
                name: 'system-role',
                meta: {
                    title: '航前质量监督检查记录表',
                    permiss: '12',
                },
                component: () => import(/* webpackChunkName: "inspection-task-list" */ '../views/preVoyageInspection/inspection-task-list.vue'),
            },
            {
                path: '/inspection-record/:task_name',
                name: 'inspection-record',
                meta: {
                    title: '检查记录详情',
                    permiss: '12',
                },
                component: () => import(/* webpackChunkName: "inspection-record" */ '../views/preVoyageInspection/inspection-record.vue'),
            },
            {
                path: '/system-menu',
                name: 'system-menu',
                meta: {
                    title: '菜单管理',
                    permiss: '13',
                },
                component: () => import(/* webpackChunkName: "system-menu" */ '../views/system/menu.vue'),
            },
            {
                path: '/table',
                name: 'basetable',
                meta: {
                    title: '基础表格',
                    permiss: '31',
                },
                component: () => import(/* webpackChunkName: "table" */ '../views/table/basetable.vue'),
            },
            {
                path: '/preVoyageInspection/personnel-qualifications',
                name: 'personnel-qualifications',
                meta: {
                    title: '外业调查人员资质',
                    permiss: '12',
                },
                component: () => import(/* webpackChunkName: "personnel-qualifications" */ '../views/preVoyageInspection/personnel-qualifications-list.vue'),
            },
            {
                path: '/preVoyageInspection/equipment',
                name: 'equipment-list',
                meta: {
                    title: '仪器设备（工作计量器具）',
                    permiss: '12',
                },
                component: () => import(/* webpackChunkName: "equipment-list" */ '../views/preVoyageInspection/equipment-list.vue'),
            },
            {
                path: '/preVoyageInspection/investigation-projects',
                name: 'investigation-list',
                meta: {
                    title: '外业调查项目/仪器比测统计表',
                    permiss: '12',
                },
                component: () => import(/* webpackChunkName: "investigation-list" */ '../views/preVoyageInspection/investigation-list.vue'),
            },
            {
                path: '/expert-personnel',
                name: 'expert-personnel',
                meta: {
                    title: '专家人才',
                    permiss: '5',
                },
                component: () => import(/* webpackChunkName: "expert-personnel" */ '../views/system/expert-personnel.vue'),
            },
            {
                path: '/task-unit',
                name: 'task-unit',
                meta: {
                    title: '任务单位',
                    permiss: '6',
                },
                component: () => import(/* webpackChunkName: "task-unit" */ '../views/system/task-unit.vue'),
            },
            {
                path: '/investigation-personnel',
                name: 'investigation-personnel',
                meta: {
                    title: '调查人员',
                    permiss: '7',
                },
                component: () => import(/* webpackChunkName: "investigation-personnel" */ '../views/system/investigation-personnel.vue'),
            },
            {
                path: '/equipment',
                name: 'equipment',
                meta: {
                    title: '仪器设备',
                    permiss: '8',
                },
                component: () => import(/* webpackChunkName: "equipment" */ '../views/system/equipment.vue'),
            },
            {
                path: '/task-info',
                name: 'task-info',
                meta: {
                    title: '任务信息',
                    permiss: '9',
                },
                component: () => import(/* webpackChunkName: "task-info" */ '../views/system/task-info.vue'),
            },
            {
                path: '/clear-cache',
                name: 'clear-cache',
                meta: {
                    title: '清除缓存',
                    permiss: '0',
                },
                component: () => import(/* webpackChunkName: "clear-cache" */ '../views/system/clear-cache.vue'),
            },
            {
                path: '/table-editor',
                name: 'table-editor',
                meta: {
                    title: '可编辑表格',
                    permiss: '32',
                },
                component: () => import(/* webpackChunkName: "table-editor" */ '../views/table/table-editor.vue'),
            },
            {
                path: '/schart',
                name: 'schart',
                meta: {
                    title: 'schart图表',
                    permiss: '41',
                },
                component: () => import(/* webpackChunkName: "schart" */ '../views/chart/schart.vue'),
            },
            {
                path: '/echarts',
                name: 'echarts',
                meta: {
                    title: 'echarts图表',
                    permiss: '42',
                },
                component: () => import(/* webpackChunkName: "echarts" */ '../views/chart/echarts.vue'),
            },

            {
                path: '/ucenter',
                name: 'ucenter',
                meta: {
                    title: '个人中心',
                },
                component: () => import(/* webpackChunkName: "ucenter" */ '../views/pages/ucenter.vue'),
            },
            {
                path: '/editor',
                name: 'editor',
                meta: {
                    title: '富文本编辑器',
                    permiss: '291',
                },
                component: () => import(/* webpackChunkName: "editor" */ '../views/pages/editor.vue'),
            },
            {
                path: '/markdown',
                name: 'markdown',
                meta: {
                    title: 'markdown编辑器',
                    permiss: '292',
                },
                component: () => import(/* webpackChunkName: "markdown" */ '../views/pages/markdown.vue'),
            },
            {
                path: '/export',
                name: 'export',
                meta: {
                    title: '导出Excel',
                    permiss: '34',
                },
                component: () => import(/* webpackChunkName: "export" */ '../views/table/export.vue'),
            },
            {
                path: '/import',
                name: 'import',
                meta: {
                    title: '导入Excel',
                    permiss: '33',
                },
                component: () => import(/* webpackChunkName: "import" */ '../views/table/import.vue'),
            },
            {
                path: '/calendar',
                name: 'calendar',
                meta: {
                    title: '日历',
                    permiss: '24',
                },
                component: () => import(/* webpackChunkName: "calendar" */ '../views/element/calendar.vue'),
            },
            {
                path: '/watermark',
                name: 'watermark',
                meta: {
                    title: '水印',
                    permiss: '25',
                },
                component: () => import(/* webpackChunkName: "watermark" */ '../views/element/watermark.vue'),
            },
            {
                path: '/carousel',
                name: 'carousel',
                meta: {
                    title: '走马灯',
                    permiss: '23',
                },
                component: () => import(/* webpackChunkName: "carousel" */ '../views/element/carousel.vue'),
            },
            {
                path: '/tour',
                name: 'tour',
                meta: {
                    title: '分步引导',
                    permiss: '26',
                },
                component: () => import(/* webpackChunkName: "tour" */ '../views/element/tour.vue'),
            },
            {
                path: '/steps',
                name: 'steps',
                meta: {
                    title: '步骤条',
                    permiss: '27',
                },
                component: () => import(/* webpackChunkName: "steps" */ '../views/element/steps.vue'),
            },
            {
                path: '/form',
                name: 'forms',
                meta: {
                    title: '表单',
                    permiss: '21',
                },
                component: () => import(/* webpackChunkName: "form" */ '../views/element/form.vue'),
            },
            {
                path: '/upload',
                name: 'upload',
                meta: {
                    title: '上传',
                    permiss: '22',
                },
                component: () => import(/* webpackChunkName: "upload" */ '../views/element/upload.vue'),
            },
            {
                path: '/statistic',
                name: 'statistic',
                meta: {
                    title: '统计',
                    permiss: '28',
                },
                component: () => import(/* webpackChunkName: "statistic" */ '../views/element/statistic.vue'),
            },
        ],
    },
    {
        path: '/login',
        meta: {
            title: '登录',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "login" */ '../views/pages/login.vue'),
    },
    {
        path: '/register',
        meta: {
            title: '注册',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "register" */ '../views/pages/register.vue'),
    },
    {
        path: '/reset-pwd',
        meta: {
            title: '重置密码',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "reset-pwd" */ '../views/pages/reset-pwd.vue'),
    },
    {
        path: '/403',
        meta: {
            title: '没有权限',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "403" */ '../views/pages/403.vue'),
    },
    {
        path: '/404',
        meta: {
            title: '找不到页面',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "404" */ '../views/pages/404.vue'),
    },
    { path: '/:path(.*)', redirect: '/404' },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    NProgress.start();

    let role = null;
    let token = null;

    try {
        role = localStorage.getItem('vuems_name');
        token = localStorage.getItem('token');
    } catch (e) {
        console.warn('无法访问localStorage:', e);
    }

    const permiss = usePermissStore();

    console.log('路由守卫检查:', {
        to: to.path,
        from: from.path,
        role,
        token: token ? `${token.substring(0, 20)}...` : '无',
        noAuth: to.meta.noAuth,
        permiss: to.meta.permiss
    });

    if (!role && !token && to.meta.noAuth !== true) {
        console.log('用户未登录，跳转到登录页');
        next('/login');
    } else if (typeof to.meta.permiss == 'string' && !permiss.key.includes(to.meta.permiss)) {
        console.log('用户权限不足，跳转到403页面');
        // 如果没有权限，则进入403
        next('/403');
    } else {
        console.log('路由守卫通过，继续访问');
        next();
    }
});

router.afterEach(() => {
    NProgress.done();
});

export default router;
