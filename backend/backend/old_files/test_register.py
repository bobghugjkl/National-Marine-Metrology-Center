#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
注册功能测试脚本
"""

import requests
import pymysql

def test_register():
    """测试注册新用户"""
    print("=" * 50)
    print("测试用户注册功能")
    print("=" * 50)
    
    # 测试数据
    test_user = {
        'username': '李四',
        'password': '123456'
    }
    
    # 1. 发送注册请求
    print(f"\n1. 注册新用户: {test_user['username']}")
    response = requests.post(
        'http://localhost:5000/api/register',
        json=test_user
    )
    
    result = response.json()
    print(f"   状态码: {response.status_code}")
    print(f"   返回消息: {result.get('message', 'N/A')}")
    
    if response.status_code == 200:
        print("   ✅ 注册成功！")
        print(f"   用户信息: {result['data']}")
    else:
        print(f"   ❌ 注册失败: {result.get('message', '未知错误')}")
        return
    
    # 2. 验证数据库
    print(f"\n2. 验证数据库中的数据")
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='WASDijkl15963',
            database='marine_survey_db',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # 查询新注册的用户
        cursor.execute(
            "SELECT name, login_name, password, role, department FROM tb_user WHERE name=%s",
            (test_user['username'],)
        )
        user_data = cursor.fetchone()
        
        if user_data:
            print("   ✅ 数据库中找到用户:")
            print(f"      用户名: {user_data[0]}")
            print(f"      登录名: {user_data[1]}")
            print(f"      密码: {user_data[2]}")
            print(f"      角色: {user_data[3]}")
            print(f"      部门: {user_data[4]}")
        else:
            print("   ❌ 数据库中未找到用户")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"   ❌ 数据库查询失败: {e}")
    
    # 3. 测试登录
    print(f"\n3. 使用新账号登录")
    login_response = requests.post(
        'http://localhost:5000/api/login',
        json={
            'username': test_user['username'],
            'password': test_user['password']
        }
    )
    
    login_result = login_response.json()
    if login_response.status_code == 200:
        print(f"   ✅ 登录成功！")
        print(f"   用户信息: {login_result['data']}")
    else:
        print(f"   ❌ 登录失败: {login_result.get('message', '未知错误')}")
    
    # 4. 测试重复注册
    print(f"\n4. 测试重复注册（应该失败）")
    duplicate_response = requests.post(
        'http://localhost:5000/api/register',
        json=test_user
    )
    
    duplicate_result = duplicate_response.json()
    if duplicate_response.status_code == 400:
        print(f"   ✅ 正确拒绝重复注册")
        print(f"   错误消息: {duplicate_result.get('message', 'N/A')}")
    else:
        print(f"   ❌ 应该拒绝重复注册，但状态码是: {duplicate_response.status_code}")
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)

if __name__ == '__main__':
    test_register()
