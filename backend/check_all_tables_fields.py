#!/usr/bin/env python3
"""
全面检查所有数据库表字段的脚本
确保所有表的字段与代码中的模型定义一致
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import db
from sqlalchemy import text
from models import user, task, expert_talent, task_unit, onboard_inspection

def get_table_schema():
    """获取数据库中所有表的字段信息"""
    try:
        # 获取所有表名
        tables_result = db.session.execute(text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = DATABASE()
        """)).fetchall()
        
        table_schemas = {}
        for table in tables_result:
            table_name = table[0]
            
            # 获取每个表的字段信息
            columns_result = db.session.execute(text(f"""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE, COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table_name}' 
                AND TABLE_SCHEMA = DATABASE()
                ORDER BY ORDINAL_POSITION
            """)).fetchall()
            
            table_schemas[table_name] = columns_result
            
        return table_schemas
    except Exception as e:
        print(f"获取数据库架构失败: {e}")
        return {}

def get_expected_fields():
    """获取代码中定义的期望字段"""
    expected_fields = {
        'tb_user': [
            {'name': 'id', 'type': 'int', 'nullable': False},
            {'name': 'name', 'type': 'varchar', 'length': 50, 'nullable': False},
            {'name': 'login_name', 'type': 'varchar', 'length': 50, 'nullable': False},
            {'name': 'password', 'type': 'varchar', 'length': 100, 'nullable': False},
            {'name': 'sex', 'type': 'varchar', 'length': 10, 'nullable': True},
            {'name': 'department', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'role', 'type': 'varchar', 'length': 20, 'nullable': True},
            {'name': 'email', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'phone', 'type': 'varchar', 'length': 20, 'nullable': True},
            {'name': 'signature', 'type': 'text', 'nullable': True},
            {'name': 'create_time', 'type': 'datetime', 'nullable': True},
            {'name': 'update_time', 'type': 'datetime', 'nullable': True}
        ],
        'tb_task_info': [
            {'name': 'task_name', 'type': 'varchar', 'length': 100, 'nullable': False},
            {'name': 'project', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'task_code', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'undertake', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'participant', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'ship', 'type': 'varchar', 'length': 45, 'nullable': True},
            {'name': 'leader', 'type': 'varchar', 'length': 45, 'nullable': True},
            {'name': 'chief_scientist', 'type': 'varchar', 'length': 45, 'nullable': True},
            {'name': 'superintendent', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'superintended', 'type': 'varchar', 'length': 45, 'nullable': True},
            {'name': 'executiontime', 'type': 'text', 'nullable': True},
            {'name': 'subject', 'type': 'varchar', 'length': 45, 'nullable': True},
            {'name': 'user_id', 'type': 'int', 'nullable': False}
        ],
        'tb_expert_talent': [
            {'name': 'id', 'type': 'int', 'nullable': False},
            {'name': 'name', 'type': 'varchar', 'length': 50, 'nullable': False},
            {'name': 'gender', 'type': 'varchar', 'length': 10, 'nullable': True},
            {'name': 'birth_date', 'type': 'date', 'nullable': True},
            {'name': 'job_title', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'work_unit', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'specialty', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'contact_info', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'id_number', 'type': 'varchar', 'length': 50, 'nullable': True},
            {'name': 'bank_card_number', 'type': 'varchar', 'length': 50, 'nullable': True},
            {'name': 'opening_bank', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'remarks', 'type': 'text', 'nullable': True},
            {'name': 'user_id', 'type': 'int', 'nullable': False},
            {'name': 'create_time', 'type': 'datetime', 'nullable': True},
            {'name': 'update_time', 'type': 'datetime', 'nullable': True}
        ],
        'tb_task_unit': [
            {'name': 'id', 'type': 'int', 'nullable': False},
            {'name': 'unit_name', 'type': 'varchar', 'length': 200, 'nullable': False},
            {'name': 'specialized_person', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'quality_manager', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'contact_person', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'contact_info', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'remarks', 'type': 'text', 'nullable': True},
            {'name': 'user_id', 'type': 'int', 'nullable': False},
            {'name': 'create_time', 'type': 'datetime', 'nullable': True},
            {'name': 'update_time', 'type': 'datetime', 'nullable': True}
        ],
        'tb_onboard_inspection': [
            {'name': 'id', 'type': 'int', 'nullable': False},
            {'name': 'task_name', 'type': 'varchar', 'length': 100, 'nullable': False},
            {'name': 'inspected_unit', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'participating_unit', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'task_code', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'chief_scientist', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'inspection_date', 'type': 'date', 'nullable': True},
            {'name': 'onboard_supervisor', 'type': 'varchar', 'length': 100, 'nullable': True},
            {'name': 'inspected_unit_personnel', 'type': 'varchar', 'length': 200, 'nullable': True},
            {'name': 'check_1', 'type': 'text', 'nullable': True},
            {'name': 'check_1_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_2', 'type': 'text', 'nullable': True},
            {'name': 'check_2_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_3', 'type': 'text', 'nullable': True},
            {'name': 'check_3_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_4', 'type': 'text', 'nullable': True},
            {'name': 'check_4_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_5', 'type': 'text', 'nullable': True},
            {'name': 'check_5_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_6', 'type': 'text', 'nullable': True},
            {'name': 'check_6_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_7', 'type': 'text', 'nullable': True},
            {'name': 'check_7_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_8', 'type': 'text', 'nullable': True},
            {'name': 'check_8_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_9', 'type': 'text', 'nullable': True},
            {'name': 'check_9_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_10', 'type': 'text', 'nullable': True},
            {'name': 'check_10_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_11', 'type': 'text', 'nullable': True},
            {'name': 'check_11_problem', 'type': 'text', 'nullable': True},
            {'name': 'check_12', 'type': 'text', 'nullable': True},
            {'name': 'check_12_problem', 'type': 'text', 'nullable': True},
            {'name': 'team_leader_sign', 'type': 'text', 'nullable': True},
            {'name': 'task_leader_sign', 'type': 'text', 'nullable': True},
            {'name': 'attachments', 'type': 'text', 'nullable': True},
            {'name': 'user_id', 'type': 'int', 'nullable': False},
            {'name': 'create_time', 'type': 'datetime', 'nullable': True},
            {'name': 'update_time', 'type': 'datetime', 'nullable': True}
        ]
    }
    return expected_fields

def check_table_fields(table_name, expected_fields, actual_fields):
    """检查单个表的字段"""
    missing_fields = []
    extra_fields = []
    
    # 检查缺失字段
    expected_field_names = {field['name'] for field in expected_fields}
    actual_field_names = {field[0] for field in actual_fields}
    
    for expected_field in expected_fields:
        field_name = expected_field['name']
        if field_name not in actual_field_names:
            missing_fields.append(expected_field)
    
    # 检查多余字段（可选，这里只记录不自动删除）
    for actual_field in actual_fields:
        field_name = actual_field[0]
        if field_name not in expected_field_names:
            extra_fields.append(actual_field)
    
    return missing_fields, extra_fields

def add_missing_field(table_name, field):
    """添加缺失字段"""
    field_name = field['name']
    field_type = field['type']
    nullable = field.get('nullable', True)
    length = field.get('length')
    
    # 构建字段定义
    if field_type == 'varchar' and length:
        type_def = f"VARCHAR({length})"
    elif field_type == 'int':
        type_def = "INT"
    elif field_type == 'text':
        type_def = "TEXT"
    elif field_type == 'datetime':
        type_def = "DATETIME"
    elif field_type == 'date':
        type_def = "DATE"
    else:
        type_def = field_type.upper()
    
    # 添加NOT NULL约束
    if not nullable:
        type_def += " NOT NULL"
    
    try:
        sql = f"ALTER TABLE {table_name} ADD COLUMN {field_name} {type_def}"
        db.session.execute(text(sql))
        return True
    except Exception as e:
        print(f"添加字段 {table_name}.{field_name} 失败: {e}")
        return False

def check_all_tables():
    """检查所有表的字段"""
    print("开始检查所有数据库表字段...")
    print("=" * 60)
    
    # 获取数据库架构
    table_schemas = get_table_schema()
    if not table_schemas:
        print("无法获取数据库架构信息")
        return False
    
    # 获取期望字段
    expected_fields = get_expected_fields()
    
    total_missing = 0
    total_added = 0
    total_extra = 0
    
    for table_name, expected_table_fields in expected_fields.items():
        if table_name not in table_schemas:
            print(f"警告: 表 {table_name} 不存在于数据库中")
            continue
        
        print(f"\n检查表: {table_name}")
        print("-" * 40)
        
        actual_fields = table_schemas[table_name]
        missing_fields, extra_fields = check_table_fields(table_name, expected_table_fields, actual_fields)
        
        # 处理缺失字段
        if missing_fields:
            print(f"发现 {len(missing_fields)} 个缺失字段:")
            for field in missing_fields:
                print(f"   - {field['name']} ({field['type']})")
                total_missing += 1
                
                # 尝试添加字段
                if add_missing_field(table_name, field):
                    print(f"   字段 {field['name']} 添加成功")
                    total_added += 1
                else:
                    print(f"   字段 {field['name']} 添加失败")
        else:
            print("所有必需字段都存在")
        
        # 报告多余字段
        if extra_fields:
            print(f"发现 {len(extra_fields)} 个额外字段:")
            for field in extra_fields:
                print(f"   - {field[0]} ({field[1]})")
                total_extra += 1
        else:
            print("没有额外字段")
    
    # 提交所有更改
    try:
        db.session.commit()
        print(f"\n数据库字段检查完成!")
        print(f"统计信息:")
        print(f"   - 缺失字段: {total_missing}")
        print(f"   - 成功添加: {total_added}")
        print(f"   - 额外字段: {total_extra}")
        return True
    except Exception as e:
        print(f"提交更改失败: {e}")
        db.session.rollback()
        return False

def run_comprehensive_check():
    """运行全面检查"""
    print("开始全面数据库字段检查...")
    success = check_all_tables()
    if success:
        print("数据库字段检查完成")
    else:
        print("数据库字段检查失败")
    return success

if __name__ == '__main__':
    # 如果直接运行此脚本
    from app import create_app
    app = create_app()
    with app.app_context():
        run_comprehensive_check()
