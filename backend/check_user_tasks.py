import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='WASDijkl15963',
    database='marine_survey_db'
)
cur = conn.cursor()

print("=" * 60)
print("用户 1234 的信息:")
cur.execute("SELECT id, name FROM tb_user WHERE name='1234'")
user_info = cur.fetchone()
if user_info:
    print(f"  ID: {user_info[0]}, Name: {user_info[1]}")
else:
    print("  用户不存在")

print("\n所有任务的 user_id:")
cur.execute("SELECT task_name, user_id FROM tb_task_info")
for row in cur.fetchall():
    print(f"  任务: {row[0][:20]}... -> user_id={row[1]}")

print("\nuser_id=12 的任务:")
cur.execute("SELECT task_name FROM tb_task_info WHERE user_id=12")
tasks = cur.fetchall()
if tasks:
    for row in tasks:
        print(f"  - {row[0]}")
else:
    print("  (无)")

print("=" * 60)

cur.close()
conn.close()
