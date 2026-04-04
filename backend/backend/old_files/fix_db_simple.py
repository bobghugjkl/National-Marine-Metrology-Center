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

    print("Connected to database successfully")

    # Check if user_id column exists in tb_task_hqzljdjcjlb
    cursor.execute("DESCRIBE tb_task_hqzljdjcjlb")
    columns = [row[0] for row in cursor.fetchall()]

    if 'user_id' not in columns:
        print("Adding user_id column to tb_task_hqzljdjcjlb...")
        cursor.execute("ALTER TABLE tb_task_hqzljdjcjlb ADD COLUMN user_id INT DEFAULT 3")
        print("user_id column added successfully")
    else:
        print("user_id column already exists")

    # Check if user_id column exists in tb_task_info
    cursor.execute("DESCRIBE tb_task_info")
    columns = [row[0] for row in cursor.fetchall()]

    if 'user_id' not in columns:
        print("Adding user_id column to tb_task_info...")
        cursor.execute("ALTER TABLE tb_task_info ADD COLUMN user_id INT DEFAULT 3")
        print("user_id column added successfully")
    else:
        print("user_id column already exists")

    # Update existing data
    cursor.execute("UPDATE tb_task_hqzljdjcjlb SET user_id = 3 WHERE user_id IS NULL")
    print(f"Updated {cursor.rowcount} inspection records")

    cursor.execute("UPDATE tb_task_info SET user_id = 3 WHERE user_id IS NULL")
    print(f"Updated {cursor.rowcount} task records")

    conn.commit()
    print("Database fix completed successfully!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
