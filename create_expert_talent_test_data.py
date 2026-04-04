#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建专家人才测试数据
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.app import create_app
from backend.config.database import db
from backend.models.expert_talent import ExpertTalent

def create_test_data():
    """创建测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建测试数据
            test_experts = [
                {
                    'name': '张海洋',
                    'gender': '男',
                    'birth_date': '1980-05-15',
                    'job_title': '教授',
                    'work_unit': '中国科学院海洋研究所',
                    'specialty': '海洋科学',
                    'contact_info': '13800138001',
                    'id_number': '110101198005150001',
                    'bank_card_number': '6222020200000000001',
                    'opening_bank': '中国工商银行北京分行',
                    'remarks': '海洋科学领域专家，主要从事海洋环境研究',
                    'user_id': 1
                },
                {
                    'name': '李研究员',
                    'gender': '女',
                    'birth_date': '1975-08-20',
                    'job_title': '研究员',
                    'work_unit': '国家海洋局第一海洋研究所',
                    'specialty': '海洋工程',
                    'contact_info': '13800138002',
                    'id_number': '110101197508200002',
                    'bank_card_number': '6222020200000000002',
                    'opening_bank': '中国建设银行青岛分行',
                    'remarks': '海洋工程技术专家，擅长海洋工程设计与施工',
                    'user_id': 1
                },
                {
                    'name': '王工程师',
                    'gender': '男',
                    'birth_date': '1985-03-10',
                    'job_title': '高级工程师',
                    'work_unit': '上海海洋大学',
                    'specialty': '海洋技术',
                    'contact_info': '13800138003',
                    'id_number': '110101198503100003',
                    'bank_card_number': '6222020200000000003',
                    'opening_bank': '中国银行上海分行',
                    'remarks': '海洋技术专家，专注于海洋观测技术研发',
                    'user_id': 1
                },
                {
                    'name': '陈博士',
                    'gender': '女',
                    'birth_date': '1988-12-05',
                    'job_title': '副研究员',
                    'work_unit': '厦门大学海洋与地球学院',
                    'specialty': '海洋生物',
                    'contact_info': '13800138004',
                    'id_number': '110101198812050004',
                    'bank_card_number': '6222020200000000004',
                    'opening_bank': '招商银行厦门分行',
                    'remarks': '海洋生物学专家，研究海洋生物多样性',
                    'user_id': 1
                },
                {
                    'name': '刘教授',
                    'gender': '男',
                    'birth_date': '1970-11-18',
                    'job_title': '教授',
                    'work_unit': '中国海洋大学',
                    'specialty': '海洋化学',
                    'contact_info': '13800138005',
                    'id_number': '110101197011180005',
                    'bank_card_number': '6222020200000000005',
                    'opening_bank': '中国农业银行青岛分行',
                    'remarks': '海洋化学专家，主要从事海洋环境化学研究',
                    'user_id': 1
                }
            ]
            
            # 插入测试数据
            for expert_data in test_experts:
                # 检查是否已存在
                existing = ExpertTalent.query.filter_by(
                    name=expert_data['name'],
                    user_id=expert_data['user_id']
                ).first()
                
                if not existing:
                    expert = ExpertTalent(**expert_data)
                    db.session.add(expert)
                    print(f"创建专家人才测试数据: {expert_data['name']}")
                else:
                    print(f"专家人才测试数据已存在: {expert_data['name']}")
            
            db.session.commit()
            print("专家人才测试数据创建完成！")
            
        except Exception as e:
            db.session.rollback()
            print(f"创建测试数据失败: {str(e)}")
            raise

if __name__ == '__main__':
    create_test_data()
