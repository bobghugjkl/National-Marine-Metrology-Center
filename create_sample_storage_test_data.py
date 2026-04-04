#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建外业调查样品储存记录抽查表测试数据
"""
import sys
import os
import json
from datetime import datetime, timedelta
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# 导入Flask应用和数据库
from backend.app import create_app
from backend.config.database import db
from backend.models.sample_storage import SampleStorage
from backend.models.user import User

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = SampleStorage.query.count()
            if existing_count > 0:
                print(f"数据库中已存在 {existing_count} 条外业调查样品储存记录抽查表数据")
                return
            
            # 获取用户ID（假设存在用户）
            user = User.query.first()
            if not user:
                print("错误：未找到用户，请先创建用户")
                return
            
            user_id = user.id
            print(f"使用用户ID: {user_id}")
            
            # 测试数据
            test_data = [
                {
                    'task_name': '南海深海探测',
                    'survey_item': '海底沉积物采样',
                    'task_undertaking_unit': '国家海洋局南海分局',
                    'stored_samples': '海底沉积物样品15个，包括表层沉积物、深层沉积物等不同类型',
                    'record_time': '2024-01-15',
                    'spot_check_time': '2024-01-16',
                    'qualified_or_not': '合格',
                    'remarks': '样品保存完好，标签清晰',
                    'attachments': [
                        {
                            'filename': '样品储存记录.pdf',
                            'url': 'http://localhost:5000/static/uploads/sample_storage_attachments/20240116_1_样品储存记录.pdf',
                            'size': 1024000
                        }
                    ]
                },
                {
                    'task_name': '南海深海探测',
                    'survey_item': '海水样品采集',
                    'task_undertaking_unit': '中科院海洋研究所',
                    'stored_samples': '海水样品20个，包括不同深度的水样，已按标准方法保存',
                    'record_time': '2024-01-17',
                    'spot_check_time': '2024-01-18',
                    'qualified_or_not': '合格',
                    'remarks': '保存条件符合要求，温度控制良好',
                    'attachments': [
                        {
                            'filename': '海水样品记录表.xlsx',
                            'url': 'http://localhost:5000/static/uploads/sample_storage_attachments/20240118_1_海水样品记录表.xlsx',
                            'size': 512000
                        },
                        {
                            'filename': '储存环境照片.jpg',
                            'url': 'http://localhost:5000/static/uploads/sample_storage_attachments/20240118_1_储存环境照片.jpg',
                            'size': 2048000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'survey_item': '海洋生物标本',
                    'task_undertaking_unit': '上海海洋大学',
                    'stored_samples': '鱼类标本10个，甲壳类标本15个，软体动物标本8个',
                    'record_time': '2024-01-20',
                    'spot_check_time': '2024-01-21',
                    'qualified_or_not': '合格',
                    'remarks': '标本保存完整，分类标签准确',
                    'attachments': [
                        {
                            'filename': '生物标本清单.docx',
                            'url': 'http://localhost:5000/static/uploads/sample_storage_attachments/20240121_1_生物标本清单.docx',
                            'size': 256000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'survey_item': '水质监测样品',
                    'task_undertaking_unit': '浙江省海洋监测中心',
                    'stored_samples': '水质监测样品12个，包括pH、溶解氧、营养盐等参数检测样品',
                    'record_time': '2024-01-22',
                    'spot_check_time': '2024-01-23',
                    'qualified_or_not': '合格',
                    'remarks': '样品保存条件良好，检测数据准确',
                    'attachments': []
                },
                {
                    'task_name': '南海深海探测',
                    'survey_item': '岩石样品采集',
                    'task_undertaking_unit': '广州海洋地质调查局',
                    'stored_samples': '海底岩石样品8个，包括玄武岩、花岗岩等不同类型',
                    'record_time': '2024-01-25',
                    'spot_check_time': '2024-01-26',
                    'qualified_or_not': '合格',
                    'remarks': '样品保存完整，地质特征明显',
                    'attachments': [
                        {
                            'filename': '岩石样品分析报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/sample_storage_attachments/20240126_1_岩石样品分析报告.pdf',
                            'size': 3072000
                        },
                        {
                            'filename': '样品照片.jpg',
                            'url': 'http://localhost:5000/static/uploads/sample_storage_attachments/20240126_1_样品照片.jpg',
                            'size': 1024000
                        }
                    ]
                }
            ]
            
            # 创建记录
            created_count = 0
            for data in test_data:
                record = SampleStorage(
                    task_name=data['task_name'],
                    survey_item=data['survey_item'],
                    task_undertaking_unit=data['task_undertaking_unit'],
                    stored_samples=data['stored_samples'],
                    record_time=datetime.strptime(data['record_time'], '%Y-%m-%d').date(),
                    spot_check_time=datetime.strptime(data['spot_check_time'], '%Y-%m-%d').date(),
                    qualified_or_not=data['qualified_or_not'],
                    remarks=data['remarks'],
                    attachments=json.dumps(data['attachments']),
                    user_id=user_id
                )
                
                db.session.add(record)
                created_count += 1
            
            # 提交事务
            db.session.commit()
            
            print(f"成功创建 {created_count} 条外业调查样品储存记录抽查表测试数据")
            print("测试数据包括:")
            for data in test_data:
                print(f"  - {data['task_name']} - {data['survey_item']}")
                
        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("开始创建外业调查样品储存记录抽查表测试数据...")
    create_test_data()
    print("测试数据创建完成！")
