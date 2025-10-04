#!/usr/bin/env python3
"""
带全面数据库检查的启动脚本
可以选择是否启用全面字段检查
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_with_full_check():
    """启动应用并执行全面数据库检查"""
    from app import create_app
    from check_all_tables_fields import run_comprehensive_check
    
    print("=" * 60)
    print("启动应用并执行全面数据库字段检查...")
    print("=" * 60)
    
    # 创建应用
    app = create_app()
    
    # 执行全面检查
    with app.app_context():
        print("\n开始执行全面数据库字段检查...")
        success = run_comprehensive_check()
        
        if success:
            print("\n数据库字段检查完成，应用启动成功!")
        else:
            print("\n数据库字段检查失败，但应用仍会启动")
    
    # 启动应用
    print("\n启动Flask应用...")
    app.run(host='0.0.0.0', port=5000, debug=True)

def start_with_user_check_only():
    """启动应用并只检查用户表字段"""
    from app import create_app
    
    print("=" * 60)
    print("启动应用并执行用户表字段检查...")
    print("=" * 60)
    
    # 创建应用（包含用户表检查）
    app = create_app()
    
    # 启动应用
    print("\n启动Flask应用...")
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--full-check':
        start_with_full_check()
    else:
        start_with_user_check_only()
