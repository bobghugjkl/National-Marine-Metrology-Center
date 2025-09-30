"""
Flask 应用启动入口
统一后端服务 - 端口 5000
"""
from flask import Flask, jsonify
from config.database import init_db
from config.cors import init_cors
from controllers import user_bp, task_bp, inspection_bp, auth_bp

def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    
    # 初始化数据库
    init_db(app)
    
    # 初始化 CORS
    init_cors(app)
    
    # 注册蓝图（路由）
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(inspection_bp)
    
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
    print("🚀 统一后端服务正在启动...")
    print("📍 服务地址: http://localhost:5000")
    print("📂 架构模式: MVC")
    print("=" * 60)
    print("\n提供的服务:")
    print("  - 用户管理 (/api/users)")
    print("  - 登录注册 (/api/login, /api/register)")
    print("  - 任务管理 (/api/tasks)")
    print("  - 检查记录管理 (/api/inspections)")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)