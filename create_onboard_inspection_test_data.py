#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建随船质量监督检查表测试数据
"""
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.app import create_app
from backend.config.database import db
from backend.models.onboard_inspection import OnboardInspection

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建测试数据
            test_inspections = [
                {
                    'task_name': '南海深海探测',
                    'inspected_unit': '中国科学院海洋研究所',
                    'participating_unit': '国家海洋局第一海洋研究所',
                    'task_code': 'NS2025001',
                    'chief_scientist': '张海洋',
                    'inspection_date': '2025/10/3',
                    'onboard_supervisor': '李监督',
                    'inspected_unit_personnel': '王研究员、刘工程师、陈技术员',
                    'check_1': '已成立质量保障组织机构，组织架构完整',
                    'check_1_problem': '',
                    'check_2': '严格按照质量保障实施方案执行各项工作',
                    'check_2_problem': '',
                    'check_3': '所有人员均持有相关证书，培训记录完整',
                    'check_3_problem': '',
                    'check_4': '仪器设备检定证书齐全，均在有效期内',
                    'check_4_problem': '',
                    'check_5': '质量检查记录完整，整改措施到位',
                    'check_5_problem': '',
                    'check_6': '样品采集、处理、储存严格按照技术规程执行',
                    'check_6_problem': '',
                    'check_7': '工作日志、班报及原始记录齐全',
                    'check_7_problem': '',
                    'check_8': '所有技术文件均使用法定计量单位',
                    'check_8_problem': '',
                    'check_9': '设备故障记录清晰，解决措施记录完整',
                    'check_9_problem': '',
                    'check_10': '原始记录清晰完整，符合技术规程规定',
                    'check_10_problem': '',
                    'check_11': '原始记录签字完整规范',
                    'check_11_problem': '',
                    'check_12': '原始记录已通过内部质量检查，有质量检查记录',
                    'check_12_problem': '',
                    'team_leader_sign': '张海洋',
                    'task_leader_sign': '李监督',
                    'attachments': json.dumps([
                        {
                            'name': '质量检查报告.pdf',
                            'url': 'http://localhost:5000/static/uploads/onboard_inspection/质量检查报告.pdf',
                            'size': 1024000,
                            'file_path': '/static/uploads/onboard_inspection/质量检查报告.pdf'
                        }
                    ]),
                    'user_id': 1
                },
                {
                    'task_name': '东海海洋调查',
                    'inspected_unit': '国家海洋局第二海洋研究所',
                    'participating_unit': '上海海洋大学',
                    'task_code': 'ES2025002',
                    'chief_scientist': '王海洋',
                    'inspection_date': '2025/10/5',
                    'onboard_supervisor': '赵监督',
                    'inspected_unit_personnel': '孙研究员、周工程师、吴技术员',
                    'check_1': '质量保障组织机构已成立，职责明确',
                    'check_1_problem': '',
                    'check_2': '质量保障实施方案执行情况良好',
                    'check_2_problem': '',
                    'check_3': '人员持证上岗，培训考核记录完整',
                    'check_3_problem': '',
                    'check_4': '仪器设备检定证书齐全有效',
                    'check_4_problem': '',
                    'check_5': '质量检查及整改记录完整',
                    'check_5_problem': '',
                    'check_6': '样品处理符合技术规程要求',
                    'check_6_problem': '',
                    'check_7': '工作日志记录完整',
                    'check_7_problem': '',
                    'check_8': '技术文件使用法定计量单位',
                    'check_8_problem': '',
                    'check_9': '设备故障处理记录完整',
                    'check_9_problem': '',
                    'check_10': '原始记录符合技术规程',
                    'check_10_problem': '',
                    'check_11': '原始记录签字规范',
                    'check_11_problem': '',
                    'check_12': '内部质量检查记录完整',
                    'check_12_problem': '',
                    'team_leader_sign': '王海洋',
                    'task_leader_sign': '赵监督',
                    'attachments': json.dumps([
                        {
                            'name': '检查记录表.xlsx',
                            'url': 'http://localhost:5000/static/uploads/onboard_inspection/检查记录表.xlsx',
                            'size': 512000,
                            'file_path': '/static/uploads/onboard_inspection/检查记录表.xlsx'
                        }
                    ]),
                    'user_id': 1
                }
            ]
            
            # 插入测试数据
            for inspection_data in test_inspections:
                # 检查是否已存在
                existing = OnboardInspection.query.filter_by(
                    task_name=inspection_data['task_name'],
                    user_id=inspection_data['user_id']
                ).first()
                
                if not existing:
                    inspection = OnboardInspection(**inspection_data)
                    db.session.add(inspection)
                    print(f"创建随船质量监督检查表测试数据: {inspection_data['task_name']}")
                else:
                    print(f"随船质量监督检查表测试数据已存在: {inspection_data['task_name']}")
            
            db.session.commit()
            print("随船质量监督检查表测试数据创建完成！")
            
        except Exception as e:
            db.session.rollback()
            print(f"创建测试数据失败: {str(e)}")
            raise

if __name__ == '__main__':
    create_test_data()
