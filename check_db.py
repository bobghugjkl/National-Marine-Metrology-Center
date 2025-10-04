#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库连接检查脚本
"""
import sys
import os

# 添加后端目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

try:
    from models.task import TaskInfo
    from config.database import db

    print("正在连接数据库...")

    # 检查数据库连接
    tasks = TaskInfo.query.all()
    print(f'数据库中任务数量: {len(tasks)}')

    if tasks:
        print("数据库中的任务:")
        for i, task in enumerate(tasks[:5], 1):  # 只显示前5个
            print(f'{i}. 任务名称: {task.task_name}')
            print(f'   项目: {task.project}')
            print(f'   承担单位: {task.undertake}')
            print(f'   用户ID: {task.user_id}')
            print()
    else:
        print('数据库中没有任务数据')

    print("数据库连接成功!")

except Exception as e:
    print(f'数据库连接错误: {e}')
    import traceback
    traceback.print_exc()
