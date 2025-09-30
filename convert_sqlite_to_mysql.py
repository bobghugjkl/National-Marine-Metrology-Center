#!/usr/bin/env python3
"""
SQLite 转 MySQL 转换脚本
读取 SQLite 数据库并生成 MySQL SQL 文件
"""

import sqlite3
import json
from datetime import datetime

def sqlite_to_mysql():
    """将 SQLite 数据库转换为 MySQL SQL 文件"""

    # 连接 SQLite 数据库
    sqlite_conn = sqlite3.connect(r'e:\OtherProoject\HaiYangDiaoChaXianChangZhiLiangJianDuGuanLi\config\sqlite.db')
    sqlite_cursor = sqlite_conn.cursor()

    # 获取所有表名
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()

    mysql_sql = []
    mysql_sql.append("-- MySQL SQL 文件")
    mysql_sql.append("-- 从 SQLite 数据库转换而来")
    mysql_sql.append(f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    mysql_sql.append("")
    mysql_sql.append("-- 删除已存在的数据库（可选）")
    mysql_sql.append("DROP DATABASE IF EXISTS marine_survey_db;")
    mysql_sql.append("CREATE DATABASE marine_survey_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    mysql_sql.append("USE marine_survey_db;")
    mysql_sql.append("")

    for table in tables:
        table_name = table[0]
        if table_name.startswith('sqlite_') or table_name == 'tb_base_danwei':
            continue  # 跳过系统表

        print(f"处理表: {table_name}")

        # 获取表结构
        sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
        columns = sqlite_cursor.fetchall()

        # 生成建表语句
        mysql_columns = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            nullable = col[3]
            default_value = col[4]
            primary_key = col[5]

            # 转换数据类型
            if col_type == 'INTEGER':
                if primary_key:
                    mysql_type = 'INT AUTO_INCREMENT'
                else:
                    mysql_type = 'INT'
            elif col_type == 'REAL':
                mysql_type = 'FLOAT'
            elif col_type == 'TEXT':
                mysql_type = 'TEXT'
            elif col_type == 'BLOB':
                mysql_type = 'LONGBLOB'
            elif col_type.startswith('VARCHAR'):
                mysql_type = col_type  # 保持原样
            elif col_type == 'DATE':
                mysql_type = 'DATE'
            elif col_type == 'DATETIME':
                mysql_type = 'DATETIME'
            else:
                mysql_type = 'VARCHAR(255)'  # 默认类型

            col_def = f"    `{col_name}` {mysql_type}"

            if primary_key:
                col_def += " PRIMARY KEY"
            if not nullable:
                col_def += " NOT NULL"
            if default_value is not None:
                if col_type in ['TEXT', 'DATE', 'DATETIME']:
                    col_def += f" DEFAULT '{default_value}'"
                else:
                    col_def += f" DEFAULT {default_value}"

            mysql_columns.append(col_def)

        # 建表语句
        create_table_sql = f"CREATE TABLE `{table_name}` (\n" + ",\n".join(mysql_columns) + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
        mysql_sql.append(create_table_sql)
        mysql_sql.append("")

        # 获取表数据
        sqlite_cursor.execute(f"SELECT * FROM {table_name};")
        rows = sqlite_cursor.fetchall()

        if rows:
            # 生成插入语句
            column_names = [col[1] for col in columns]
            insert_sql = f"INSERT INTO `{table_name}` (`" + "`, `".join(column_names) + "`) VALUES"

            values = []
            for row in rows:
                # 处理数据中的特殊字符
                formatted_values = []
                for i, value in enumerate(row):
                    if value is None:
                        formatted_values.append('NULL')
                    elif columns[i][2] in ['TEXT', 'DATE', 'DATETIME', 'VARCHAR']:
                        # 转义单引号
                        escaped_value = str(value).replace("'", "''")
                        formatted_values.append(f"'{escaped_value}'")
                    else:
                        formatted_values.append(str(value))

                values.append(f"({', '.join(formatted_values)})")

            if values:
                full_insert_sql = insert_sql + "\n" + ",\n".join(values) + ";"
                mysql_sql.append(full_insert_sql)
                mysql_sql.append("")

    # 关闭连接
    sqlite_cursor.close()
    sqlite_conn.close()

    # 写入文件
    with open('mysql_from_sqlite.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(mysql_sql))

    print("转换完成！")
    print("生成文件: mysql_from_sqlite.sql")
    print(f"转换了 {len(tables)} 个表")

if __name__ == '__main__':
    sqlite_to_mysql()
