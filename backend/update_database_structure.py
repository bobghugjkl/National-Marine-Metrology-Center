"""
更新数据库结构 - 添加用户隔离功能
"""
import pymysql

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'WASDijkl15963',
    'database': 'marine_survey_db',
    'charset': 'utf8mb4'
}

def execute_sql(cursor, sql, description):
    """执行 SQL 并处理错误"""
    try:
        cursor.execute(sql)
        print(f"[OK] {description}")
        return True
    except Exception as e:
        print(f"[ERROR] {description}: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("开始更新数据库结构...")
    print("=" * 60)
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        # 1. 给 tb_user 表添加自增主键 id
        print("\n[1] 修改 tb_user 表...")
        
        # 检查是否已有 id 列
        cursor.execute("SHOW COLUMNS FROM tb_user LIKE 'id'")
        if cursor.fetchone():
            print("  - id 列已存在，跳过")
        else:
            # 删除原主键
            execute_sql(cursor, "ALTER TABLE tb_user DROP PRIMARY KEY", 
                       "删除原主键 (name)")
            
            # 添加 id 列作为主键
            execute_sql(cursor, 
                       "ALTER TABLE tb_user ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST",
                       "添加 id 列作为主键")
            
            # name 列改为唯一索引
            execute_sql(cursor, 
                       "ALTER TABLE tb_user ADD UNIQUE KEY unique_name (name)",
                       "name 列设为唯一索引")
        
        # 2. 给 tb_task_info 表添加 user_id 列
        print("\n[2] 修改 tb_task_info 表...")
        cursor.execute("SHOW COLUMNS FROM tb_task_info LIKE 'user_id'")
        if cursor.fetchone():
            print("  - user_id 列已存在，跳过")
        else:
            execute_sql(cursor, 
                       "ALTER TABLE tb_task_info ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建任务的用户ID'",
                       "添加 user_id 列")
            
            # 更新现有数据
            execute_sql(cursor,
                       "UPDATE tb_task_info SET user_id = 3 WHERE user_id IS NULL",
                       "更新现有任务数据")
        
        # 3. 给 tb_task_hqzljdjcjlb 表添加 user_id 列
        print("\n[3] 修改 tb_task_hqzljdjcjlb 表...")
        cursor.execute("SHOW COLUMNS FROM tb_task_hqzljdjcjlb LIKE 'user_id'")
        if cursor.fetchone():
            print("  - user_id 列已存在，跳过")
        else:
            execute_sql(cursor,
                       "ALTER TABLE tb_task_hqzljdjcjlb ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建检查记录的用户ID'",
                       "添加 user_id 列")
            
            execute_sql(cursor,
                       "UPDATE tb_task_hqzljdjcjlb SET user_id = 3 WHERE user_id IS NULL",
                       "更新现有检查记录数据")
        
        # 4. 给 tb_base_master 表添加 user_id 列
        print("\n[4] 修改 tb_base_master 表...")
        cursor.execute("SHOW COLUMNS FROM tb_base_master LIKE 'user_id'")
        if cursor.fetchone():
            print("  - user_id 列已存在，跳过")
        else:
            execute_sql(cursor,
                       "ALTER TABLE tb_base_master ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建人员信息的用户ID'",
                       "添加 user_id 列")
            
            execute_sql(cursor,
                       "UPDATE tb_base_master SET user_id = 3 WHERE user_id IS NULL",
                       "更新现有人员数据")
        
        # 提交事务
        conn.commit()
        
        print("\n" + "=" * 60)
        print("数据库结构更新完成!")
        print("=" * 60)
        
        # 查看 tb_user 表的结构
        print("\n[验证] tb_user 表结构:")
        cursor.execute("DESC tb_user")
        for row in cursor.fetchall():
            print(f"  {row}")
        
        # 查看用户数据
        print("\n[验证] 用户数据 (前5条):")
        cursor.execute("SELECT id, name, login_name, role FROM tb_user LIMIT 5")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, Name: {row[1]}, Login: {row[2]}, Role: {row[3]}")
            
    except Exception as e:
        print(f"\n错误: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
