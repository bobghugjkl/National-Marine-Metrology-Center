#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建监督员日志测试数据
"""
import sys
import os
import json
from datetime import datetime, timedelta
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from app import create_app
from models.supervisor_log import SupervisorLog
from config.database import db

def create_test_data():
    """创建监督员日志测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已有数据
            existing_count = SupervisorLog.query.count()
            if existing_count > 0:
                print(f"数据库中已有 {existing_count} 条监督员日志记录，跳过创建")
                return
            
            # 创建测试数据
            test_data = [
                {
                    'task_name': '南海海洋调查任务2024-001',
                    'supervisor': '张监督员',
                    'inspection_date': '2024-01-15',
                    'inspection_content': '检查船舶设备运行状态，确认导航设备正常，检查安全设备配置',
                    'existing_problems': '部分救生设备需要更新，导航雷达信号不稳定',
                    'rectification_status': '已联系设备供应商，预计3天内完成更新',
                    'form_filling_time': '2024-01-15 14:30:00',
                    'attachments': [
                        {
                            'filename': '设备检查报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/supervisor_log_attachments/20240115143000_1_设备检查报告.pdf',
                            'size': 1024000
                        }
                    ]
                },
                {
                    'task_name': '南海海洋调查任务2024-001',
                    'supervisor': '李监督员',
                    'inspection_date': '2024-01-16',
                    'inspection_content': '检查人员资质证书，确认所有人员持证上岗',
                    'existing_problems': '2名船员证书即将过期',
                    'rectification_status': '已安排证书续期培训，下周完成',
                    'form_filling_time': '2024-01-16 09:15:00',
                    'attachments': [
                        {
                            'filename': '人员资质检查表.xlsx',
                            'url': 'http://localhost:5000/static/uploads/supervisor_log_attachments/20240116091500_1_人员资质检查表.xlsx',
                            'size': 512000
                        },
                        {
                            'filename': '证书复印件.pdf',
                            'url': 'http://localhost:5000/static/uploads/supervisor_log_attachments/20240116091500_1_证书复印件.pdf',
                            'size': 2048000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查任务2024-002',
                    'supervisor': '王监督员',
                    'inspection_date': '2024-01-20',
                    'inspection_content': '检查调查设备校准情况，确认数据采集系统正常运行',
                    'existing_problems': '温盐深仪需要重新校准',
                    'rectification_status': '已联系校准机构，明天进行现场校准',
                    'form_filling_time': '2024-01-20 16:45:00',
                    'attachments': [
                        {
                            'filename': '设备校准记录.pdf',
                            'url': 'http://localhost:5000/static/uploads/supervisor_log_attachments/20240120164500_1_设备校准记录.pdf',
                            'size': 1536000
                        }
                    ]
                },
                {
                    'task_name': '东海海洋调查任务2024-002',
                    'supervisor': '赵监督员',
                    'inspection_date': '2024-01-22',
                    'inspection_content': '检查样品采集和保存流程，确认符合标准要求',
                    'existing_problems': '部分样品保存温度不符合要求',
                    'rectification_status': '已调整保存设备温度，重新检查所有样品',
                    'form_filling_time': '2024-01-22 11:20:00',
                    'attachments': []
                },
                {
                    'task_name': '黄海海洋调查任务2024-003',
                    'supervisor': '陈监督员',
                    'inspection_date': '2024-01-25',
                    'inspection_content': '检查数据记录和传输系统，确认数据完整性',
                    'existing_problems': '数据传输偶尔中断',
                    'rectification_status': '已更换网络设备，问题已解决',
                    'form_filling_time': '2024-01-25 13:10:00',
                    'attachments': [
                        {
                            'filename': '数据传输测试报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/supervisor_log_attachments/20240125131000_1_数据传输测试报告.pdf',
                            'size': 768000
                        }
                    ]
                }
            ]
            
            # 插入测试数据
            for data in test_data:
                supervisor_log = SupervisorLog(
                    task_name=data['task_name'],
                    supervisor=data['supervisor'],
                    inspection_date=data['inspection_date'],
                    inspection_content=data['inspection_content'],
                    existing_problems=data['existing_problems'],
                    rectification_status=data['rectification_status'],
                    form_filling_time=data['form_filling_time'],
                    attachments=json.dumps(data['attachments']),
                    user_id=1  # 假设用户ID为1
                )
                db.session.add(supervisor_log)
            
            db.session.commit()
            print(f"成功创建 {len(test_data)} 条监督员日志测试数据")
            
        except Exception as e:
            print(f"创建测试数据失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("开始创建监督员日志测试数据...")
    create_test_data()
    print("监督员日志测试数据创建完成！")
