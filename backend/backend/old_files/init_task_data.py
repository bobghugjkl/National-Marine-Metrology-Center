#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化任务数据
"""

import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='WASDijkl15963',
        database='marine_survey_db',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    # 插入初始任务数据
    tasks = [
        ('东海海洋调查', '海洋资源调查专项', 'HY2025001', '国家海洋标准计量中心', '', '向阳红01', '张主任', '', '', '', '2025-01-15 至 2025-02-20', '海洋地质'),
        ('南海深海探测', '深海科考专项', 'HY2025002', '中国海洋大学', '', '科学号', '李教授', '', '', '', '2025-03-01 至 2025-04-15', '海洋生物'),
        ('渤海环境监测', '海洋环境保护专项', 'HY2025003', '海洋环境监测中心', '', '海巡01', '王工程师', '', '', '', '2025-05-10 至 2025-06-20', '海洋化学'),
    ]
    
    for task in tasks:
        try:
            cursor.execute("""
                INSERT INTO tb_task_info 
                (task_name, project, task_code, undertake, participant, ship, leader, chief_scientist, superintendent, superintended, executiontime, subject)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE task_name=task_name
            """, task)
        except Exception as e:
            print(f'Error inserting task {task[0]}: {e}')
    
    conn.commit()
    print('Initial task data added successfully')
    
    # 查询并显示
    cursor.execute('SELECT task_name, project, leader FROM tb_task_info')
    rows = cursor.fetchall()
    print('\nCurrent tasks:')
    for row in rows:
        print(f'  - {row[0]} ({row[1]}) - {row[2]}')
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')
