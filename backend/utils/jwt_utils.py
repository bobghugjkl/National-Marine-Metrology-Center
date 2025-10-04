"""
JWT 工具函数
用于生成和验证 JWT token
"""
import jwt
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# JWT 密钥（生产环境应使用环境变量）
SECRET_KEY = 'your-secret-key-change-in-production'
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_HOURS = 24 * 7  # token 有效期（7天）

def generate_token(user_id: int, username: str, role: str) -> str:
    """
    生成 JWT token
    
    Args:
        user_id: 用户ID
        username: 用户名
        role: 用户角色
        
    Returns:
        JWT token 字符串
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),  # 过期时间
        'iat': datetime.utcnow()  # 签发时间
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    """
    验证 JWT token
    
    Args:
        token: JWT token 字符串
        
    Returns:
        解析后的 payload 字典，包含 user_id, username, role
        
    Raises:
        jwt.ExpiredSignatureError: token 已过期
        jwt.InvalidTokenError: token 无效
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token已过期，请重新登录')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Token无效')

def token_required(f):
    """
    装饰器：要求请求必须携带有效的 token
    
    用法：
        @task_bp.route('/tasks', methods=['GET'])
        @token_required
        def get_tasks(current_user):
            # current_user 包含 user_id, username, role
            user_id = current_user['user_id']
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头获取 token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            print(f'收到Authorization头: {auth_header[:50]}...')
            # 格式：Bearer <token>
            try:
                token = auth_header.split(' ')[1]
                print(f'提取的token: {token[:50]}...')
            except IndexError:
                print('Token格式错误：无法分割Authorization头')
                return jsonify({'code': 401, 'message': 'Token格式错误'}), 401
        else:
            print('未找到Authorization头')
            print(f'所有请求头: {dict(request.headers)}')
        
        if not token:
            print('Token为空')
            return jsonify({'code': 401, 'message': '未提供Token，请先登录'}), 401
        
        try:
            # 验证 token
            print(f'开始验证token...')
            current_user = verify_token(token)
            print(f'Token验证成功，用户: {current_user}')
            # 将用户信息传递给路由函数
            return f(current_user, *args, **kwargs)
        except jwt.ExpiredSignatureError as e:
            print(f'Token已过期: {e}')
            return jsonify({'code': 401, 'message': 'Token已过期，请重新登录'}), 401
        except jwt.InvalidTokenError as e:
            print(f'Token无效: {e}')
            return jsonify({'code': 401, 'message': 'Token无效'}), 401
        except Exception as e:
            print(f'Token验证时发生未知错误: {e}')
            import traceback
            print(f'错误详情: {traceback.format_exc()}')
            return jsonify({'code': 401, 'message': f'Token验证失败: {str(e)}'}), 401
    
    return decorated

def hash_password(password: str) -> str:
    """
    对密码进行哈希加密
    
    Args:
        password: 原始密码
        
    Returns:
        加密后的密码字符串
    """
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    Args:
        password: 原始密码
        hashed_password: 加密后的密码
        
    Returns:
        密码是否正确
    """
    return hash_password(password) == hashed_password

