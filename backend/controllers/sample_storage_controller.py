"""
外业调查样品储存记录抽查表管理控制器
"""
from flask import Blueprint, request, jsonify, current_app
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models.sample_storage import SampleStorage
from config.database import db
from utils.jwt_utils import token_required

sample_storage_bp = Blueprint('sample_storage', __name__, url_prefix='/api')

@sample_storage_bp.before_request
def handle_preflight():
    """处理CORS预检请求"""
    if request.method == "OPTIONS":
        response = jsonify({'message': 'OK'})
        # 当使用withCredentials时，不能使用通配符，必须指定具体域名
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://127.0.0.1:5173']:
            response.headers.add("Access-Control-Allow-Origin", origin)
        else:
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization, Accept, X-Requested-With")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', "true")
        return response

@sample_storage_bp.route('/sample-storage', methods=['GET'])
@token_required
def get_sample_storage_list(current_user):
    """获取外业调查样品储存记录抽查表列表（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 获取查询参数
        task_name = request.args.get('task_name')
        survey_item = request.args.get('survey_item')

        # 构建查询
        query = SampleStorage.query

        # 非管理员只能查看自己创建的记录
        if user_role != 'admin':
            query = query.filter(SampleStorage.user_id == user_id)

        # 按任务名称筛选（必须过滤，确保数据隔离）
        if task_name:
            query = query.filter(SampleStorage.task_name == task_name)
        else:
            # 如果没有传递任务名称，返回空结果（安全考虑）
            return jsonify({
                'code': 200,
                'msg': '获取成功',
                'data': []
            })

        # 按调查项目筛选
        if survey_item:
            query = query.filter(SampleStorage.survey_item.like(f'%{survey_item}%'))

        # 执行查询
        records = query.all()

        # 转换为字典格式
        data = [record.to_dict() for record in records]

        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': data
        })

    except Exception as e:
        current_app.logger.error(f"获取外业调查样品储存记录抽查表列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'获取失败: {str(e)}'
        }), 500

@sample_storage_bp.route('/sample-storage', methods=['POST'])
@token_required
def create_sample_storage(current_user):
    """创建外业调查样品储存记录抽查表记录（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']

        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'msg': '请求数据不能为空'
            }), 400

        # 验证必填字段
        required_fields = ['task_name', 'survey_item', 'task_undertaking_unit']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'code': 400,
                    'msg': f'{field}不能为空'
                }), 400

        # 处理附件列表
        attachment_list = data.get('attachmentList', [])
        attachments_json = json.dumps(attachment_list) if attachment_list else None

        # 创建新记录
        record = SampleStorage(
            task_name=data['task_name'],
            survey_item=data['survey_item'],
            task_undertaking_unit=data['task_undertaking_unit'],
            stored_samples=data.get('stored_samples'),
            record_time=datetime.strptime(data['record_time'], '%Y-%m-%d').date() if data.get('record_time') else None,
            spot_check_time=datetime.strptime(data['spot_check_time'], '%Y-%m-%d').date() if data.get('spot_check_time') else None,
            qualified_or_not=data.get('qualified_or_not'),
            remarks=data.get('remarks'),
            attachments=attachments_json,
            user_id=user_id
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': record.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建外业调查样品储存记录抽查表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'创建失败: {str(e)}'
        }), 500

@sample_storage_bp.route('/sample-storage/<int:record_id>', methods=['PUT'])
@token_required
def update_sample_storage(current_user, record_id):
    """更新外业调查样品储存记录抽查表记录（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 查找记录
        record = SampleStorage.query.get(record_id)
        if not record:
            return jsonify({
                'code': 404,
                'msg': '记录不存在'
            }), 404

        # 非管理员只能修改自己的记录
        if user_role != 'admin' and record.user_id != user_id:
            return jsonify({
                'code': 403,
                'msg': '无权限修改此记录'
            }), 403

        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'msg': '请求数据不能为空'
            }), 400

        # 更新字段
        if 'task_name' in data:
            record.task_name = data['task_name']
        if 'survey_item' in data:
            record.survey_item = data['survey_item']
        if 'task_undertaking_unit' in data:
            record.task_undertaking_unit = data['task_undertaking_unit']
        if 'stored_samples' in data:
            record.stored_samples = data['stored_samples']
        if 'record_time' in data:
            record.record_time = datetime.strptime(data['record_time'], '%Y-%m-%d').date() if data['record_time'] else None
        if 'spot_check_time' in data:
            record.spot_check_time = datetime.strptime(data['spot_check_time'], '%Y-%m-%d').date() if data['spot_check_time'] else None
        if 'qualified_or_not' in data:
            record.qualified_or_not = data['qualified_or_not']
        if 'remarks' in data:
            record.remarks = data['remarks']
        if 'attachmentList' in data:
            attachment_list = data.get('attachmentList', [])
            record.attachments = json.dumps(attachment_list) if attachment_list else None

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': record.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新外业调查样品储存记录抽查表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}'
        }), 500

@sample_storage_bp.route('/sample-storage/<int:record_id>', methods=['DELETE'])
@token_required
def delete_sample_storage(current_user, record_id):
    """删除外业调查样品储存记录抽查表记录（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 查找记录
        record = SampleStorage.query.get(record_id)
        if not record:
            return jsonify({
                'code': 404,
                'msg': '记录不存在'
            }), 404

        # 非管理员只能删除自己的记录
        if user_role != 'admin' and record.user_id != user_id:
            return jsonify({
                'code': 403,
                'msg': '无权限删除此记录'
            }), 403

        db.session.delete(record)
        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '删除成功'
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除外业调查样品储存记录抽查表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'删除失败: {str(e)}'
        }), 500

@sample_storage_bp.route('/sample-storage/batch-delete', methods=['POST'])
@token_required
def batch_delete_sample_storage(current_user):
    """批量删除外业调查样品储存记录抽查表记录（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 获取请求数据
        data = request.get_json()
        if not data or 'ids' not in data:
            return jsonify({
                'code': 400,
                'msg': '请求数据不能为空'
            }), 400

        record_ids = data['ids']
        if not isinstance(record_ids, list) or len(record_ids) == 0:
            return jsonify({
                'code': 400,
                'msg': '记录ID列表不能为空'
            }), 400

        # 查找记录
        query = SampleStorage.query.filter(SampleStorage.id.in_(record_ids))
        
        # 非管理员只能删除自己的记录
        if user_role != 'admin':
            query = query.filter(SampleStorage.user_id == user_id)

        records = query.all()
        
        if len(records) != len(record_ids):
            return jsonify({
                'code': 403,
                'msg': '部分记录无权限删除'
            }), 403

        # 删除记录
        for record in records:
            db.session.delete(record)

        db.session.commit()

        return jsonify({
            'code': 200,
            'msg': f'成功删除{len(records)}条记录'
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除外业调查样品储存记录抽查表记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'批量删除失败: {str(e)}'
        }), 500

@sample_storage_bp.route('/sample-storage/upload', methods=['POST'])
@token_required
def upload_sample_storage_attachment(current_user):
    """上传外业调查样品储存记录抽查表附件（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']

        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'code': 400,
                'msg': '没有选择文件'
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'code': 400,
                'msg': '没有选择文件'
            }), 400

        # 检查文件类型
        allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({
                'code': 400,
                'msg': '不支持的文件类型'
            }), 400

        # 生成安全的文件名
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{user_id}_{filename}"

        # 创建上传目录
        upload_dir = os.path.join(current_app.static_folder, 'uploads', 'sample_storage_attachments')
        os.makedirs(upload_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        # 生成访问URL
        file_url = f"http://localhost:5000/static/uploads/sample_storage_attachments/{filename}"

        return jsonify({
            'code': 200,
            'msg': '上传成功',
            'data': {
                'filename': file.filename,
                'url': file_url,
                'size': os.path.getsize(file_path)
            }
        })

    except Exception as e:
        current_app.logger.error(f"上传外业调查样品储存记录抽查表附件失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'上传失败: {str(e)}'
        }), 500
