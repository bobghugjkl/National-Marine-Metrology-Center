#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建数据库表
"""

from app import create_app
from config.database import db
from models.voyage_personnel import VoyagePersonnel

def create_tables():
    """创建数据库表"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建所有表
            db.create_all()
            print("数据库表创建完成！")
            
            # 检查表是否存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"当前数据库中的表: {tables}")
            
            if 'tb_voyage_personnel' in tables:
                print("✅ tb_voyage_personnel 表已创建")
            else:
                print("❌ tb_voyage_personnel 表未创建")
                
        except Exception as e:
            print(f"创建数据库表失败: {str(e)}")

if __name__ == '__main__':
    create_tables()
