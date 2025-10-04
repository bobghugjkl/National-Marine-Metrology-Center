#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建外业调查工作日志抽查表测试数据
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
from backend.models.work_log import WorkLog
from backend.models.user import User

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = WorkLog.query.count()
            if existing_count > 0:
                print(f"数据库中已存在 {existing_count} 条外业调查工作日志抽查表数据")
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
                    'survey_project': '海底地形测量',
                    'task_undertaking_unit': '国家海洋局南海分局',
                    'work_log': '今日完成多波束测深仪校准工作，设备运行正常。完成3个测线数据采集，数据质量良好。',
                    'record_time': '2024-01-15',
                    'spot_check_time': '2024-01-16',
                    'remarks': '操作规范，记录完整',
                    'attachments': [
                        {
                            'filename': '工作日志记录.pdf',
                            'url': 'http://localhost:5000/static/uploads/work_log_attachments/20240116_1_工作日志记录.pdf',
                            'size': 1024000
                        }
                    ]
                },
                {
                    'task_name': '南海深海探测',
                    'survey_project': '海水采样',
                    'task_undertaking_unit': '中科院海洋研究所',
                    'work_log': '完成CTD采水器操作培训，进行海水采样作业。采集样品15个，样品保存良好。',
                    'record_time': '2024-01-17',
                    'spot_check_time': '2024-01-18',
                    'remarks': '培训到位，操作熟练',
                    'attachments': [
                        {
                            'filename': '采样记录表.xlsx',
                            'url': 'http://localhost:5000/static/uploads/work_log_attachments/20240118_1_采样记录表.xlsx',
                            'size': 512000
                        },
                        {
                            'filename': '培训证书.jpg',
                            'url': 'http://localhost:5000/static/uploads/work_log_attachments/20240118_1_培训证书.jpg',
                            'size': 2048000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'survey_project': '海洋生物调查',
                    'task_undertaking_unit': '上海海洋大学',
                    'work_log': '进行拖网作业，捕获鱼类样本。记录海洋生物种类和数量，数据记录详细。',
                    'record_time': '2024-01-20',
                    'spot_check_time': '2024-01-21',
                    'remarks': '记录详细，数据准确',
                    'attachments': [
                        {
                            'filename': '生物调查记录.docx',
                            'url': 'http://localhost:5000/static/uploads/work_log_attachments/20240121_1_生物调查记录.docx',
                            'size': 256000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'survey_project': '水质监测',
                    'task_undertaking_unit': '浙江省海洋监测中心',
                    'work_log': '使用便携式水质仪进行水质监测，检测pH、溶解氧、温度等参数。数据正常。',
                    'record_time': '2024-01-22',
                    'spot_check_time': '2024-01-23',
                    'remarks': '监测数据准确，设备运行正常',
                    'attachments': []
                },
                {
                    'task_name': '南海深海探测',
                    'survey_project': '海底沉积物采样',
                    'task_undertaking_unit': '广州海洋地质调查局',
                    'work_log': '使用重力取样器进行海底沉积物采样，采样深度达到设计要求。样品质量良好。',
                    'record_time': '2024-01-25',
                    'spot_check_time': '2024-01-26',
                    'remarks': '采样深度符合要求，样品质量良好',
                    'attachments': [
                        {
                            'filename': '沉积物分析报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/work_log_attachments/20240126_1_沉积物分析报告.pdf',
                            'size': 3072000
                        },
                        {
                            'filename': '采样视频.mp4',
                            'url': 'http://localhost:5000/static/uploads/work_log_attachments/20240126_1_采样视频.mp4',
                            'size': 10240000
                        }
                    ]
                }
            ]
            
            # 创建记录
            created_count = 0
            for data in test_data:
                record = WorkLog(
                    task_name=data['task_name'],
                    survey_project=data['survey_project'],
                    task_undertaking_unit=data['task_undertaking_unit'],
                    work_log=data['work_log'],
                    record_time=data['record_time'],
                    spot_check_time=data['spot_check_time'],
                    remarks=data['remarks'],
                    attachments=json.dumps(data['attachments']),
                    user_id=user_id
                )
                
                db.session.add(record)
                created_count += 1
            
            # 提交事务
            db.session.commit()
            
            print(f"成功创建 {created_count} 条外业调查工作日志抽查表测试数据")
            print("测试数据包括:")
            for data in test_data:
                print(f"  - {data['task_name']} - {data['survey_project']}")
                
        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("开始创建外业调查工作日志抽查表测试数据...")
    create_test_data()
    print("测试数据创建完成！")
