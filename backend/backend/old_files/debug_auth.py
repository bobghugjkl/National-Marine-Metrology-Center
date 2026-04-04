#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试认证问题的脚本
"""
import requests
import json

def check_auth_status():
    """检查认证状态"""
    print("=== 调试认证问题 ===")

    # 检查localStorage中的认证信息
    print("\n1. 检查前端认证信息...")
    print("请在浏览器控制台执行以下命令检查localStorage:")
    print("console.log('token:', localStorage.getItem('token'))")
    print("console.log('userId:', localStorage.getItem('userId'))")
    print("console.log('vuems_name:', localStorage.getItem('vuems_name'))")

    # 测试后端健康检查
    print("\n2. 测试后端连接...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        print(f"后端健康检查: {response.status_code}")
        if response.status_code == 200:
            print("后端服务正常运行")
        else:
            print(f"后端服务异常: {response.text}")
    except Exception as e:
        print(f"无法连接到后端: {e}")
        return

    # 测试登录接口
    print("\n3. 测试登录接口...")
    login_data = {
        'username': 'admin',
        'password': '123456'
    }

    try:
        response = requests.post('http://localhost:5000/api/login', json=login_data, timeout=5)
        print(f"登录接口响应: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                print("登录成功")
                token = data.get('data', {}).get('token')
                if token:
                    print(f"获取到的token: {token[:50]}...")

                    # 测试带token的请求
                    print("\n4. 测试带token的API请求...")
                    headers = {'Authorization': f'Bearer {token}'}
                    test_response = requests.get('http://localhost:5000/api/tasks', headers=headers, timeout=5)
                    print(f"任务列表接口: {test_response.status_code}")

                    if test_response.status_code == 200:
                        print("认证成功，可以访问受保护的API")
                    elif test_response.status_code == 401:
                        print("认证失败，token无效")
                    else:
                        print(f"其他错误: {test_response.status_code}")
                else:
                    print("登录响应中没有token")
            else:
                print(f"登录失败: {data.get('message')}")
        else:
            print(f"登录请求失败: {response.status_code}")

    except Exception as e:
        print(f"登录测试失败: {e}")

    print("\n=== 调试步骤建议 ===")
    print("1. 请确保您已经登录（刷新页面后重新登录）")
    print("2. 检查浏览器控制台的localStorage内容")
    print("3. 查看网络面板中的请求和响应")
    print("4. 如果问题持续，请清除浏览器缓存和localStorage后重新登录")

if __name__ == '__main__':
    check_auth_status()
