import { Menus } from '@/types/menu';

export const menuData: Menus[] = [
    {
        id: '0',
        title: '系统首页',
        index: '/dashboard',
        icon: 'Odometer',
    },
    {
        id: '0', 
        title: '任务管理',
        index: '/system-user', 
        icon: 'Document', 
       
    },
    {
        id: '5',
        title: '专家人才',
        index: '/expert-talent',
        icon: 'UserFilled',
        permiss: '5',
    },
    {
        id: '6',
        title: '任务单位',
        index: '/task-unit',
        icon: 'OfficeBuilding',
        permiss: '5',
    },
    {
        id: '7',
        title: '调查人员',
        index: '/investigation-personnel',
        icon: 'UserFilled',
        permiss: '5',
    },
    {
        id: '8',
        title: '仪器设备管理',
        index: '/equipment-management',
        icon: 'Tools',
        permiss: '5',
    },
    {
        id: '9',
        title: '任务信息',
        index: '/task-info',
        icon: 'Star',
        permiss: '9',
    },
    {
        id: '0',
        title: '清除缓存',
        index: '/clear-cache',
        icon: 'Delete',
        permiss: '0',
    },
     {
        id: '2',
        title: '航中检查',
        index: '2',
        icon: 'Ship',
         children: [
            {
                id: '21',
                pid: '1',
                index: '/system-user',
                title: '外业调查人员资质',
            },
           
            {
                id: '22',
                pid: '1',
                index: '/system-menu',
                title: '外业设备（工作计量器具）',
            },
             {
                id: '23',
                pid: '1',
                index: '/system-menu',
                title: '外业调查项目/仪器比测',
            },  
             {
                id: '24',
                pid: '1',
                index: '/system-role',
                title: '监督员日志',
               
            },   
             {
                id: '22',
                pid: '1',
                index: '/system-role',
                title: '外业调查原始记录抽查',
               
            }, 
            {
                id: '22',
                pid: '1',
                index: '/system-role',
                title: '外业调查操作规程统计',
               
            },    
            {
                id: '22',
                pid: '1',
                index: '/system-role',
                title: '外业调查工作日志抽查',
               
            },    
            {
                id: '22',
                pid: '1',
                index: '/system-role',
                title: '外业调查样品存储记录抽查',
               
            },    
            {
                id: '22',
                pid: '1',
                index: '/system-role',
                title: '随船质量监督检查',
               
            },   
        ],
    },
    {
        id: '3',
        title: '航后检查',
        index: '3',
        icon: 'Calendar',
         children: [
            {
                id: '11',
                pid: '1',
                index: '/system-user',
                title: '航后检查',
            },
         
        ],
    },
    {
        id: '4',
        title: '导入导出',
        index: '4',
        icon: 'Setting',
         children: [
            {
                id: '41',
                pid: '1',
                index: '/system-user',
                title: '导入数据包',
            },
            {
                id: '42',
                pid: '1',
                index: '/system-user',
                title: '导出数据包',
            },
         
        ],
    },
    {
        id: '1',
        title: '系统管理',
        index: '1',
        icon: 'HomeFilled',
        children: [
            {
                id: '11',
                pid: '1',
                index: '/user-profile',
                title: '用户管理',
            },
            {
                id: '12',
                pid: '1',
                index: '/system-role',
                title: '角色管理',
            },
            {
                id: '13',
                pid: '1',
                index: '/system-menu',
                title: '菜单管理',
            },
        ],
    },
    {
        id: '2',
        title: '组件',
        index: '2-1',
        icon: 'Calendar',
        children: [
            {
                id: '21',
                pid: '3',
                index: '/form',
                title: '表单',
            },
            {
                id: '22',
                pid: '3',
                index: '/upload',
                title: '上传',
            },
            {
                id: '23',
                pid: '2',
                index: '/carousel',
                title: '走马灯',
            },
            {
                id: '24',
                pid: '2',
                index: '/calendar',
                title: '日历',
            },
            {
                id: '25',
                pid: '2',
                index: '/watermark',
                title: '水印',
            },
            {
                id: '26',
                pid: '2',
                index: '/tour',
                title: '分布引导',
            },
            {
                id: '27',
                pid: '2',
                index: '/steps',
                title: '步骤条',
            },
            {
                id: '28',
                pid: '2',
                index: '/statistic',
                title: '统计',
            },
            {
                id: '29',
                pid: '3',
                index: '29',
                title: '三级菜单',
                children: [
                    {
                        id: '291',
                        pid: '29',
                        index: '/editor',
                        title: '富文本编辑器',
                    },
                    {
                        id: '292',
                        pid: '29',
                        index: '/markdown',
                        title: 'markdown编辑器',
                    },
                ],
            },
        ],
    },
    {
        id: '3',
        title: '表格',
        index: '3',
        icon: 'Calendar',
        children: [
            {
                id: '31',
                pid: '3',
                index: '/table',
                title: '基础表格',
            },
            {
                id: '32',
                pid: '3',
                index: '/table-editor',
                title: '可编辑表格',
            },
            {
                id: '33',
                pid: '3',
                index: '/import',
                title: '导入Excel',
            },
            {
                id: '34',
                pid: '3',
                index: '/export',
                title: '导出Excel',
            },
        ],
    },
    {
        id: '4',
        icon: 'PieChart',
        index: '4',
        title: '图表',
        children: [
            {
                id: '41',
                pid: '4',
                index: '/schart',
                title: 'schart图表',
            },
            {
                id: '42',
                pid: '4',
                index: '/echarts',
                title: 'echarts图表',
            },
        ],
    },
];
