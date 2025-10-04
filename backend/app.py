"""
Flask 应用启动入口
统一后端服务 - 端口 5000
"""
from flask import Flask, jsonify
from config.database import init_db
from config.cors import init_cors
from controllers import user_bp, task_bp, inspection_bp, auth_bp, personnel_bp, equipment_bp, investigation_bp, voyage_personnel_bp, voyage_equipment_bp, voyage_investigation_bp, supervisor_log_bp, original_records_bp, procedure_execution_bp, work_log_bp, sample_storage_bp, post_inspection_bp, pre_summary_bp, onboard_inspection_bp, expert_talent_bp, task_unit_bp, investigation_personnel_bp, equipment_management_bp

def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # 设置JSON编码，确保中文字符正确显示
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    # 初始化数据库
    init_db(app)

    # 自动检查并添加用户表缺失字段
    with app.app_context():
        from auto_migrate_user_fields import run_migration
        run_migration()
    
    # 全面检查所有表字段（可选，根据需要启用）
    # with app.app_context():
    #     from check_all_tables_fields import run_comprehensive_check
    #     run_comprehensive_check()

    # 初始化 CORS
    init_cors(app)
    
    # 注册蓝图（路由）
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(inspection_bp)
    app.register_blueprint(personnel_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(investigation_bp)
    app.register_blueprint(voyage_personnel_bp)
    app.register_blueprint(voyage_equipment_bp)
    app.register_blueprint(voyage_investigation_bp)
    app.register_blueprint(supervisor_log_bp)
    app.register_blueprint(original_records_bp)
    app.register_blueprint(procedure_execution_bp)
    app.register_blueprint(work_log_bp)
    app.register_blueprint(sample_storage_bp)
    app.register_blueprint(post_inspection_bp)
    app.register_blueprint(pre_summary_bp)
    app.register_blueprint(onboard_inspection_bp)
    app.register_blueprint(expert_talent_bp)
    app.register_blueprint(task_unit_bp)
    app.register_blueprint(investigation_personnel_bp)
    app.register_blueprint(equipment_management_bp)
    
    # 健康检查接口
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'code': 200,
            'message': '服务运行正常',
            'service': '统一后端服务',
            'port': 5000
        })
    
    # 欢迎页面
    @app.route('/', methods=['GET'])
    def index():
        return '''
        <html>
        <head><title>海洋调查管理系统 - 后端服务</title></head>
        <body>
            <h1>🌊 海洋调查管理系统 - 后端服务</h1>
            <h2>服务状态：运行中 ✅</h2>
            <h3>可用接口：</h3>
            <ul>
                <li><a href="/api/health">/api/health</a> - 健康检查</li>
                <li>/api/users - 用户管理 (GET, POST, PUT, DELETE)</li>
                <li>/api/login - 登录</li>
                <li>/api/register - 注册</li>
                <li>/api/tasks - 任务管理 (GET, POST, PUT, DELETE)</li>
                <li>/api/inspections - 检查记录管理 (GET, PUT)</li>
            </ul>
            <hr>
            <p>📚 MVC 架构说明：</p>
            <ul>
                <li><b>models/</b> - 数据模型层</li>
                <li><b>controllers/</b> - 控制器层（业务逻辑）</li>
                <li><b>config/</b> - 配置层</li>
                <li><b>app.py</b> - 启动入口</li>
            </ul>
        </body>
        </html>
        '''
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("[启动] 统一后端服务正在启动...")
    print("[地址] 服务地址: http://localhost:5000")
    print("[架构] 架构模式: MVC + JWT认证")
    print("=" * 60)
    print("\n提供的服务:")
    print("  - 用户管理 (/api/users)")
    print("  - 登录注册 (/api/login, /api/register) - 返回JWT Token")
    print("  - 任务管理 (/api/tasks) - 需要JWT认证")
    print("  - 检查记录管理 (/api/inspections) - 需要JWT认证")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)