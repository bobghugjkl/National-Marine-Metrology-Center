#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务管理后端主程序
"""

from flask import Flask
from flask_cors import CORS
import pymysql

# 安装 PyMySQL 作为 MySQLdb
pymysql.install_as_MySQLdb()

# 创建 Flask 应用
app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:WASDijkl15963@localhost:3306/marine_survey_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# 初始化数据库
from models_task import db
db.init_app(app)

# CORS 配置
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 注册任务路由
from routes_task import task_bp
app.register_blueprint(task_bp)

# 健康检查
@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'success', 'message': '任务管理后端运行正常'}

if __name__ == '__main__':
    print('任务管理后端已启动: http://localhost:5001')
    app.run(debug=True, port=5001, host='0.0.0.0')
