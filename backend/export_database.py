"""
导出当前数据库的完整 SQL 文件
"""
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='WASDijkl15963',
    database='marine_survey_db',
    charset='utf8mb4'
)
cur = conn.cursor()

sql_content = []

# 添加文件头
sql_content.append("-- ================================================")
sql_content.append("-- 海洋调查现场质量监督管理系统 - 数据库完整备份")
sql_content.append("-- 生成时间: 2025-09-30")
sql_content.append("-- 数据库名: marine_survey_db")
sql_content.append("-- ================================================\n")

sql_content.append("-- 设置字符集")
sql_content.append("SET NAMES utf8mb4;")
sql_content.append("SET FOREIGN_KEY_CHECKS = 0;\n")

# 获取所有表名
cur.execute("SHOW TABLES")
tables = [row[0] for row in cur.fetchall()]

print(f"找到 {len(tables)} 个表:")
for table in tables:
    print(f"  - {table}")

# 为每个表生成建表语句和数据
for table_name in tables:
    print(f"\n正在导出表: {table_name}")
    
    # 获取建表语句
    cur.execute(f"SHOW CREATE TABLE `{table_name}`")
    create_table = cur.fetchone()[1]
    
    sql_content.append(f"\n-- ----------------------------")
    sql_content.append(f"-- Table structure for {table_name}")
    sql_content.append(f"-- ----------------------------")
    sql_content.append(f"DROP TABLE IF EXISTS `{table_name}`;")
    sql_content.append(create_table + ";\n")
    
    # 获取表数据
    cur.execute(f"SELECT * FROM `{table_name}`")
    rows = cur.fetchall()
    
    if rows:
        # 获取列名
        cur.execute(f"DESCRIBE `{table_name}`")
        columns = [row[0] for row in cur.fetchall()]
        
        sql_content.append(f"-- ----------------------------")
        sql_content.append(f"-- Records of {table_name}")
        sql_content.append(f"-- ----------------------------")
        
        for row in rows:
            # 构建 INSERT 语句
            values = []
            for value in row:
                if value is None:
                    values.append('NULL')
                elif isinstance(value, str):
                    # 转义单引号
                    escaped_value = value.replace("'", "''")
                    values.append(f"'{escaped_value}'")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    values.append(f"'{str(value)}'")
            
            column_names = ', '.join([f'`{col}`' for col in columns])
            values_str = ', '.join(values)
            sql_content.append(f"INSERT INTO `{table_name}` ({column_names}) VALUES ({values_str});")
        
        sql_content.append("")  # 空行

sql_content.append("\nSET FOREIGN_KEY_CHECKS = 1;")

# 写入文件
output_file = 'database_backup.sql'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_content))

print(f"\n导出完成! 文件已保存到: {output_file}")
print(f"总共导出了 {len(tables)} 个表")

cur.close()
conn.close()
