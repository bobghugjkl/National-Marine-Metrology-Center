#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建仪器设备测试数据脚本
"""
import sys
import os

# 添加后端目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

try:
    from models.equipment import Equipment
    from config.database import db
    from app import create_app

    print("创建仪器设备测试数据...")

    # 创建Flask应用上下文
    app = create_app()

    with app.app_context():
        # 检查是否已有仪器设备数据
        existing_equipment = Equipment.query.all()
        print(f'当前数据库中已有 {len(existing_equipment)} 个仪器设备记录')

        if len(existing_equipment) == 0:
            # 创建测试仪器设备
            test_equipment1 = Equipment(
                task_name='南海海洋调查任务',
                category='仪器',
                name='CTD温盐深仪',
                number='CTD-001',
                model='SBE-911',
                traceability_method='国家海洋计量站校准',
                calibration_date='2024-03-15',
                certificate_number='OM-2024-001',
                validity_period='2025-03-15',
                calibration_organization='国家海洋计量站',
                remarks='用于海洋温盐深剖面测量',
                attachments='[]',
                user_id=1  # 假设用户ID为1
            )

            test_equipment2 = Equipment(
                task_name='南海海洋调查任务',
                category='标准物质',
                name='海水盐度标准物质',
                number='SS-002',
                model='IAPSO标准海水',
                traceability_method='国际原子能机构溯源',
                calibration_date='2024-01-10',
                certificate_number='IAEA-2024-002',
                validity_period='2026-01-10',
                calibration_organization='国际原子能机构',
                remarks='用于盐度测量校准',
                attachments='[]',
                user_id=1
            )

            test_equipment3 = Equipment(
                task_name='东海海洋调查任务',
                category='计量器具',
                name='数字温度计',
                number='DT-003',
                model='Fluke-51II',
                traceability_method='国家计量院校准',
                calibration_date='2024-02-20',
                certificate_number='NIM-2024-003',
                validity_period='2025-02-20',
                calibration_organization='国家计量院',
                remarks='用于水温测量',
                attachments='[]',
                user_id=1
            )

            db.session.add(test_equipment1)
            db.session.add(test_equipment2)
            db.session.add(test_equipment3)

            # 提交到数据库
            db.session.commit()
            print("成功创建了3个测试仪器设备记录")
        else:
            print("数据库中已有仪器设备数据，跳过创建测试数据")

        # 验证数据
        all_equipment = Equipment.query.all()
        print(f"\n数据库中现在共有 {len(all_equipment)} 个仪器设备记录:")
        for i, equipment in enumerate(all_equipment, 1):
            print(f"{i}. {equipment.name} ({equipment.category}) - {equipment.task_name}")

except Exception as e:
    print(f"创建仪器设备测试数据失败: {e}")
    import traceback
    traceback.print_exc()
