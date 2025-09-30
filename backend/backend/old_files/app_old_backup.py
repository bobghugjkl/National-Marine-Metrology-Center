from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:WASDijkl15963@localhost:3306/marine_survey_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

# CORS 配置 - 允许所有来源和方法
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 用户模型
class User(db.Model):
    __tablename__ = 'tb_user'
    name = db.Column(db.String(45), primary_key=True)
    login_name = db.Column(db.String(45))
    password = db.Column(db.String(45))
    sex = db.Column(db.String(45))
    role = db.Column(db.String(45))
    desc = db.Column('desc', db.String(45))
    permission = db.Column(db.String(45))
    department = db.Column(db.String(255))

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

# 任务模型
class TaskInfo(db.Model):
    __tablename__ = 'tb_task_info'
    task_name = db.Column(db.String(100), primary_key=True)
    project = db.Column(db.String(100))
    task_code = db.Column(db.String(100))
    undertake = db.Column(db.String(100))
    participant = db.Column(db.String(200))
    ship = db.Column(db.String(45))
    leader = db.Column(db.String(45))
    chief_scientist = db.Column(db.String(45))
    superintendent = db.Column(db.String(100))
    superintended = db.Column(db.String(45))
    executiontime = db.Column(db.Text)
    subject = db.Column(db.String(45))

    def to_dict(self):
        return {
            'task_name': self.task_name,
            'project': self.project,
            'task_code': self.task_code,
            'undertake': self.undertake,
            'participant': self.participant,
            'ship': self.ship,
            'leader': self.leader,
            'chief_scientist': self.chief_scientist,
            'superintendent': self.superintendent,
            'superintended': self.superintended,
            'executiontime': self.executiontime,
            'subject': self.subject
        }

# 基础人员模型
class BaseMaster(db.Model):
    __tablename__ = 'tb_base_master'
    id_card_number = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(40))
    sex = db.Column(db.String(4))
    birthday = db.Column(db.Date)
    title = db.Column(db.String(45))
    organization = db.Column(db.String(45))
    major = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    band_card_number = db.Column(db.String(45))
    opening_band = db.Column(db.String(45))
    remark = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id_card_number': self.id_card_number,
            'name': self.name,
            'sex': self.sex,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'title': self.title,
            'organization': self.organization,
            'major': self.major,
            'phone': self.phone,
            'band_card_number': self.band_card_number,
            'opening_band': self.opening_band,
            'remark': self.remark
        }

# 健康检查
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'success', 'message': 'Flask后端运行正常'})

# 用户管理
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # 获取搜索参数
        name = request.args.get('name', '')
        
        # 如果有搜索条件，则按用户名模糊搜索
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
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return jsonify({'code': 200, 'message': '创建成功', 'data': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/users/<name>', methods=['PUT'])
def update_user(name):
    try:
        user = User.query.get(name)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        data = request.json
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/users/<name>', methods=['DELETE'])
def delete_user(name):
    try:
        user = User.query.get(name)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

# 任务管理
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = TaskInfo.query.all()
        task_list = [t.to_dict() for t in tasks]
        return jsonify({
            'code': 200,
            'data': {
                'list': task_list,
                'pageTotal': len(task_list)
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        task = TaskInfo(**data)
        db.session.add(task)
        db.session.commit()
        return jsonify({'code': 200, 'message': '创建成功', 'data': task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/tasks/<task_name>', methods=['PUT'])
def update_task(task_name):
    try:
        task = TaskInfo.query.get(task_name)
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        data = request.json
        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/tasks/<task_name>', methods=['DELETE'])
def delete_task(task_name):
    try:
        task = TaskInfo.query.get(task_name)
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

# 基础人员管理
@app.route('/api/masters', methods=['GET'])
def get_masters():
    try:
        masters = BaseMaster.query.all()
        master_list = [m.to_dict() for m in masters]
        return jsonify({
            'code': 200,
            'data': {
                'list': master_list,
                'pageTotal': len(master_list)
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/masters', methods=['POST'])
def create_master():
    try:
        data = request.json
        if 'birthday' in data and isinstance(data['birthday'], str):
            data['birthday'] = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
        master = BaseMaster(**data)
        db.session.add(master)
        db.session.commit()
        return jsonify({'code': 200, 'message': '创建成功', 'data': master.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/masters/<id_card_number>', methods=['PUT'])
def update_master(id_card_number):
    try:
        master = BaseMaster.query.get(id_card_number)
        if not master:
            return jsonify({'code': 404, 'message': '人员不存在'}), 404
        data = request.json
        if 'birthday' in data and isinstance(data['birthday'], str):
            data['birthday'] = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
        for key, value in data.items():
            if hasattr(master, key):
                setattr(master, key, value)
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': master.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/masters/<id_card_number>', methods=['DELETE'])
def delete_master(id_card_number):
    try:
        master = BaseMaster.query.get(id_card_number)
        if not master:
            return jsonify({'code': 404, 'message': '人员不存在'}), 404
        db.session.delete(master)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

# 角色数据（兼容前端）
@app.route('/api/roles', methods=['GET'])
def get_roles():
    return jsonify({
        'code': 200,
        'data': {
            'list': [],
            'pageTotal': 0
        }
    })

# ==================== 登录注册接口 ====================

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400
        
        # 查找用户（可以用用户名或登录名登录）
        user = User.query.filter(
            (User.name == username) | (User.login_name == username)
        ).first()
        
        # 统一错误提示（更安全，不泄露用户是否存在）
        if not user or user.password != password:
            return jsonify({'code': 401, 'message': '用户名或密码不正确'}), 401
        
        # 登录成功，返回用户信息
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

# 注册接口
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        login_name = data.get('login_name', username)  # 如果没有提供登录名，使用用户名
        department = data.get('department', '未分配')
        
        if not username or not password:
            return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            return jsonify({'code': 400, 'message': '用户名已存在'}), 400
        
        # 检查登录名是否已存在
        existing_login = User.query.filter_by(login_name=login_name).first()
        if existing_login:
            return jsonify({'code': 400, 'message': '登录名已存在'}), 400
        
        # 创建新用户
        new_user = User(
            name=username,
            login_name=login_name,
            password=password,
            role='普通用户',
            department=department
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '注册成功',
            'data': new_user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

if __name__ == '__main__':
    print('Flask后端已启动: http://localhost:5000')
    app.run(debug=True, port=5000, host='0.0.0.0')