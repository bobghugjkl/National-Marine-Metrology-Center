"""
监督员日志管理控制器
"""
from flask import Blueprint, request, jsonify, current_app
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models.supervisor_log import SupervisorLog
from config.database import db
from utils.jwt_utils import token_required

supervisor_log_bp = Blueprint('supervisor_log', __name__, url_prefix='/api')

@supervisor_log_bp.route('/supervisor-logs', methods=['GET'])
@token_required
def get_supervisor_logs(current_user):
    """获取监督员日志列表（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 获取查询参数
        task_name = request.args.get('task_name')
        supervisor = request.args.get('supervisor')

        # 构建查询
        query = SupervisorLog.query

        # 非管理员只能查看自己创建的记录
        if user_role != 'admin':
            query = query.filter(SupervisorLog.user_id == user_id)

        # 按任务名称筛选（必须过滤，确保数据隔离）
        if task_name:
            query = query.filter(SupervisorLog.task_name == task_name)
        else:
            # 如果没有传递任务名称，返回空结果（安全考虑）
            return jsonify({
                'code': 200,
                'msg': '获取成功',
                'data': []
            })

        # 按监督员筛选
        if supervisor:
            query = query.filter(SupervisorLog.supervisor.like(f'%{supervisor}%'))

        # 执行查询
        logs_list = query.all()

        # 转换为字典列表
        result = [log.to_dict() for log in logs_list]

        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': result
        })
    except Exception as e:
        current_app.logger.error(f"获取监督员日志列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'获取监督员日志列表失败: {str(e)}',
            'data': None
        })

@supervisor_log_bp.route('/supervisor-logs', methods=['POST'])
@token_required
def create_supervisor_log(current_user):
    """创建监督员日志记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 验证必填字段
        required_fields = ['task_name', 'supervisor', 'inspection_date', 'inspection_content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })

        # 创建新监督员日志记录
        new_log = SupervisorLog(
            task_name=data['task_name'],
            supervisor=data['supervisor'],
            inspection_date=data['inspection_date'],
            inspection_content=data['inspection_content'],
            existing_problems=data.get('existing_problems'),
            rectification_status=data.get('rectification_status'),
            form_filling_time=data.get('form_filling_time'),
            attachments=json.dumps(data.get('attachmentList', [])),
            user_id=user_id
        )

        db.session.add(new_log)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': new_log.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建监督员日志失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'创建监督员日志失败: {str(e)}',
            'data': None
        })

@supervisor_log_bp.route('/supervisor-logs/<int:log_id>', methods=['PUT'])
@token_required
def update_supervisor_log(current_user, log_id):
    """更新监督员日志记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 查找日志记录
        log = SupervisorLog.query.get(log_id)
        if not log:
            return jsonify({
                'code': 404,
                'msg': '监督员日志不存在',
                'data': None
            })

        # 验证权限：只能修改自己的记录（管理员除外）
        if log.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权修改其他用户的监督员日志记录',
                'data': None
            })

        # 更新字段
        updatable_fields = [
            'task_name', 'supervisor', 'inspection_date', 'inspection_content',
            'existing_problems', 'rectification_status', 'form_filling_time'
        ]

        for field in updatable_fields:
            if field in data:
                setattr(log, field, data[field])

        # 更新附件
        if 'attachmentList' in data:
            log.attachments = json.dumps(data['attachmentList'])

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': log.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新监督员日志失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'更新监督员日志失败: {str(e)}',
            'data': None
        })

@supervisor_log_bp.route('/supervisor-logs/<int:log_id>', methods=['DELETE'])
@token_required
def delete_supervisor_log(current_user, log_id):
    """删除监督员日志记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        # 查找日志记录
        log = SupervisorLog.query.get(log_id)
        if not log:
            return jsonify({
                'code': 404,
                'msg': '监督员日志不存在',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if log.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权删除其他用户的监督员日志记录',
                'data': None
            })

        db.session.delete(log)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '删除成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除监督员日志失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'删除监督员日志失败: {str(e)}',
            'data': None
        })

@supervisor_log_bp.route('/supervisor-logs/batch-delete', methods=['DELETE'])
@token_required
def batch_delete_supervisor_logs(current_user):
    """批量删除监督员日志记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json
        log_ids = data.get('ids', [])

        if not log_ids:
            return jsonify({
                'code': 400,
                'msg': '请选择要删除的监督员日志',
                'data': None
            })

        # 查找要删除的日志记录
        logs_list = SupervisorLog.query.filter(
            SupervisorLog.id.in_(log_ids)
        ).all()

        if not logs_list:
            return jsonify({
                'code': 404,
                'msg': '未找到要删除的监督员日志记录',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if current_user['role'] != 'admin':
            for log in logs_list:
                if log.user_id != user_id:
                    return jsonify({
                        'code': 403,
                        'msg': '无权删除其他用户的监督员日志记录',
                        'data': None
                    })

        # 执行删除
        for log in logs_list:
            db.session.delete(log)

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': f'成功删除{len(logs_list)}条监督员日志记录',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除监督员日志失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'批量删除监督员日志失败: {str(e)}',
            'data': None
        })

@supervisor_log_bp.route('/supervisor-logs/upload', methods=['POST'])
@token_required
def upload_supervisor_log_attachment(current_user):
    """上传监督员日志附件"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                'code': 400,
                'msg': '未找到上传文件',
                'data': None
            })

        file = request.files['file']

        # 检查文件名
        if file.filename == '':
            return jsonify({
                'code': 400,
                'msg': '未选择文件',
                'data': None
            })

        # 安全的文件名
        filename = secure_filename(file.filename)

        # 确保上传目录存在
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'supervisor_log_attachments')
        os.makedirs(upload_folder, exist_ok=True)

        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{user_id}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)

        # 保存文件
        file.save(filepath)

        # 生成访问URL
        file_url = f"http://localhost:5000/static/uploads/supervisor_log_attachments/{unique_filename}"

        return jsonify({
            'code': 200,
            'msg': '上传成功',
            'data': {
                'filename': filename,
                'url': file_url,
                'size': os.path.getsize(filepath)
            }
        })
    except Exception as e:
        current_app.logger.error(f"上传监督员日志附件失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'上传监督员日志附件失败: {str(e)}',
            'data': None
        })
