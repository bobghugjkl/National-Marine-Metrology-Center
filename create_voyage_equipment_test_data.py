#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.models.voyage_equipment import VoyageEquipment
from backend.config.database import db
from datetime import datetime, date

def create_voyage_equipment_test_data():
    """创建航中仪器设备测试数据"""
    app = create_app()
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = VoyageEquipment.query.count()
            if existing_count > 0:
                print(f"数据库中已有 {existing_count} 条航中仪器设备记录")
                return

            # 创建测试数据
            test_equipment_data = [
                {
                    'task_name': '2024年春季海洋调查',
                    'category': '仪器',
                    'name': 'CTD温盐深仪',
                    'number': 'CTD-2024-001',
                    'model': 'SBE-911plus',
                    'traceability_method': '可追溯',
                    'calibration_date': '2024-01-15',
                    'certificate_number': 'JJG-2024-001',
                    'validity_period': '2025-01-14',
                    'calibration_organization': '国家海洋计量站',
                    'remarks': '使用前需预热30分钟',
                    'user_id': 1
                },
                {
                    'task_name': '2024年春季海洋调查',
                    'category': '仪器',
                    'name': '多参数水质仪',
                    'number': 'WQ-2024-001',
                    'model': 'YSI-EXO2',
                    'traceability_method': '可追溯',
                    'calibration_date': '2024-01-20',
                    'certificate_number': 'JJG-2024-002',
                    'validity_period': '2025-01-19',
                    'calibration_organization': '国家海洋计量站',
                    'remarks': '定期校准，确保精度',
                    'user_id': 1
                },
                {
                    'task_name': '2024年春季海洋调查',
                    'category': '计量器具',
                    'name': '分光光度计',
                    'number': 'SP-2024-001',
                    'model': 'UV-2600',
                    'traceability_method': '可追溯',
                    'calibration_date': '2024-02-01',
                    'certificate_number': 'JJG-2024-003',
                    'validity_period': '2025-01-31',
                    'calibration_organization': '国家海洋计量站',
                    'remarks': '用于水质分析',
                    'user_id': 1
                },
                {
                    'task_name': '2024年春季海洋调查',
                    'category': '标准物质',
                    'name': '标准海水',
                    'number': 'SW-2024-001',
                    'model': 'NIST-35',
                    'traceability_method': '可追溯',
                    'calibration_date': '2024-02-10',
                    'certificate_number': 'JJG-2024-004',
                    'validity_period': '2025-02-09',
                    'calibration_organization': '国家海洋计量站',
                    'remarks': '用于盐度校准',
                    'user_id': 1
                },
                {
                    'task_name': '2024年春季海洋调查',
                    'category': '仪器',
                    'name': '地质采样器',
                    'number': 'GS-2024-001',
                    'model': 'Box-Corer',
                    'traceability_method': '可追溯',
                    'calibration_date': '2024-02-15',
                    'certificate_number': 'JJG-2024-005',
                    'validity_period': '2025-02-14',
                    'calibration_organization': '国家海洋计量站',
                    'remarks': '用于采集海底沉积物样品',
                    'user_id': 1
                }
            ]

            # 插入数据
            for data in test_equipment_data:
                equipment = VoyageEquipment(**data)
                db.session.add(equipment)

            db.session.commit()
            print(f"成功创建 {len(test_equipment_data)} 条航中仪器设备测试数据")

        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    create_voyage_equipment_test_data()
