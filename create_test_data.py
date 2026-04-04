#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建测试数据脚本
"""
import sys
import os

# 添加后端目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

try:
    from models.task import TaskInfo
    from config.database import db
    from app import create_app

    print("创建测试数据...")

    # 创建Flask应用上下文
    app = create_app()

    with app.app_context():
        # 检查是否已有任务数据
        existing_tasks = TaskInfo.query.all()
        print(f'当前数据库中已有 {len(existing_tasks)} 个任务')

        if len(existing_tasks) == 0:
            # 创建测试任务
            test_task = TaskInfo(
                task_name='南海海洋调查任务',
                project='南海海洋环境监测',
                task_code='NH-2024-001',
                undertake='海洋研究所',
                participant='南海分队',
                ship='南海号',
                leader='张海洋',
                chief_scientist='李科研',
                superintendent='王监督',
                superintended='南海海监局',
                executiontime='2024年3月-2024年5月',
                subject='海洋环境监测',
                user_id=1  # 假设用户ID为1
            )

            db.session.add(test_task)

            # 创建另一个测试任务
            test_task2 = TaskInfo(
                task_name='东海海洋调查任务',
                project='东海海洋生态调查',
                task_code='DH-2024-002',
                undertake='生态研究所',
                participant='东海分队',
                ship='东海号',
                leader='刘海洋',
                chief_scientist='陈科研',
                superintendent='赵监督',
                superintended='东海海监局',
                executiontime='2024年4月-2024年6月',
                subject='海洋生态调查',
                user_id=1  # 假设用户ID为1
            )

            db.session.add(test_task2)

            # 提交到数据库
            db.session.commit()
            print("✅ 成功创建了2个测试任务")
        else:
            print("数据库中已有任务数据，跳过创建测试数据")

        # 验证数据
        all_tasks = TaskInfo.query.all()
        print(f"\n数据库中现在共有 {len(all_tasks)} 个任务:")
        for i, task in enumerate(all_tasks, 1):
            print(f"{i}. {task.task_name} (用户ID: {task.user_id})")

except Exception as e:
    print(f"创建测试数据失败: {e}")
    import traceback
    traceback.print_exc()
