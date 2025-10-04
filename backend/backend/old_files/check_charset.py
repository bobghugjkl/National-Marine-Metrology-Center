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

    # 检查数据库字符集
    cursor.execute('SHOW VARIABLES LIKE \'%character_set%\'')
    charset_vars = cursor.fetchall()
    print('Database charset variables:')
    for var in charset_vars:
        print(f'  {var[0]}: {var[1]}')

    # 检查表字符集
    cursor.execute('SHOW CREATE TABLE tb_task_hqzljdjcjlb')
    result = cursor.fetchone()
    print('\nTable create statement:')
    print(result[1])

    cursor.close()
    conn.close()

except Exception as e:
    print(f'Query failed: {e}')
