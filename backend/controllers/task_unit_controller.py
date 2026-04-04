"""
任务单位控制器
"""
from flask import Blueprint, request, jsonify, current_app
from config.database import db
from models.task_unit import TaskUnit
from utils.jwt_utils import verify_token
import json

task_unit_bp = Blueprint('task_unit', __name__, url_prefix='/api')

def handle_preflight():
    """处理CORS预检请求"""
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://127.0.0.1:5173']:
        response = jsonify({'message': 'OK'})
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    return jsonify({'message': 'OK'})

@task_unit_bp.before_request
def handle_preflight_request():
    if request.method == 'OPTIONS':
        return handle_preflight()

@task_unit_bp.route('/task-unit', methods=['GET'])
def get_task_unit_list():
    """获取任务单位列表"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'message': '未提供有效的认证令牌'}), 401
        
        token = token[7:]  # 移除 'Bearer ' 前缀
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'message': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'message': '用户ID无效'}), 401
        
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        unit_name = request.args.get('unit_name', '').strip()
        
        # 构建查询
        query = TaskUnit.query.filter_by(user_id=user_id)
        
        # 应用筛选条件
        if unit_name:
            query = query.filter(TaskUnit.unit_name.like(f'%{unit_name}%'))
        
        # 分页
        total = query.count()
        units = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'list': [unit.to_dict() for unit in units],
                'total': total,
                'page': page,
                'page_size': page_size
            }
        })
        
    except Exception as e:
        current_app.logger.error(f'获取任务单位列表失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@task_unit_bp.route('/task-unit', methods=['POST'])
def create_task_unit():
    """创建任务单位"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'message': '未提供有效的认证令牌'}), 401
        
        token = token[7:]  # 移除 'Bearer ' 前缀
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'message': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'message': '用户ID无效'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        # 检查必填字段
        if not data.get('unit_name'):
            return jsonify({'code': 400, 'message': '单位名称不能为空'}), 400
        
        # 创建任务单位记录
        unit = TaskUnit(
            unit_name=data.get('unit_name'),
            specialized_person=data.get('specialized_person', ''),
            quality_manager=data.get('quality_manager', ''),
            contact_person=data.get('contact_person', ''),
            contact_info=data.get('contact_info', ''),
            remarks=data.get('remarks', ''),
            user_id=user_id
        )
        
        db.session.add(unit)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '创建成功',
            'data': unit.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'创建任务单位失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@task_unit_bp.route('/task-unit/<int:unit_id>', methods=['PUT'])
def update_task_unit(unit_id):
    """更新任务单位"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'message': '未提供有效的认证令牌'}), 401
        
        token = token[7:]  # 移除 'Bearer ' 前缀
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'message': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'message': '用户ID无效'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求数据不能为空'}), 400
        
        # 查找任务单位记录
        unit = TaskUnit.query.filter_by(id=unit_id, user_id=user_id).first()
        if not unit:
            return jsonify({'code': 404, 'message': '任务单位不存在'}), 404
        
        # 更新字段
        for key, value in data.items():
            if hasattr(unit, key) and key != 'id' and key != 'user_id':
                setattr(unit, key, value)
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': unit.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'更新任务单位失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@task_unit_bp.route('/task-unit/<int:unit_id>', methods=['DELETE'])
def delete_task_unit(unit_id):
    """删除任务单位"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'message': '未提供有效的认证令牌'}), 401
        
        token = token[7:]  # 移除 'Bearer ' 前缀
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'message': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'message': '用户ID无效'}), 401
        
        # 查找任务单位记录
        unit = TaskUnit.query.filter_by(id=unit_id, user_id=user_id).first()
        if not unit:
            return jsonify({'code': 404, 'message': '任务单位不存在'}), 404
        
        db.session.delete(unit)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'删除任务单位失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@task_unit_bp.route('/task-unit/batch-delete', methods=['POST'])
def batch_delete_task_unit():
    """批量删除任务单位"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'message': '未提供有效的认证令牌'}), 401
        
        token = token[7:]  # 移除 'Bearer ' 前缀
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'message': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'message': '用户ID无效'}), 401
        
        data = request.get_json()
        if not data or 'ids' not in data:
            return jsonify({'code': 400, 'message': '请选择要删除的记录'}), 400
        
        unit_ids = data.get('ids', [])
        if not unit_ids:
            return jsonify({'code': 400, 'message': '请选择要删除的记录'}), 400
        
        # 删除选中的任务单位记录
        deleted_count = TaskUnit.query.filter(
            TaskUnit.id.in_(unit_ids),
            TaskUnit.user_id == user_id
        ).delete(synchronize_session=False)
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': f'成功删除 {deleted_count} 条记录'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'批量删除任务单位失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500
