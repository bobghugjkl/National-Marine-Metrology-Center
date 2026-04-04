#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建航后检查表测试数据
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
from backend.models.post_inspection import PostInspection
from backend.models.user import User

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = PostInspection.query.count()
            if existing_count > 0:
                print(f"数据库中已存在 {existing_count} 条航后检查表数据")
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
                    'inspection_date': '2024-01-20',
                    'inspection_content': '完成航后设备检查，包括导航设备、通信设备、测量设备等各项功能测试',
                    'existing_problems': '发现GPS定位系统存在轻微漂移，需要校准',
                    'rectification_status': '已联系设备厂商进行校准，预计3天内完成',
                    'form_filling_time': '2024-01-20',
                    'attachments': [
                        {
                            'filename': '航后检查报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/post_inspection_attachments/20240120_1_航后检查报告.pdf',
                            'size': 1024000
                        }
                    ]
                },
                {
                    'task_name': '南海深海探测',
                    'inspection_date': '2024-01-25',
                    'inspection_content': '进行航后安全检查，包括消防设备、救生设备、安全防护设施等',
                    'existing_problems': '救生艇发动机启动困难，需要维修',
                    'rectification_status': '已安排专业维修人员检查，更换了火花塞和燃油滤清器',
                    'form_filling_time': '2024-01-25',
                    'attachments': [
                        {
                            'filename': '安全检查记录.docx',
                            'url': 'http://localhost:5000/static/uploads/post_inspection_attachments/20240125_1_安全检查记录.docx',
                            'size': 512000
                        },
                        {
                            'filename': '设备维修照片.jpg',
                            'url': 'http://localhost:5000/static/uploads/post_inspection_attachments/20240125_1_设备维修照片.jpg',
                            'size': 2048000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'inspection_date': '2024-01-22',
                    'inspection_content': '完成航后数据质量检查，验证采集数据的完整性和准确性',
                    'existing_problems': '部分水质监测数据存在异常值，需要重新分析',
                    'rectification_status': '已重新校准监测设备，对异常数据进行标记和说明',
                    'form_filling_time': '2024-01-22',
                    'attachments': [
                        {
                            'filename': '数据质量报告.xlsx',
                            'url': 'http://localhost:5000/static/uploads/post_inspection_attachments/20240122_1_数据质量报告.xlsx',
                            'size': 256000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'inspection_date': '2024-01-28',
                    'inspection_content': '进行航后人员状态检查，包括身体健康状况、工作状态评估等',
                    'existing_problems': '无',
                    'rectification_status': '所有人员状态良好，无异常情况',
                    'form_filling_time': '2024-01-28',
                    'attachments': []
                },
                {
                    'task_name': '南海深海探测',
                    'inspection_date': '2024-01-30',
                    'inspection_date': '2024-01-30',
                    'inspection_content': '完成航后综合评估，包括任务完成情况、设备状态、人员表现等',
                    'existing_problems': '部分科研设备使用频率过高，需要保养',
                    'rectification_status': '已制定设备保养计划，安排定期维护',
                    'form_filling_time': '2024-01-30',
                    'attachments': [
                        {
                            'filename': '航后综合评估报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/post_inspection_attachments/20240130_1_航后综合评估报告.pdf',
                            'size': 3072000
                        },
                        {
                            'filename': '设备保养计划.docx',
                            'url': 'http://localhost:5000/static/uploads/post_inspection_attachments/20240130_1_设备保养计划.docx',
                            'size': 1024000
                        }
                    ]
                }
            ]
            
            # 创建记录
            created_count = 0
            for data in test_data:
                record = PostInspection(
                    task_name=data['task_name'],
                    inspection_date=datetime.strptime(data['inspection_date'], '%Y-%m-%d').date(),
                    inspection_content=data['inspection_content'],
                    existing_problems=data['existing_problems'],
                    rectification_status=data['rectification_status'],
                    form_filling_time=datetime.strptime(data['form_filling_time'], '%Y-%m-%d').date(),
                    attachments=json.dumps(data['attachments']),
                    user_id=user_id
                )
                
                db.session.add(record)
                created_count += 1
            
            # 提交事务
            db.session.commit()
            
            print(f"成功创建 {created_count} 条航后检查表测试数据")
            print("测试数据包括:")
            for data in test_data:
                print(f"  - {data['task_name']} - {data['inspection_date']}")
                
        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("开始创建航后检查表测试数据...")
    create_test_data()
    print("测试数据创建完成！")
