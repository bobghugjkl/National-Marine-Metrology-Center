#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建航前质量监督情况汇总表测试数据
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
from backend.models.pre_summary import PreSummary
from backend.models.user import User

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = PreSummary.query.count()
            if existing_count > 0:
                print(f"数据库中已存在 {existing_count} 条航前质量监督情况汇总表数据")
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
                    'undertaking_unit': '国家海洋局南海分局',
                    'participating_unit': '中科院海洋研究所、广州海洋地质调查局',
                    'task_code': 'NH2024001',
                    'survey_vessel': '海洋六号',
                    'task_leader': '张海洋',
                    'supervision_personnel': '李监督、王检查',
                    'main_participants': '赵研究员、钱工程师、孙技术员',
                    'inspection_date': '2024-01-15',
                    'inspection_details': '对南海深海探测项目进行了全面的航前质量监督检查，包括人员资质、设备状态、安全措施、作业计划等11个方面的检查。检查过程中发现部分设备需要校准，人员培训记录完整，安全防护措施到位。',
                    'inspection_results': '检查结果总体良好，11个检查项目中9项合格，2项需要整改。主要问题：1. GPS定位系统需要重新校准；2. 部分救生设备需要更新。整改措施：已安排设备厂商进行校准，救生设备已订购新设备。',
                    'related_materials': [
                        {
                            'filename': '航前检查报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/pre_summary_attachments/20240115_1_航前检查报告.pdf',
                            'size': 2048000
                        },
                        {
                            'filename': '设备检查清单.xlsx',
                            'url': 'http://localhost:5000/static/uploads/pre_summary_attachments/20240115_1_设备检查清单.xlsx',
                            'size': 512000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'undertaking_unit': '上海海洋大学',
                    'participating_unit': '浙江省海洋监测中心、上海海洋研究所',
                    'task_code': 'DH2024002',
                    'survey_vessel': '向阳红10号',
                    'task_leader': '陈海洋',
                    'supervision_personnel': '刘监督、周检查',
                    'main_participants': '吴研究员、郑工程师、冯技术员',
                    'inspection_date': '2024-01-20',
                    'inspection_details': '对东海海洋调查项目进行了航前质量监督检查，重点检查了调查设备、人员配置、安全预案等。检查发现设备状态良好，人员配置合理，安全预案完善。',
                    'inspection_results': '检查结果优秀，所有检查项目均合格。设备运行正常，人员资质齐全，安全措施到位，可以按计划开始调查作业。',
                    'related_materials': [
                        {
                            'filename': '质量监督报告.docx',
                            'url': 'http://localhost:5000/static/uploads/pre_summary_attachments/20240120_1_质量监督报告.docx',
                            'size': 1024000
                        }
                    ]
                }
            ]
            
            # 创建记录
            created_count = 0
            for data in test_data:
                record = PreSummary(
                    task_name=data['task_name'],
                    undertaking_unit=data['undertaking_unit'],
                    participating_unit=data['participating_unit'],
                    task_code=data['task_code'],
                    survey_vessel=data['survey_vessel'],
                    task_leader=data['task_leader'],
                    supervision_personnel=data['supervision_personnel'],
                    main_participants=data['main_participants'],
                    inspection_date=datetime.strptime(data['inspection_date'], '%Y-%m-%d').date(),
                    inspection_details=data['inspection_details'],
                    inspection_results=data['inspection_results'],
                    related_materials=json.dumps(data['related_materials']),
                    user_id=user_id
                )
                
                db.session.add(record)
                created_count += 1
            
            # 提交事务
            db.session.commit()
            
            print(f"成功创建 {created_count} 条航前质量监督情况汇总表测试数据")
            print("测试数据包括:")
            for data in test_data:
                print(f"  - {data['task_name']} - {data['inspection_date']}")
                
        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("开始创建航前质量监督情况汇总表测试数据...")
    create_test_data()
    print("测试数据创建完成！")
