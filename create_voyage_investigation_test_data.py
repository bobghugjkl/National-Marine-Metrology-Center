#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.models.voyage_investigation import VoyageInvestigationProject
from backend.config.database import db
from datetime import datetime, date

def create_voyage_investigation_test_data():
    """创建航中外业调查项目/仪器比测统计测试数据"""
    app = create_app()
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = VoyageInvestigationProject.query.count()
            if existing_count > 0:
                print(f"数据库中已有 {existing_count} 条航中外业调查项目/仪器比测统计记录")
                return

            # 创建测试数据
            test_investigation_data = [
                {
                    'task_name': '2024年春季海洋调查',
                    'investigation_item_instrument': 'CTD温盐深测量',
                    'comparison_unit_a_instrument': '国家海洋局第一海洋研究所 - SBE-911plus',
                    'comparison_unit_b_instrument': '中科院海洋研究所 - SBE-25',
                    'comparison_time': '2024-03-15',
                    'comparison_location': '青岛海洋科学考察基地',
                    'comparison_result': '数据一致性良好，误差在允许范围内',
                    'remarks': '比测结果符合要求，仪器运行正常',
                    'user_id': 1
                },
                {
                    'task_name': '2024年春季海洋调查',
                    'investigation_item_instrument': '多参数水质分析',
                    'comparison_unit_a_instrument': '国家海洋环境监测中心 - YSI-EXO2',
                    'comparison_unit_b_instrument': '中科院南海海洋研究所 - WTW-3430',
                    'comparison_time': '2024-03-20',
                    'comparison_location': '厦门海洋科学考察基地',
                    'comparison_result': 'pH值测量误差±0.1，溶解氧误差±2%',
                    'remarks': '比测数据可靠，可用于正式调查',
                    'user_id': 1
                },
                {
                    'task_name': '2024年夏季海洋调查',
                    'investigation_item_instrument': '浮游生物采样',
                    'comparison_unit_a_instrument': '中国海洋大学 - 标准浮游生物网',
                    'comparison_unit_b_instrument': '厦门大学 - 改进型浮游生物网',
                    'comparison_time': '2024-06-10',
                    'comparison_location': '舟山海洋科学考察基地',
                    'comparison_result': '采样效率相当，生物量统计一致',
                    'remarks': '两种网具均符合标准，可交替使用',
                    'user_id': 1
                },
                {
                    'task_name': '2024年秋季海洋调查',
                    'investigation_item_instrument': '沉积物采样',
                    'comparison_unit_a_instrument': '国家海洋局第二海洋研究所 - Box-Corer',
                    'comparison_unit_b_instrument': '中科院海洋研究所 - Gravity-Corer',
                    'comparison_time': '2024-09-15',
                    'comparison_location': '大连海洋科学考察基地',
                    'comparison_result': '采样深度一致，样品完整性良好',
                    'remarks': '两种采样器各有优势，可根据需要选择',
                    'user_id': 2
                },
                {
                    'task_name': '2024年冬季海洋调查',
                    'investigation_item_instrument': '海流测量',
                    'comparison_unit_a_instrument': '国家海洋技术中心 - ADCP-600kHz',
                    'comparison_unit_b_instrument': '中科院声学研究所 - ADCP-300kHz',
                    'comparison_time': '2024-12-05',
                    'comparison_location': '天津海洋科学考察基地',
                    'comparison_result': '流速测量精度相当，方向角误差<5°',
                    'remarks': '高频ADCP分辨率更高，低频ADCP穿透力更强',
                    'user_id': 2
                }
            ]

            # 插入数据
            for data in test_investigation_data:
                investigation = VoyageInvestigationProject(**data)
                db.session.add(investigation)

            db.session.commit()
            print(f"成功创建 {len(test_investigation_data)} 条航中外业调查项目/仪器比测统计测试数据")

        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    create_voyage_investigation_test_data()
