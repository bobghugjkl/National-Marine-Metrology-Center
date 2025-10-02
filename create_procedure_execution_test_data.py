#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建外业调查操作规程执行统计表测试数据
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
from backend.models.procedure_execution import ProcedureExecution
from backend.models.user import User

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = ProcedureExecution.query.count()
            if existing_count > 0:
                print(f"数据库中已存在 {existing_count} 条外业调查操作规程执行统计表数据")
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
                    'investigation_item_instrument': '海底地形测量/多波束测深仪',
                    'task_undertaking_unit': '国家海洋局南海分局',
                    'has_operating_procedures': '是',
                    'operating_procedure_name': '多波束测深仪操作规程',
                    'remarks': '严格按照操作规程执行，数据质量良好',
                    'attachments': [
                        {
                            'filename': '多波束测深仪操作规程.pdf',
                            'url': 'http://localhost:5000/static/uploads/procedure_execution_attachments/20240116_1_多波束测深仪操作规程.pdf',
                            'size': 2048000
                        }
                    ]
                },
                {
                    'task_name': '南海深海探测',
                    'investigation_item_instrument': '海水采样/CTD采水器',
                    'task_undertaking_unit': '中科院海洋研究所',
                    'has_operating_procedures': '是',
                    'operating_procedure_name': 'CTD采水器操作规范',
                    'remarks': '操作人员已培训，执行情况良好',
                    'attachments': [
                        {
                            'filename': 'CTD操作手册.docx',
                            'url': 'http://localhost:5000/static/uploads/procedure_execution_attachments/20240118_1_CTD操作手册.docx',
                            'size': 1536000
                        },
                        {
                            'filename': '采样记录表.xlsx',
                            'url': 'http://localhost:5000/static/uploads/procedure_execution_attachments/20240118_1_采样记录表.xlsx',
                            'size': 512000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查',
                    'investigation_item_instrument': '海洋生物调查/拖网',
                    'task_undertaking_unit': '上海海洋大学',
                    'has_operating_procedures': '否',
                    'operating_procedure_name': '',
                    'remarks': '缺乏标准操作规程，需要制定相关规范',
                    'attachments': []
                },
                {
                    'task_name': '东海海洋调查',
                    'investigation_item_instrument': '水质监测/便携式水质仪',
                    'task_undertaking_unit': '浙江省海洋监测中心',
                    'has_operating_procedures': '是',
                    'operating_procedure_name': '便携式水质仪使用规范',
                    'remarks': '操作规程完善，执行到位',
                    'attachments': [
                        {
                            'filename': '水质仪使用说明.pdf',
                            'url': 'http://localhost:5000/static/uploads/procedure_execution_attachments/20240123_1_水质仪使用说明.pdf',
                            'size': 1024000
                        }
                    ]
                },
                {
                    'task_name': '南海深海探测',
                    'investigation_item_instrument': '海底沉积物采样/重力取样器',
                    'task_undertaking_unit': '广州海洋地质调查局',
                    'has_operating_procedures': '是',
                    'operating_procedure_name': '重力取样器操作规程',
                    'remarks': '操作规范，样品质量符合要求',
                    'attachments': [
                        {
                            'filename': '重力取样器操作指南.pdf',
                            'url': 'http://localhost:5000/static/uploads/procedure_execution_attachments/20240126_1_重力取样器操作指南.pdf',
                            'size': 3072000
                        },
                        {
                            'filename': '操作培训记录.docx',
                            'url': 'http://localhost:5000/static/uploads/procedure_execution_attachments/20240126_1_操作培训记录.docx',
                            'size': 256000
                        }
                    ]
                }
            ]
            
            # 创建记录
            created_count = 0
            for data in test_data:
                record = ProcedureExecution(
                    task_name=data['task_name'],
                    investigation_item_instrument=data['investigation_item_instrument'],
                    task_undertaking_unit=data['task_undertaking_unit'],
                    has_operating_procedures=data['has_operating_procedures'],
                    operating_procedure_name=data['operating_procedure_name'],
                    remarks=data['remarks'],
                    attachments=json.dumps(data['attachments']),
                    user_id=user_id
                )
                
                db.session.add(record)
                created_count += 1
            
            # 提交事务
            db.session.commit()
            
            print(f"成功创建 {created_count} 条外业调查操作规程执行统计表测试数据")
            print("测试数据包括:")
            for data in test_data:
                print(f"  - {data['task_name']} - {data['investigation_item_instrument']} ({data['has_operating_procedures']})")
                
        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("开始创建外业调查操作规程执行统计表测试数据...")
    create_test_data()
    print("测试数据创建完成！")
