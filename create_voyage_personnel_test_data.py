#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建航中外业调查人员测试数据
"""

import sys
import os
from datetime import datetime, date

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sys
import os

# 添加backend目录到Python路径
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from app import create_app
from config.database import db
from models.voyage_personnel import VoyagePersonnel

def create_test_data():
    """创建航中外业调查人员测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建测试数据
            test_data = [
                {
                    'task_name': '2024年春季海洋调查',
                    'name': '王五',
                    'sex': '女',
                    'birthdate': date(1988, 11, 8),
                    'professional_title': '助理工程师',
                    'employer': '海洋研究所',
                    'specialty': '海洋生物',
                    'instruments': 'CTD温盐深仪、多参数水质仪、生物采样器',
                    'training': '海洋生物调查技术培训，生物多样性调查专项培训',
                    'remarks': '海洋生物专家，负责生物多样性调查',
                    'attachments': '[]',
                    'user_id': 1
                },
                {
                    'task_name': '2024年春季海洋调查',
                    'name': '赵六',
                    'sex': '男',
                    'birthdate': date(1983, 5, 12),
                    'professional_title': '工程师',
                    'employer': '海洋研究所',
                    'specialty': '海洋化学',
                    'instruments': '分光光度计、原子吸收光谱仪、离子色谱仪',
                    'training': '海洋化学分析培训，水质监测专项培训',
                    'remarks': '海洋化学分析专家，熟悉多种分析仪器',
                    'attachments': '[]',
                    'user_id': 1
                },
                {
                    'task_name': '2024年春季海洋调查',
                    'name': '孙七',
                    'sex': '男',
                    'birthdate': date(1980, 8, 25),
                    'professional_title': '高级工程师',
                    'employer': '海洋研究所',
                    'specialty': '海洋地质',
                    'instruments': '地质采样器、重力仪、磁力仪',
                    'training': '海洋地质调查技术培训，海底采样专项培训',
                    'remarks': '海洋地质专家，具有丰富的外业调查经验',
                    'attachments': '[]',
                    'user_id': 1
                }
            ]
            
            # 插入测试数据
            for data in test_data:
                # 检查是否已存在相同记录
                existing = VoyagePersonnel.query.filter_by(
                    task_name=data['task_name'],
                    name=data['name'],
                    user_id=data['user_id']
                ).first()
                
                if not existing:
                    record = VoyagePersonnel(**data)
                    db.session.add(record)
                    print(f"添加航中外业调查人员: {data['name']} - {data['specialty']}")
                else:
                    print(f"航中外业调查人员已存在: {data['name']} - {data['specialty']}")
            
            # 提交事务
            db.session.commit()
            print("航中外业调查人员测试数据创建成功！")
            
            # 显示创建的数据
            records = VoyagePersonnel.query.filter_by(user_id=1).all()
            print(f"\n当前数据库中共有 {len(records)} 条航中外业调查人员记录:")
            for record in records:
                print(f"- {record.name} ({record.sex}) - {record.specialty} - {record.professional_title}")
                
        except Exception as e:
            print(f"创建航中外业调查人员测试数据失败: {str(e)}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    print("开始创建航中外业调查人员测试数据...")
    success = create_test_data()
    if success:
        print("航中外业调查人员测试数据创建完成！")
    else:
        print("航中外业调查人员测试数据创建失败！")
