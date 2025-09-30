"""
API 测试脚本
测试所有的增删改查功能
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"[测试] {title}")
    print(f"{'='*60}")
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except:
        print(f"响应内容: {response.text}")

def test_health():
    """测试健康检查"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("健康检查", response)

def test_users():
    """测试用户管理"""
    # 1. 获取所有用户
    response = requests.get(f"{BASE_URL}/users")
    print_response("获取所有用户", response)
    
    # 2. 创建新用户
    new_user = {
        "name": "新用户",
        "login_name": "newuser",
        "password": "123456",
        "role": "测试角色",
        "department": "测试部门",
        "sex": "男"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    print_response("创建新用户", response)
    
    # 3. 更新用户
    update_data = {
        "role": "更新后的角色",
        "department": "更新后的部门"
    }
    response = requests.put(f"{BASE_URL}/users/新用户", json=update_data)
    print_response("更新用户", response)
    
    # 4. 删除用户
    response = requests.delete(f"{BASE_URL}/users/新用户")
    print_response("删除用户", response)

def test_tasks():
    """测试任务管理"""
    # 1. 获取所有任务
    response = requests.get(f"{BASE_URL}/tasks")
    print_response("获取所有任务", response)
    
    # 2. 创建新任务
    new_task = {
        "task_name": "测试任务003",
        "project": "测试项目",
        "task_code": "TEST003",
        "undertake": "测试单位",
        "ship": "测试号",
        "leader": "测试负责人"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    print_response("创建新任务", response)
    
    # 3. 更新任务
    update_data = {
        "project": "更新后的项目",
        "ship": "更新后的船只"
    }
    response = requests.put(f"{BASE_URL}/tasks/测试任务003", json=update_data)
    print_response("更新任务", response)
    
    # 4. 删除任务
    response = requests.delete(f"{BASE_URL}/tasks/测试任务003")
    print_response("删除任务", response)

def test_masters():
    """测试基础人员管理"""
    # 1. 获取所有基础人员
    response = requests.get(f"{BASE_URL}/masters")
    print_response("获取所有基础人员", response)
    
    # 2. 创建新基础人员
    new_master = {
        "id_card_number": "110101199001011111",
        "name": "测试人员",
        "sex": "女",
        "birthday": "1990-01-01",
        "title": "测试职称",
        "organization": "测试机构",
        "phone": "13800138888"
    }
    response = requests.post(f"{BASE_URL}/masters", json=new_master)
    print_response("创建新基础人员", response)
    
    # 3. 更新基础人员
    update_data = {
        "title": "更新后的职称",
        "organization": "更新后的机构"
    }
    response = requests.put(f"{BASE_URL}/masters/110101199001011111", json=update_data)
    print_response("更新基础人员", response)
    
    # 4. 删除基础人员
    response = requests.delete(f"{BASE_URL}/masters/110101199001011111")
    print_response("删除基础人员", response)

if __name__ == "__main__":
    print("\n" + "开始 API 测试".center(60, "="))
    
    # 健康检查
    test_health()
    
    # 用户管理测试
    print("\n\n" + "用户管理测试".center(60, "="))
    test_users()
    
    # 任务管理测试
    print("\n\n" + "任务管理测试".center(60, "="))
    test_tasks()
    
    # 基础人员管理测试
    print("\n\n" + "基础人员管理测试".center(60, "="))
    test_masters()
    
    print("\n\n" + "测试完成".center(60, "=") + "\n")
