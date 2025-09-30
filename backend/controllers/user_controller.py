"""
用户管理控制器
"""
from flask import Blueprint, request, jsonify
from urllib.parse import unquote
from models import User
from config.database import db

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
