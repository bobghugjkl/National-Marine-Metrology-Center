#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库修复脚本 - 添加缺失的 user_id 字段
"""
import pymysql
import sys

def fix_database():
    """修复数据库结构，添加 user_id 字段"""
    try:
        # 连接数据库
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='WASDijkl15963',
            database='marine_survey_db',
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        print("连接数据库成功，开始修复数据库结构...")

        # 检查并添加 user_id 字段到 tb_task_hqzljdjcjlb 表
        print("\n[1] 检查 tb_task_hqzljdjcjlb 表结构...")
        cursor.execute("DESCRIBE tb_task_hqzljdjcjlb")
        columns = [row[0] for row in cursor.fetchall()]

        if 'user_id' not in columns:
            print("添加 user_id 字段到 tb_task_hqzljdjcjlb 表...")
            try:
                cursor.execute("""
                    ALTER TABLE tb_task_hqzljdjcjlb
                    ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建检查记录的用户ID'
                """)
                print("✓ user_id 字段添加成功")
            except Exception as e:
                print(f"添加字段失败（可能已存在）: {e}")
        else:
            print("✓ user_id 字段已存在")

        # 检查并添加 user_id 字段到 tb_task_info 表
        print("\n[2] 检查 tb_task_info 表结构...")
        cursor.execute("DESCRIBE tb_task_info")
        columns = [row[0] for row in cursor.fetchall()]

        if 'user_id' not in columns:
            print("添加 user_id 字段到 tb_task_info 表...")
            cursor.execute("""
                ALTER TABLE tb_task_info
                ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建任务的用户ID'
            """)
            print("✓ user_id 字段添加成功")
        else:
            print("✓ user_id 字段已存在")

        # 更新现有数据，为没有 user_id 的记录设置默认值
        print("\n[3] 更新现有数据...")
        cursor.execute("UPDATE tb_task_hqzljdjcjlb SET user_id = 3 WHERE user_id IS NULL")
        updated_rows = cursor.rowcount
        print(f"✓ 更新了 {updated_rows} 条航前检查记录")

        cursor.execute("UPDATE tb_task_info SET user_id = 3 WHERE user_id IS NULL")
        updated_rows = cursor.rowcount
        print(f"✓ 更新了 {updated_rows} 条任务记录")

        conn.commit()
        print("\n✅ 数据库修复完成！")

        # 验证修复结果
        print("\n[4] 验证修复结果...")
        cursor.execute("SELECT COUNT(*) FROM tb_task_hqzljdjcjlb WHERE user_id = 3")
        inspection_count = cursor.fetchone()[0]
        print(f"航前检查记录总数: {inspection_count}")

        cursor.execute("SELECT COUNT(*) FROM tb_task_info WHERE user_id = 3")
        task_count = cursor.fetchone()[0]
        print(f"任务记录总数: {task_count}")

    except Exception as e:
        print(f"❌ 执行失败: {e}")
        if 'conn' in locals():
            conn.rollback()
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    fix_database()
