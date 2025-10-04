#!/usr/bin/env python3
"""
自动检测并添加用户表缺失字段的迁移脚本
在应用启动时自动执行，确保数据库字段完整性
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import db
from sqlalchemy import text

def check_and_add_user_fields():
    """检查并添加用户表缺失的字段"""
    try:
        # 需要检查的字段列表
        required_fields = [
            {'name': 'email', 'type': 'VARCHAR(100)', 'comment': '邮箱'},
            {'name': 'phone', 'type': 'VARCHAR(20)', 'comment': '电话'},
            {'name': 'signature', 'type': 'TEXT', 'comment': '手写签名'}
        ]
        
        added_fields = []
        existing_fields = []
        
        # 检查每个字段是否存在
        for field in required_fields:
            field_name = field['name']
            field_type = field['type']
            field_comment = field['comment']
            
            try:
                # 查询字段是否存在
                result = db.session.execute(text(f"""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'tb_user' 
                    AND COLUMN_NAME = '{field_name}'
                """)).fetchall()
                
                if not result:
                    print(f"检测到缺失字段 {field_name}({field_comment})，正在添加...")
                    try:
                        # 添加字段
                        db.session.execute(text(f"ALTER TABLE tb_user ADD COLUMN {field_name} {field_type}"))
                        added_fields.append(field_name)
                        print(f"✓ 字段 {field_name} 添加成功")
                    except Exception as e:
                        print(f"✗ 添加字段 {field_name} 失败: {e}")
                        continue
                else:
                    existing_fields.append(field_name)
                    print(f"✓ 字段 {field_name} 已存在，跳过")
                    
            except Exception as e:
                print(f"✗ 检查字段 {field_name} 时发生错误: {e}")
                continue
        
        # 提交所有更改
        db.session.commit()
        
        # 输出总结
        if added_fields:
            print(f"成功添加字段: {', '.join(added_fields)}")
        if existing_fields:
            print(f"已存在字段: {', '.join(existing_fields)}")
        
        print("用户表字段检查完成")
        return True
        
    except Exception as e:
        print(f"字段检查过程中发生错误: {e}")
        try:
            db.session.rollback()
        except:
            pass
        return False

def run_migration():
    """运行迁移"""
    print("开始检查用户表字段...")
    success = check_and_add_user_fields()
    if success:
        print("用户表字段迁移完成")
    else:
        print("用户表字段迁移失败")
    return success

if __name__ == '__main__':
    # 如果直接运行此脚本
    from app import create_app
    app = create_app()
    with app.app_context():
        run_migration()
