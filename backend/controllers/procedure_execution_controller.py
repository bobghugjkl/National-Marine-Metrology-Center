"""
外业调查操作规程执行统计表管理控制器
"""
from flask import Blueprint, request, jsonify, current_app
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models.procedure_execution import ProcedureExecution
from config.database import db
from utils.jwt_utils import token_required

procedure_execution_bp = Blueprint('procedure_execution', __name__, url_prefix='/api')

@procedure_execution_bp.route('/procedure-execution', methods=['GET'])
@token_required
def get_procedure_execution_list(current_user):
    """获取外业调查操作规程执行统计表列表（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 获取查询参数
        task_name = request.args.get('task_name')
        investigation_item_instrument = request.args.get('investigation_item_instrument')

        # 构建查询
        query = ProcedureExecution.query

        # 非管理员只能查看自己创建的记录
        if user_role != 'admin':
            query = query.filter(ProcedureExecution.user_id == user_id)

        # 按任务名称筛选（必须过滤，确保数据隔离）
        if task_name:
            query = query.filter(ProcedureExecution.task_name == task_name)
        else:
            # 如果没有传递任务名称，返回空结果（安全考虑）
            return jsonify({
                'code': 200,
                'msg': '获取成功',
                'data': []
            })

        # 按调查项目/仪器筛选
        if investigation_item_instrument:
            query = query.filter(ProcedureExecution.investigation_item_instrument.like(f'%{investigation_item_instrument}%'))

        # 执行查询
        records_list = query.all()

        # 转换为字典列表
        result = [record.to_dict() for record in records_list]

        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': result
        })
    except Exception as e:
        current_app.logger.error(f"获取外业调查操作规程执行统计表列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'获取外业调查操作规程执行统计表列表失败: {str(e)}',
            'data': None
        })

@procedure_execution_bp.route('/procedure-execution', methods=['POST'])
@token_required
def create_procedure_execution(current_user):
    """创建外业调查操作规程执行统计表记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 验证必填字段
        required_fields = ['task_name', 'investigation_item_instrument', 'task_undertaking_unit']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })

        # 创建新记录
        new_record = ProcedureExecution(
            task_name=data['task_name'],
            investigation_item_instrument=data['investigation_item_instrument'],
            task_undertaking_unit=data['task_undertaking_unit'],
            has_operating_procedures=data.get('has_operating_procedures'),
            operating_procedure_name=data.get('operating_procedure_name'),
            remarks=data.get('remarks'),
            attachments=json.dumps(data.get('attachmentList', [])),
            user_id=user_id
        )

        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': new_record.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建外业调查操作规程执行统计表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'创建外业调查操作规程执行统计表记录失败: {str(e)}',
            'data': None
        })

@procedure_execution_bp.route('/procedure-execution/<int:record_id>', methods=['PUT'])
@token_required
def update_procedure_execution(current_user, record_id):
    """更新外业调查操作规程执行统计表记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 查找记录
        record = ProcedureExecution.query.get(record_id)
        if not record:
            return jsonify({
                'code': 404,
                'msg': '外业调查操作规程执行统计表记录不存在',
                'data': None
            })

        # 验证权限：只能修改自己的记录（管理员除外）
        if record.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权修改其他用户的外业调查操作规程执行统计表记录',
                'data': None
            })

        # 更新字段
        updatable_fields = [
            'task_name', 'investigation_item_instrument', 'task_undertaking_unit',
            'has_operating_procedures', 'operating_procedure_name', 'remarks'
        ]

        for field in updatable_fields:
            if field in data:
                setattr(record, field, data[field])

        # 更新附件
        if 'attachmentList' in data:
            record.attachments = json.dumps(data['attachmentList'])

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': record.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新外业调查操作规程执行统计表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'更新外业调查操作规程执行统计表记录失败: {str(e)}',
            'data': None
        })

@procedure_execution_bp.route('/procedure-execution/<int:record_id>', methods=['DELETE'])
@token_required
def delete_procedure_execution(current_user, record_id):
    """删除外业调查操作规程执行统计表记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        # 查找记录
        record = ProcedureExecution.query.get(record_id)
        if not record:
            return jsonify({
                'code': 404,
                'msg': '外业调查操作规程执行统计表记录不存在',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if record.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权删除其他用户的外业调查操作规程执行统计表记录',
                'data': None
            })

        db.session.delete(record)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '删除成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除外业调查操作规程执行统计表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'删除外业调查操作规程执行统计表记录失败: {str(e)}',
            'data': None
        })

@procedure_execution_bp.route('/procedure-execution/batch-delete', methods=['DELETE'])
@token_required
def batch_delete_procedure_execution(current_user):
    """批量删除外业调查操作规程执行统计表记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json
        record_ids = data.get('ids', [])

        if not record_ids:
            return jsonify({
                'code': 400,
                'msg': '请选择要删除的外业调查操作规程执行统计表记录',
                'data': None
            })

        # 查找要删除的记录
        records_list = ProcedureExecution.query.filter(
            ProcedureExecution.id.in_(record_ids)
        ).all()

        if not records_list:
            return jsonify({
                'code': 404,
                'msg': '未找到要删除的外业调查操作规程执行统计表记录',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if current_user['role'] != 'admin':
            for record in records_list:
                if record.user_id != user_id:
                    return jsonify({
                        'code': 403,
                        'msg': '无权删除其他用户的外业调查操作规程执行统计表记录',
                        'data': None
                    })

        # 执行删除
        for record in records_list:
            db.session.delete(record)

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': f'成功删除{len(records_list)}条外业调查操作规程执行统计表记录',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除外业调查操作规程执行统计表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'批量删除外业调查操作规程执行统计表记录失败: {str(e)}',
            'data': None
        })

@procedure_execution_bp.route('/procedure-execution/upload', methods=['POST'])
@token_required
def upload_procedure_execution_attachment(current_user):
    """上传外业调查操作规程执行统计表附件"""
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
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'procedure_execution_attachments')
        os.makedirs(upload_folder, exist_ok=True)

        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{user_id}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)

        # 保存文件
        file.save(filepath)

        # 生成访问URL
        file_url = f"http://localhost:5000/static/uploads/procedure_execution_attachments/{unique_filename}"

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
        current_app.logger.error(f"上传外业调查操作规程执行统计表附件失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'上传外业调查操作规程执行统计表附件失败: {str(e)}',
            'data': None
        })
