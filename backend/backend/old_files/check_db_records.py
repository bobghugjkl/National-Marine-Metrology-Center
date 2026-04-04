import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='WASDijkl15963',
        database='marine_survey_db',
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    # 查询特定检查记录
    task_name = '南海深海探测'
    cursor.execute('SELECT task_name, check_date, superintendent FROM tb_task_hqzljdjcjlb WHERE task_name = %s', (task_name,))
    result = cursor.fetchone()

    if result:
        print(f'Found inspection record: {result}')
    else:
        print(f'No inspection record found for: {task_name}')

    # 查询所有检查记录
    cursor.execute('SELECT task_name FROM tb_task_hqzljdjcjlb LIMIT 10')
    all_records = cursor.fetchall()
    print('All inspection records in database:')
    for record in all_records:
        print(f'  - {record[0]}')

    cursor.close()
    conn.close()

except Exception as e:
    print(f'Database query failed: {e}')
