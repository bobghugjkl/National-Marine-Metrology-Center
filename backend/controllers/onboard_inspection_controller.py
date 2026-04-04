"""
随船质量监督检查表控制器
"""
from flask import Blueprint, request, jsonify, current_app
from config.database import db
from models.onboard_inspection import OnboardInspection
from utils.jwt_utils import verify_token
import json
import os
import time
from werkzeug.utils import secure_filename

onboard_inspection_bp = Blueprint('onboard_inspection', __name__, url_prefix='/api')

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

@onboard_inspection_bp.before_request
def handle_preflight_request():
    if request.method == 'OPTIONS':
        return handle_preflight()

@onboard_inspection_bp.route('/onboard-inspection/<task_name>', methods=['GET'])
def get_onboard_inspection(task_name):
    """获取随船质量监督检查表"""
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
        
        # 根据任务名称获取检查记录
        if not task_name:
            return jsonify({'code': 400, 'message': '任务名称不能为空'}), 400
        
        inspection = OnboardInspection.query.filter_by(
            task_name=task_name,
            user_id=user_id
        ).first()
        
        if not inspection:
            # 如果没有找到记录，返回空数据
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'task_name': task_name,
                    'inspected_unit': '',
                    'participating_unit': '',
                    'task_code': '',
                    'chief_scientist': '',
                    'inspection_date': '',
                    'onboard_supervisor': '',
                    'inspected_unit_personnel': '',
                    'check_1': '',
                    'check_1_problem': '',
                    'check_2': '',
                    'check_2_problem': '',
                    'check_3': '',
                    'check_3_problem': '',
                    'check_4': '',
                    'check_4_problem': '',
                    'check_5': '',
                    'check_5_problem': '',
                    'check_6': '',
                    'check_6_problem': '',
                    'check_7': '',
                    'check_7_problem': '',
                    'check_8': '',
                    'check_8_problem': '',
                    'check_9': '',
                    'check_9_problem': '',
                    'check_10': '',
                    'check_10_problem': '',
                    'check_11': '',
                    'check_11_problem': '',
                    'check_12': '',
                    'check_12_problem': '',
                    'team_leader_sign': '',
                    'task_leader_sign': '',
                    'attachments': '[]'
                }
            })
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': inspection.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f'获取随船质量监督检查表失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@onboard_inspection_bp.route('/onboard-inspection', methods=['POST'])
def create_onboard_inspection():
    """创建随船质量监督检查表"""
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
        
        # 检查是否已存在该任务的检查记录
        existing = OnboardInspection.query.filter_by(
            task_name=data.get('task_name'),
            user_id=user_id
        ).first()
        
        if existing:
            return jsonify({'code': 400, 'message': '该任务已存在检查记录'}), 400
        
        # 创建新记录
        inspection = OnboardInspection(
            task_name=data.get('task_name'),
            inspected_unit=data.get('inspected_unit', ''),
            participating_unit=data.get('participating_unit', ''),
            task_code=data.get('task_code', ''),
            chief_scientist=data.get('chief_scientist', ''),
            inspection_date=data.get('inspection_date', ''),
            onboard_supervisor=data.get('onboard_supervisor', ''),
            inspected_unit_personnel=data.get('inspected_unit_personnel', ''),
            check_1=data.get('check_1', ''),
            check_1_problem=data.get('check_1_problem', ''),
            check_2=data.get('check_2', ''),
            check_2_problem=data.get('check_2_problem', ''),
            check_3=data.get('check_3', ''),
            check_3_problem=data.get('check_3_problem', ''),
            check_4=data.get('check_4', ''),
            check_4_problem=data.get('check_4_problem', ''),
            check_5=data.get('check_5', ''),
            check_5_problem=data.get('check_5_problem', ''),
            check_6=data.get('check_6', ''),
            check_6_problem=data.get('check_6_problem', ''),
            check_7=data.get('check_7', ''),
            check_7_problem=data.get('check_7_problem', ''),
            check_8=data.get('check_8', ''),
            check_8_problem=data.get('check_8_problem', ''),
            check_9=data.get('check_9', ''),
            check_9_problem=data.get('check_9_problem', ''),
            check_10=data.get('check_10', ''),
            check_10_problem=data.get('check_10_problem', ''),
            check_11=data.get('check_11', ''),
            check_11_problem=data.get('check_11_problem', ''),
            check_12=data.get('check_12', ''),
            check_12_problem=data.get('check_12_problem', ''),
            team_leader_sign=data.get('team_leader_sign', ''),
            task_leader_sign=data.get('task_leader_sign', ''),
            attachments=data.get('attachments', '[]'),
            user_id=user_id
        )
        
        db.session.add(inspection)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '创建成功',
            'data': inspection.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'创建随船质量监督检查表失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@onboard_inspection_bp.route('/onboard-inspection/<task_name>', methods=['PUT'])
def update_onboard_inspection(task_name):
    """更新随船质量监督检查表"""
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
        
        # 查找现有记录
        inspection = OnboardInspection.query.filter_by(
            task_name=task_name,
            user_id=user_id
        ).first()
        
        if not inspection:
            # 如果不存在，创建新记录
            inspection = OnboardInspection(
                task_name=task_name,
                user_id=user_id
            )
            db.session.add(inspection)
        
        # 更新字段
        for key, value in data.items():
            if hasattr(inspection, key):
                setattr(inspection, key, value)
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': inspection.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'更新随船质量监督检查表失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@onboard_inspection_bp.route('/onboard-inspection/<task_name>', methods=['DELETE'])
def delete_onboard_inspection(task_name):
    """删除随船质量监督检查表"""
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
        
        # 查找记录
        inspection = OnboardInspection.query.filter_by(
            task_name=task_name,
            user_id=user_id
        ).first()
        
        if not inspection:
            return jsonify({'code': 404, 'message': '检查记录不存在'}), 404
        
        # 删除附件文件
        if inspection.attachments:
            try:
                attachments = json.loads(inspection.attachments)
                for attachment in attachments:
                    file_path = attachment.get('file_path')
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
            except Exception as e:
                current_app.logger.warning(f'删除附件文件失败: {str(e)}')
        
        db.session.delete(inspection)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'删除随船质量监督检查表失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@onboard_inspection_bp.route('/onboard-inspection/upload', methods=['POST'])
def upload_onboard_inspection_attachment():
    """上传随船质量监督检查表附件"""
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
        
        if 'file' not in request.files:
            return jsonify({'code': 400, 'message': '未找到上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': 400, 'message': '未选择文件'}), 400
        
        if file:
            # 确保上传目录存在
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'onboard_inspection')
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成安全的文件名
            filename = secure_filename(file.filename)
            timestamp = str(int(time.time() * 1000))
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"
            
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            # 生成访问URL
            file_url = f"http://localhost:5000/static/uploads/onboard_inspection/{filename}"
            
            return jsonify({
                'code': 200,
                'message': '上传成功',
                'data': {
                    'filename': filename,
                    'file_path': file_path,
                    'file_url': file_url,
                    'file_size': os.path.getsize(file_path)
                }
            })
        
    except Exception as e:
        current_app.logger.error(f'上传附件失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500
