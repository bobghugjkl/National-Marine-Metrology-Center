#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建外业调查项目/仪器比测统计表测试数据脚本
"""
import sys
import os

# 添加后端目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

try:
    from models.investigation import InvestigationProject
    from config.database import db
    from app import create_app

    print("创建外业调查项目测试数据...")

    # 创建Flask应用上下文
    app = create_app()

    with app.app_context():
        # 检查是否已有调查项目数据
        existing_projects = InvestigationProject.query.all()
        print(f'当前数据库中已有 {len(existing_projects)} 个调查项目记录')

        if len(existing_projects) == 0:
            # 创建测试调查项目
            test_project1 = InvestigationProject(
                task_name='南海海洋调查任务',
                investigation_item='海水温度测量',
                unit_a_instrument='CTD温盐深仪A',
                unit_b_instrument='CTD温盐深仪B',
                comparison_time='2024-03-15',
                comparison_location='南海海域A点',
                comparison_result='两台仪器测量结果一致，温度偏差在0.1℃范围内',
                remarks='比测结果良好，可用于正式调查',
                attachments='[]',
                user_id=1  # 假设用户ID为1
            )

            test_project2 = InvestigationProject(
                task_name='南海海洋调查任务',
                investigation_item='海水盐度测量',
                unit_a_instrument='盐度计A',
                unit_b_instrument='盐度计B',
                comparison_time='2024-03-16',
                comparison_location='南海海域B点',
                comparison_result='盐度测量结果偏差较大，需要重新校准仪器',
                remarks='建议对盐度计B进行校准检查',
                attachments='[]',
                user_id=1
            )

            test_project3 = InvestigationProject(
                task_name='东海海洋调查任务',
                investigation_item='海流测量',
                unit_a_instrument='ADV流速仪A',
                unit_b_instrument='ADV流速仪B',
                comparison_time='2024-04-10',
                comparison_location='东海海域C点',
                comparison_result='流速测量结果基本一致，符合精度要求',
                remarks='两台仪器工作状态良好',
                attachments='[]',
                user_id=1
            )

            db.session.add(test_project1)
            db.session.add(test_project2)
            db.session.add(test_project3)

            # 提交到数据库
            db.session.commit()
            print("成功创建了3个测试调查项目记录")
        else:
            print("数据库中已有调查项目数据，跳过创建测试数据")

        # 验证数据
        all_projects = InvestigationProject.query.all()
        print(f"\n数据库中现在共有 {len(all_projects)} 个调查项目记录:")
        for i, project in enumerate(all_projects, 1):
            print(f"{i}. {project.investigation_item} - {project.task_name}")

except Exception as e:
    print(f"创建外业调查项目测试数据失败: {e}")
    import traceback
    traceback.print_exc()
