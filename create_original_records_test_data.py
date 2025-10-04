#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建外业调查原始记录抽查表测试数据
"""
import sys
import os
import json
from datetime import datetime, timedelta
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入Flask应用和数据库
from backend.app import create_app
from backend.config.database import db
from backend.models.original_records import OriginalRecords
from backend.models.user import User

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = OriginalRecords.query.count()
            if existing_count > 0:
                print(f"数据库中已存在 {existing_count} 条外业调查原始记录抽查表数据")
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
                    'survey_item': '海底地形测量',
                    'task_undertaking_unit': '国家海洋局南海分局',
                    'station': 'A1',
                    'time': '2024-01-15',
                    'location': '南海北部',
                    'spot_check_time': '2024-01-16',
                    'qualified_or_not': '合格',
                    'remarks': '测量数据准确，操作规范',
                    'attachments': [
                        {
                            'filename': '测量记录表.pdf',
                            'url': 'http://localhost:5000/static/uploads/original_records_attachments/20240116_1_测量记录表.pdf',
                            'size': 1024000
                        }
                    ]
                },
                {
                    'task_name': '南海深海探测',
                    'survey_item': '海水采样',
                    'task_undertaking_unit': '中科院海洋研究所',
                    'station': 'B2',
                    'time': '2024-01-17',
                    'location': '南海中部',
                    'spot_check_time': '2024-01-18',
                    'qualified_or_not': '合格',
                    'remarks': '采样过程符合标准，样品保存良好',
                    'attachments': [
                        {
                            'filename': '采样记录.xlsx',
                            'url': 'http://localhost:5000/static/uploads/original_records_attachments/20240118_1_采样记录.xlsx',
                            'size': 512000
                        },
                        {
                            'filename': '样品照片.jpg',
                            'url': 'http://localhost:5000/static/uploads/original_records_attachments/20240118_1_样品照片.jpg',
                            'size': 2048000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'survey_item': '海洋生物调查',
                    'task_undertaking_unit': '上海海洋大学',
                    'station': 'C3',
                    'time': '2024-01-20',
                    'location': '东海海域',
                    'spot_check_time': '2024-01-21',
                    'qualified_or_not': '不合格',
                    'remarks': '调查方法存在问题，需要重新培训',
                    'attachments': [
                        {
                            'filename': '问题记录.docx',
                            'url': 'http://localhost:5000/static/uploads/original_records_attachments/20240121_1_问题记录.docx',
                            'size': 256000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'survey_item': '水质监测',
                    'task_undertaking_unit': '浙江省海洋监测中心',
                    'station': 'D4',
                    'time': '2024-01-22',
                    'location': '东海近岸',
                    'spot_check_time': '2024-01-23',
                    'qualified_or_not': '合格',
                    'remarks': '监测数据完整，仪器运行正常',
                    'attachments': []
                },
                {
                    'task_name': '南海深海探测',
                    'survey_item': '海底沉积物采样',
                    'task_undertaking_unit': '广州海洋地质调查局',
                    'station': 'E5',
                    'time': '2024-01-25',
                    'location': '南海深水区',
                    'spot_check_time': '2024-01-26',
                    'qualified_or_not': '合格',
                    'remarks': '采样深度达到要求，样品质量良好',
                    'attachments': [
                        {
                            'filename': '沉积物分析报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/original_records_attachments/20240126_1_沉积物分析报告.pdf',
                            'size': 3072000
                        },
                        {
                            'filename': '采样视频.mp4',
                            'url': 'http://localhost:5000/static/uploads/original_records_attachments/20240126_1_采样视频.mp4',
                            'size': 10240000
                        }
                    ]
                }
            ]
            
            # 创建记录
            created_count = 0
            for data in test_data:
                record = OriginalRecords(
                    task_name=data['task_name'],
                    survey_item=data['survey_item'],
                    task_undertaking_unit=data['task_undertaking_unit'],
                    station=data['station'],
                    time=data['time'],
                    location=data['location'],
                    spot_check_time=data['spot_check_time'],
                    qualified_or_not=data['qualified_or_not'],
                    remarks=data['remarks'],
                    attachments=json.dumps(data['attachments']),
                    user_id=user_id
                )
                
                db.session.add(record)
                created_count += 1
            
            # 提交事务
            db.session.commit()
            
            print(f"成功创建 {created_count} 条外业调查原始记录抽查表测试数据")
            print("测试数据包括:")
            for data in test_data:
                print(f"  - {data['task_name']} - {data['survey_item']} ({data['qualified_or_not']})")
                
        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("开始创建外业调查原始记录抽查表测试数据...")
    create_test_data()
    print("测试数据创建完成！")
