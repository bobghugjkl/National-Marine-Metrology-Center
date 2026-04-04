import pymysql
import jwt

# JWT配置（与后端保持一致）
SECRET_KEY = 'your-secret-key-change-in-production'
ALGORITHM = 'HS256'

def test_db_connection():
    """测试数据库连接"""
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

        # 测试查询航前检查记录
        cursor.execute("SELECT * FROM tb_task_hqzljdjcjlb WHERE task_name = '南海深海探测'")
        result = cursor.fetchone()

        if result:
            print(f"找到检查记录: {result[0]}")
        else:
            print("未找到指定的检查记录")

        # 测试查询任务记录
        cursor.execute("SELECT * FROM tb_task_info WHERE task_name = '南海深海探测'")
        result = cursor.fetchone()

        if result:
            print(f"找到任务记录: {result[0]}")
        else:
            print("未找到指定的任务记录")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

def test_jwt_token():
    """测试JWT token生成和验证"""
    try:
        payload = {
            'user_id': 3,
            'username': 'test_user',
            'role': '管理员',
            'exp': 9999999999,  # 很远的过期时间
            'iat': 9999999999
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        print(f"生成的token: {token}")

        # 验证token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"解码后的token: {decoded}")

        return True
    except Exception as e:
        print(f"JWT测试失败: {e}")
        return False

if __name__ == '__main__':
    print("测试数据库连接...")
    db_ok = test_db_connection()

    print("\n测试JWT token...")
    jwt_ok = test_jwt_token()

    if db_ok and jwt_ok:
        print("\n所有测试通过！")
    else:
        print("\n某些测试失败，请检查配置。")
