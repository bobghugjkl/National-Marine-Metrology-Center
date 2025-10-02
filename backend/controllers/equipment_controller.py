"""
仪器设备管理控制器
"""
from flask import Blueprint, request, jsonify, current_app
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models.equipment import Equipment
from config.database import db
from utils.jwt_utils import token_required

equipment_bp = Blueprint('equipment', __name__, url_prefix='/api')

@equipment_bp.route('/equipment', methods=['GET'])
@token_required
def get_equipment_list(current_user):
    """获取仪器设备列表（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 获取查询参数
        task_name = request.args.get('task_name')
        name = request.args.get('name')

        # 构建查询
        query = Equipment.query

        # 非管理员只能查看自己创建的记录
        if user_role != 'admin':
            query = query.filter(Equipment.user_id == user_id)

        # 按任务名称筛选
        if task_name:
            query = query.filter(Equipment.task_name == task_name)

        # 按设备名称筛选
        if name:
            query = query.filter(Equipment.name.like(f'%{name}%'))

        # 执行查询
        equipment_list = query.all()

        # 转换为字典列表
        result = [equipment.to_dict() for equipment in equipment_list]

        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': result
        })
    except Exception as e:
        current_app.logger.error(f"获取仪器设备列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'获取仪器设备列表失败: {str(e)}',
            'data': None
        })

@equipment_bp.route('/equipment', methods=['POST'])
@token_required
def create_equipment(current_user):
    """创建仪器设备记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 验证必填字段
        required_fields = ['task_name', 'category', 'name', 'number', 'model']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })

        # 检查是否已存在相同编号的设备
        existing_equipment = Equipment.query.filter_by(
            number=data['number'],
            task_name=data['task_name']
        ).first()

        if existing_equipment:
            return jsonify({
                'code': 400,
                'msg': '该任务中已存在相同编号的设备',
                'data': None
            })

        # 创建新设备记录
        new_equipment = Equipment(
            task_name=data['task_name'],
            category=data['category'],
            name=data['name'],
            number=data['number'],
            model=data['model'],
            traceability_method=data.get('traceability_method'),
            calibration_date=data.get('calibration_date'),
            certificate_number=data.get('certificate_number'),
            validity_period=data.get('validity_period'),
            calibration_organization=data.get('calibration_organization'),
            remarks=data.get('remarks'),
            attachments=json.dumps(data.get('attachmentList', [])),
            user_id=user_id
        )

        db.session.add(new_equipment)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': new_equipment.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建仪器设备失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'创建仪器设备失败: {str(e)}',
            'data': None
        })

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['PUT'])
@token_required
def update_equipment(current_user, equipment_id):
    """更新仪器设备记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 查找设备记录
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({
                'code': 404,
                'msg': '仪器设备不存在',
                'data': None
            })

        # 验证权限：只能修改自己的记录（管理员除外）
        if equipment.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权修改其他用户的设备记录',
                'data': None
            })

        # 更新字段
        updatable_fields = [
            'task_name', 'category', 'name', 'number', 'model',
            'traceability_method', 'calibration_date', 'certificate_number',
            'validity_period', 'calibration_organization', 'remarks'
        ]

        for field in updatable_fields:
            if field in data:
                setattr(equipment, field, data[field])

        # 更新附件
        if 'attachmentList' in data:
            equipment.attachments = json.dumps(data['attachmentList'])

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': equipment.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新仪器设备失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'更新仪器设备失败: {str(e)}',
            'data': None
        })

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['DELETE'])
@token_required
def delete_equipment(current_user, equipment_id):
    """删除仪器设备记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        # 查找设备记录
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({
                'code': 404,
                'msg': '仪器设备不存在',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if equipment.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权删除其他用户的设备记录',
                'data': None
            })

        db.session.delete(equipment)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '删除成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除仪器设备失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'删除仪器设备失败: {str(e)}',
            'data': None
        })

@equipment_bp.route('/equipment/batch-delete', methods=['DELETE'])
@token_required
def batch_delete_equipment(current_user):
    """批量删除仪器设备记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json
        equipment_ids = data.get('ids', [])

        if not equipment_ids:
            return jsonify({
                'code': 400,
                'msg': '请选择要删除的设备',
                'data': None
            })

        # 查找要删除的设备记录
        equipment_list = Equipment.query.filter(
            Equipment.id.in_(equipment_ids)
        ).all()

        if not equipment_list:
            return jsonify({
                'code': 404,
                'msg': '未找到要删除的设备记录',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if current_user['role'] != 'admin':
            for equipment in equipment_list:
                if equipment.user_id != user_id:
                    return jsonify({
                        'code': 403,
                        'msg': '无权删除其他用户的设备记录',
                        'data': None
                    })

        # 执行删除
        for equipment in equipment_list:
            db.session.delete(equipment)

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': f'成功删除{len(equipment_list)}条设备记录',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除仪器设备失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'批量删除仪器设备失败: {str(e)}',
            'data': None
        })

@equipment_bp.route('/equipment/upload', methods=['POST'])
@token_required
def upload_equipment_attachment(current_user):
    """上传仪器设备附件"""
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
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'equipment_attachments')
        os.makedirs(upload_folder, exist_ok=True)

        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{user_id}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)

        # 保存文件
        file.save(filepath)

        # 生成访问URL
        file_url = f"http://localhost:5000/static/uploads/equipment_attachments/{unique_filename}"

        return jsonify({
            'code': 200,
            'msg': '上传成功',
            'data': {
                'name': filename,
                'url': file_url,
                'uid': timestamp
            }
        })
    except Exception as e:
        current_app.logger.error(f"上传仪器设备附件失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'上传仪器设备附件失败: {str(e)}',
            'data': None
        })
