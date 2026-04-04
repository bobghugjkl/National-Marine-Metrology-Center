#!/usr/bin/env python3
"""
创建任务单位测试数据脚本
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.config.database import init_db
from backend.models.task_unit import TaskUnit
from backend.config.database import db

def create_test_data():
    """创建测试数据"""
    try:
        # 初始化数据库
        init_db()
        
        # 创建测试数据
        test_units = [
            {
                'unit_name': '测试',
                'specialized_person': '测试人',
                'quality_manager': '测试',
                'contact_person': '测试',
                'contact_info': '测试',
                'remarks': '测试',
                'user_id': 1
            },
            {
                'unit_name': '自然资源部东海局',
                'specialized_person': '测试',
                'quality_manager': '测试',
                'contact_person': '测试',
                'contact_info': '12345678902',
                'remarks': '物理海洋',
                'user_id': 1
            },
            {
                'unit_name': '自然资源部北海局',
                'specialized_person': '测试',
                'quality_manager': '测试',
                'contact_person': '测试',
                'contact_info': '12345678901',
                'remarks': '物理海洋',
                'user_id': 1
            },
            {
                'unit_name': '自然资源部南海局',
                'specialized_person': '测试',
                'quality_manager': '测试',
                'contact_person': '测试',
                'contact_info': '12345678903',
                'remarks': '物理海洋',
                'user_id': 1
            },
            {
                'unit_name': '自然资源部第一海洋研究所',
                'specialized_person': '测试',
                'quality_manager': '测试',
                'contact_person': '测试',
                'contact_info': '12345678904',
                'remarks': '物理海洋',
                'user_id': 1
            },
            {
                'unit_name': '自然资源部第三海洋研究所',
                'specialized_person': '测试',
                'quality_manager': '测试',
                'contact_person': '测试',
                'contact_info': '12345678906',
                'remarks': '海洋化学',
                'user_id': 1
            },
            {
                'unit_name': '自然资源部第二海洋研究所',
                'specialized_person': '测试',
                'quality_manager': '测试',
                'contact_person': '测试',
                'contact_info': '12345678905',
                'remarks': '海洋化学',
                'user_id': 1
            }
        ]
        
        # 检查是否已存在数据
        existing_count = TaskUnit.query.count()
        if existing_count > 0:
            print(f"任务单位表中已存在 {existing_count} 条记录，跳过创建测试数据")
            return
        
        # 创建任务单位记录
        for unit_data in test_units:
            unit = TaskUnit(**unit_data)
            db.session.add(unit)
        
        db.session.commit()
        print(f"成功创建 {len(test_units)} 条任务单位测试数据")
        
        # 显示创建的数据
        units = TaskUnit.query.all()
        print("\n创建的任务单位数据:")
        for unit in units:
            print(f"- {unit.unit_name}: {unit.contact_info} ({unit.remarks})")
            
    except Exception as e:
        print(f"创建测试数据失败: {str(e)}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    create_test_data()
