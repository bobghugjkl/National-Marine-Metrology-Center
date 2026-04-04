"""
认证控制器（登录、注册）
"""
from flask import Blueprint, request, jsonify
from models import User
from config.database import db
from utils.jwt_utils import generate_token, verify_password

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录（使用JWT认证）"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400

        user = User.query.filter(
            (User.name == username) | (User.login_name == username)
        ).first()

        # 兼容明文和加密密码验证
        if not user or (user.password != password and not verify_password(password, user.password)):
            return jsonify({'code': 401, 'message': '用户名或密码不正确'}), 401

        # 生成 JWT token
        token = generate_token(user.id, user.name, user.role)

        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'id': user.id,
                'username': user.name,
                'login_name': user.login_name,
                'role': user.role,
                'department': user.department,
                'token': token  # 返回 token
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
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
            sex='未知',
            role='普通用户',
            desc='',
            permission='基础权限',
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
