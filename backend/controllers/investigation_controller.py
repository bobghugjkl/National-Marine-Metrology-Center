"""
外业调查项目/仪器比测统计表控制器
"""
from flask import Blueprint, request, jsonify, current_app
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models.investigation import InvestigationProject
from config.database import db
from utils.jwt_utils import token_required

investigation_bp = Blueprint('investigation', __name__, url_prefix='/api')

@investigation_bp.route('/investigation-projects', methods=['GET'])
@token_required
def get_investigation_projects(current_user):
    """获取外业调查项目/仪器比测统计表列表（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 获取查询参数
        task_name = request.args.get('task_name')
        investigation_item = request.args.get('investigation_item')

        # 构建查询
        query = InvestigationProject.query

        # 非管理员只能查看自己创建的记录
        if user_role != 'admin':
            query = query.filter(InvestigationProject.user_id == user_id)

        # 按任务名称筛选（必须过滤，确保数据隔离）
        if task_name:
            query = query.filter(InvestigationProject.task_name == task_name)
        else:
            # 如果没有传递任务名称，返回空结果（安全考虑）
            return jsonify({
                'code': 200,
                'msg': '获取成功',
                'data': []
            })

        # 按调查项目筛选
        if investigation_item:
            query = query.filter(InvestigationProject.investigation_item.like(f'%{investigation_item}%'))

        # 执行查询
        projects_list = query.all()

        # 转换为字典列表
        result = [project.to_dict() for project in projects_list]

        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': result
        })
    except Exception as e:
        current_app.logger.error(f"获取外业调查项目列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'获取外业调查项目列表失败: {str(e)}',
            'data': None
        })

@investigation_bp.route('/investigation-projects', methods=['POST'])
@token_required
def create_investigation_project(current_user):
    """创建外业调查项目记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 验证必填字段
        required_fields = ['task_name', 'investigation_item', 'unit_a_instrument', 'unit_b_instrument']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空',
                    'data': None
                })

        # 创建新调查项目记录
        new_project = InvestigationProject(
            task_name=data['task_name'],
            investigation_item=data['investigation_item'],
            unit_a_instrument=data['unit_a_instrument'],
            unit_b_instrument=data['unit_b_instrument'],
            comparison_time=data.get('comparison_time'),
            comparison_location=data.get('comparison_location'),
            comparison_result=data.get('comparison_result'),
            remarks=data.get('remarks'),
            attachments=json.dumps(data.get('attachmentList', [])),
            user_id=user_id
        )

        db.session.add(new_project)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': new_project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建外业调查项目失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'创建外业调查项目失败: {str(e)}',
            'data': None
        })

@investigation_bp.route('/investigation-projects/<int:project_id>', methods=['PUT'])
@token_required
def update_investigation_project(current_user, project_id):
    """更新外业调查项目记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json

        # 查找项目记录
        project = InvestigationProject.query.get(project_id)
        if not project:
            return jsonify({
                'code': 404,
                'msg': '外业调查项目不存在',
                'data': None
            })

        # 验证权限：只能修改自己的记录（管理员除外）
        if project.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权修改其他用户的调查项目记录',
                'data': None
            })

        # 更新字段
        updatable_fields = [
            'task_name', 'investigation_item', 'unit_a_instrument', 'unit_b_instrument',
            'comparison_time', 'comparison_location', 'comparison_result', 'remarks'
        ]

        for field in updatable_fields:
            if field in data:
                setattr(project, field, data[field])

        # 更新附件
        if 'attachmentList' in data:
            project.attachments = json.dumps(data['attachmentList'])

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新外业调查项目失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'更新外业调查项目失败: {str(e)}',
            'data': None
        })

@investigation_bp.route('/investigation-projects/<int:project_id>', methods=['DELETE'])
@token_required
def delete_investigation_project(current_user, project_id):
    """删除外业调查项目记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        # 查找项目记录
        project = InvestigationProject.query.get(project_id)
        if not project:
            return jsonify({
                'code': 404,
                'msg': '外业调查项目不存在',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if project.user_id != user_id and current_user['role'] != 'admin':
            return jsonify({
                'code': 403,
                'msg': '无权删除其他用户的调查项目记录',
                'data': None
            })

        db.session.delete(project)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '删除成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除外业调查项目失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'删除外业调查项目失败: {str(e)}',
            'data': None
        })

@investigation_bp.route('/investigation-projects/batch-delete', methods=['DELETE'])
@token_required
def batch_delete_investigation_projects(current_user):
    """批量删除外业调查项目记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']

        data = request.json
        project_ids = data.get('ids', [])

        if not project_ids:
            return jsonify({
                'code': 400,
                'msg': '请选择要删除的调查项目',
                'data': None
            })

        # 查找要删除的项目记录
        projects_list = InvestigationProject.query.filter(
            InvestigationProject.id.in_(project_ids)
        ).all()

        if not projects_list:
            return jsonify({
                'code': 404,
                'msg': '未找到要删除的调查项目记录',
                'data': None
            })

        # 验证权限：只能删除自己的记录（管理员除外）
        if current_user['role'] != 'admin':
            for project in projects_list:
                if project.user_id != user_id:
                    return jsonify({
                        'code': 403,
                        'msg': '无权删除其他用户的调查项目记录',
                        'data': None
                    })

        # 执行删除
        for project in projects_list:
            db.session.delete(project)

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': f'成功删除{len(projects_list)}条调查项目记录',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除外业调查项目失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'批量删除外业调查项目失败: {str(e)}',
            'data': None
        })

@investigation_bp.route('/investigation-projects/upload', methods=['POST'])
@token_required
def upload_investigation_attachment(current_user):
    """上传外业调查项目附件"""
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
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'investigation_attachments')
        os.makedirs(upload_folder, exist_ok=True)

        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{user_id}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)

        # 保存文件
        file.save(filepath)

        # 生成访问URL
        file_url = f"http://localhost:5000/static/uploads/investigation_attachments/{unique_filename}"

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
        current_app.logger.error(f"上传外业调查项目附件失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'上传外业调查项目附件失败: {str(e)}',
            'data': None
        })
