"""
为现有任务自动创建空的检查记录
"""
import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'WASDijkl15963',
    'database': 'marine_survey_db',
    'charset': 'utf8mb4'
}

def init_inspection_records():
    """为所有现有任务创建空的检查记录"""
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()
        
        # 获取所有任务名称
        cur.execute('SELECT task_name FROM tb_task_info')
        tasks = cur.fetchall()
        
        # 为每个任务创建检查记录（如果不存在）
        for (task_name,) in tasks:
            # 检查是否已存在
            cur.execute('SELECT task_name FROM tb_task_hqzljdjcjlb WHERE task_name = %s', (task_name,))
            existing = cur.fetchone()
            
            if not existing:
                # 创建空记录
                sql = '''
                INSERT INTO tb_task_hqzljdjcjlb (task_name) 
                VALUES (%s)
                '''
                cur.execute(sql, (task_name,))
                print(f'已为任务 "{task_name}" 创建检查记录')
            else:
                print(f'任务 "{task_name}" 的检查记录已存在')
        
        conn.commit()
        print('\n初始化完成！')
        
    except pymysql.Error as e:
        print(f'错误: {e}')
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_inspection_records()
