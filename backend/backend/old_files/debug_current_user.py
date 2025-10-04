#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试当前用户登录状态的脚本
"""
import json

def check_current_user():
    """检查当前用户的登录状态"""
    print("=== 检查当前用户登录状态 ===")

    print("\n请在浏览器控制台执行以下命令检查localStorage:")
    print("console.log('=== localStorage 内容 ===');")
    print("console.log('token:', localStorage.getItem('token'));")
    print("console.log('vuems_name:', localStorage.getItem('vuems_name'));")
    print("console.log('vuems_user:', localStorage.getItem('vuems_user'));")
    print("console.log('userId:', localStorage.getItem('userId'));")

    print("\n请在浏览器控制台执行以下命令检查当前页面信息:")
    print("console.log('当前URL:', window.location.href);")
    print("console.log('当前路由:', window.location.hash);")

    print("\n请检查网络面板中的请求头:")
    print("1. 在Network标签中找到失败的请求")
    print("2. 查看Request Headers，确认是否有Authorization字段")
    print("3. 如果有Authorization字段，检查格式是否为 'Bearer <token>'")

    print("\n=== 手动测试步骤 ===")
    print("1. 打开浏览器开发者工具 (F12)")
    print("2. 转到 Console 标签")
    print("3. 执行上面的命令查看localStorage内容")
    print("4. 转到 Network 标签")
    print("5. 重新点击'查看检查记录'按钮")
    print("6. 查看失败请求的详细信息")

    print("\n=== 常见问题排查 ===")
    print("1. 确认您已经登录：刷新页面，重新登录")
    print("2. 检查localStorage是否有token")
    print("3. 检查请求头是否包含Authorization")
    print("4. 如果以上都正常，可能是后端问题")

if __name__ == '__main__':
    check_current_user()
