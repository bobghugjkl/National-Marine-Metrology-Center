"""
统一后端服务 - 整合所有功能
端口: 5000
"""
from flask import Flask
from flask_cors import CORS
import pymysql

# 导入共享的 db 实例
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:WASDijkl15963@localhost:3306/marine_survey_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# 首先初始化所有模型的 db
from models_task import db as task_db
from models_inspection import db as inspection_db

# 使用同一个 app 初始化
task_db.init_app(app)
inspection_db.init_app(app)

# CORS配置
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 导入并注册所有蓝图
from routes_task import task_bp
from routes_inspection import inspection_bp

# 注册蓝图
app.register_blueprint(task_bp)
app.register_blueprint(inspection_bp)

# 健康检查
@app.route('/api/health', methods=['GET'])
def health():
    from flask import jsonify
    return jsonify({
        'status': 'success', 
        'message': '统一后端服务运行正常',
        'services': ['任务管理', '检查记录']
    })

# 原有的用户登录注册等接口
from flask import request, jsonify
from urllib.parse import unquote

# ==================== 用户模型 ====================
from flask_sqlalchemy import SQLAlchemy

# 使用已经初始化的 db
db_main = task_db

class User(db_main.Model):
    __tablename__ = 'tb_user'
    name = db_main.Column(db_main.String(45), primary_key=True)
    login_name = db_main.Column(db_main.String(45))
    password = db_main.Column(db_main.String(45))
    sex = db_main.Column(db_main.String(45))
    role = db_main.Column(db_main.String(45))
    desc = db_main.Column('desc', db_main.String(45))
    permission = db_main.Column(db_main.String(45))
    department = db_main.Column(db_main.String(255))

    def to_dict(self):
        return {
            'name': self.name,
            'login_name': self.login_name,
            'password': self.password,
            'sex': self.sex,
            'role': self.role,
            'desc': self.desc,
            'permission': self.permission,
            'department': self.department
        }

# ==================== 用户管理接口 ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        name = request.args.get('name', '')
        if name:
            users = User.query.filter(User.name.like(f'%{name}%')).all()
        else:
            users = User.query.all()
        
        user_list = [u.to_dict() for u in users]
        return jsonify({
            'code': 200,
            'data': {
                'list': user_list,
                'pageTotal': len(user_list)
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        new_user = User(
            name=data.get('name'),
            login_name=data.get('login_name'),
            password=data.get('password'),
            sex=data.get('sex'),
            role=data.get('role'),
            desc=data.get('desc'),
            permission=data.get('permission'),
            department=data.get('department')
        )
        db_main.session.add(new_user)
        db_main.session.commit()
        return jsonify({'code': 200, 'message': '创建成功', 'data': new_user.to_dict()})
    except Exception as e:
        db_main.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/users/<name>', methods=['PUT'])
def update_user(name):
    try:
        decoded_name = unquote(name)
        user = User.query.get(decoded_name)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        data = request.json
        for key, value in data.items():
            if key != 'name' and hasattr(user, key):
                setattr(user, key, value)
        
        db_main.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': user.to_dict()})
    except Exception as e:
        db_main.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/users/<name>', methods=['DELETE'])
def delete_user(name):
    try:
        decoded_name = unquote(name)
        user = User.query.get(decoded_name)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        db_main.session.delete(user)
        db_main.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db_main.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

# ==================== 登录注册接口 ====================

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400

        user = User.query.filter(
            (User.name == username) | (User.login_name == username)
        ).first()

        if not user or user.password != password:
            return jsonify({'code': 401, 'message': '用户名或密码不正确'}), 401

        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'username': user.name,
                'login_name': user.login_name,
                'role': user.role,
                'department': user.department
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        login_name = data.get('login_name', username)
        department = data.get('department', '未分配')

        if not username or not password:
            return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400

        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            return jsonify({'code': 400, 'message': '用户名已存在'}), 400

        existing_login = User.query.filter_by(login_name=login_name).first()
        if existing_login:
            return jsonify({'code': 400, 'message': '登录名已存在'}), 400

        new_user = User(
            name=username,
            login_name=login_name,
            password=password,
            role='普通用户',
            department=department
        )

        db_main.session.add(new_user)
        db_main.session.commit()

        return jsonify({
            'code': 200,
            'message': '注册成功',
            'data': new_user.to_dict()
        })
    except Exception as e:
        db_main.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

if __name__ == '__main__':
    print('=' * 60)
    print('统一后端服务已启动: http://localhost:5000')
    print('提供服务:')
    print('  - 用户管理')
    print('  - 任务管理 (原端口5001)')
    print('  - 检查记录管理 (原端口5002)')
    print('=' * 60)
    app.run(debug=True, port=5000, host='0.0.0.0')
