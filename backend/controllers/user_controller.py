"""
用户管理控制器
"""
from flask import Blueprint, request, jsonify
from urllib.parse import unquote
from models import User
from config.database import db
from utils.jwt_utils import token_required, hash_password, verify_password

user_bp = Blueprint('user', __name__, url_prefix='/api')

@user_bp.route('/users', methods=['GET'])
def get_users():
    """获取用户列表（支持搜索）"""
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

@user_bp.route('/users', methods=['POST'])
def create_user():
    """创建用户"""
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
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'code': 200, 'message': '创建成功', 'data': new_user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@user_bp.route('/users/<name>', methods=['PUT'])
def update_user(name):
    """更新用户"""
    try:
        decoded_name = unquote(name)
        user = User.query.filter_by(name=decoded_name).first()
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        data = request.json
        for key, value in data.items():
            if key not in ['name', 'id'] and hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@user_bp.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    """删除用户"""
    try:
        decoded_name = unquote(name)
        user = User.query.filter_by(name=decoded_name).first()
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@user_bp.route('/user/profile', methods=['GET'])
@token_required
def get_current_user_profile(current_user):
    """获取当前用户信息"""
    try:
        user_id = current_user['user_id']
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        # 不返回密码字段
        user_data = user.to_dict()
        user_data.pop('password', None)
        
        return jsonify({
            'code': 200,
            'data': user_data
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@user_bp.route('/user/profile', methods=['PUT'])
@token_required
def update_current_user_profile(current_user):
    """更新当前用户信息"""
    try:
        user_id = current_user['user_id']
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        data = request.json
        
        # 允许更新的字段
        allowed_fields = ['sex', 'department', 'email', 'phone', 'signature']
        for key, value in data.items():
            if key in allowed_fields and hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@user_bp.route('/user/change-password', methods=['PUT'])
@token_required
def change_password(current_user):
    """修改密码"""
    try:
        user_id = current_user['user_id']
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        data = request.json
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        
        if not current_password or not new_password:
            return jsonify({'code': 400, 'message': '请提供当前密码和新密码'}), 400
        
        # 验证当前密码 - 兼容明文和加密密码
        if user.password == current_password or verify_password(current_password, user.password):
            pass  # 密码正确
        else:
            return jsonify({'code': 400, 'message': '当前密码错误'}), 400
        
        # 更新密码
        user.password = hash_password(new_password)
        db.session.commit()
        
        return jsonify({'code': 200, 'message': '密码修改成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
