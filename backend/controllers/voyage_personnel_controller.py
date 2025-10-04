"""
航中外业调查人员控制器
"""
import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from config.database import db
from models.voyage_personnel import VoyagePersonnel
from utils.jwt_utils import verify_token

# 创建蓝图
voyage_personnel_bp = Blueprint('voyage_personnel', __name__, url_prefix='/api')

@voyage_personnel_bp.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'code': 200, 'msg': 'OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@voyage_personnel_bp.route('/voyage-personnel', methods=['GET', 'OPTIONS'])
def get_voyage_personnel():
    """获取航中外业调查人员列表"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'msg': '未提供有效的认证令牌'}), 401
        
        token = token.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'msg': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'msg': '用户ID无效'}), 401
        
        # 获取查询参数
        task_name = request.args.get('task_name')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 构建查询（必须按任务名称过滤，确保数据隔离）
        query = VoyagePersonnel.query.filter_by(user_id=user_id)
        if task_name:
            query = query.filter_by(task_name=task_name)
        else:
            # 如果没有传递任务名称，返回空结果（安全考虑）
            return jsonify({
                'code': 200,
                'msg': '获取成功',
                'data': [],
                'total': 0
            })
        
        # 分页查询
        total = query.count()
        records = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 转换为字典
        data = [record.to_dict() for record in records]
        
        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
        
    except Exception as e:
        print(f"获取航中外业调查人员列表错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'}), 500

@voyage_personnel_bp.route('/voyage-personnel', methods=['POST', 'OPTIONS'])
def create_voyage_personnel():
    """创建航中外业调查人员记录"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'msg': '未提供有效的认证令牌'}), 401
        
        token = token.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'msg': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'msg': '用户ID无效'}), 401
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'msg': '请求数据不能为空'}), 400
        
        # 验证必填字段
        required_fields = ['task_name', 'name', 'sex', 'birthdate', 'professional_title', 'employer', 'specialty']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'code': 400, 'msg': f'{field}字段不能为空'}), 400
        
        # 创建新记录
        record = VoyagePersonnel(
            task_name=data['task_name'],
            name=data['name'],
            sex=data['sex'],
            birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d').date(),
            professional_title=data['professional_title'],
            employer=data['employer'],
            specialty=data['specialty'],
            instruments=data.get('instruments', ''),
            training=data.get('training', ''),
            remarks=data.get('remarks', ''),
            attachments=json.dumps(data.get('attachmentList', [])),
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
        print(f"创建航中外业调查人员记录错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'}), 500

@voyage_personnel_bp.route('/voyage-personnel/<int:record_id>', methods=['PUT'])
def update_voyage_personnel(record_id):
    """更新航中外业调查人员记录"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'msg': '未提供有效的认证令牌'}), 401
        
        token = token.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'msg': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'msg': '用户ID无效'}), 401
        
        # 查找记录
        record = VoyagePersonnel.query.filter_by(id=record_id, user_id=user_id).first()
        if not record:
            return jsonify({'code': 404, 'msg': '记录不存在'}), 404
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'msg': '请求数据不能为空'}), 400
        
        # 更新字段
        if 'task_name' in data:
            record.task_name = data['task_name']
        if 'name' in data:
            record.name = data['name']
        if 'sex' in data:
            record.sex = data['sex']
        if 'birthdate' in data:
            record.birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
        if 'professional_title' in data:
            record.professional_title = data['professional_title']
        if 'employer' in data:
            record.employer = data['employer']
        if 'specialty' in data:
            record.specialty = data['specialty']
        if 'instruments' in data:
            record.instruments = data['instruments']
        if 'training' in data:
            record.training = data['training']
        if 'remarks' in data:
            record.remarks = data['remarks']
        if 'attachmentList' in data:
            record.attachments = json.dumps(data['attachmentList'])
        
        record.update_time = datetime.now()
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': record.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"更新航中外业调查人员记录错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'}), 500

@voyage_personnel_bp.route('/voyage-personnel/<int:record_id>', methods=['DELETE'])
def delete_voyage_personnel(record_id):
    """删除航中外业调查人员记录"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'msg': '未提供有效的认证令牌'}), 401
        
        token = token.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'msg': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'msg': '用户ID无效'}), 401
        
        # 查找记录
        record = VoyagePersonnel.query.filter_by(id=record_id, user_id=user_id).first()
        if not record:
            return jsonify({'code': 404, 'msg': '记录不存在'}), 404
        
        # 删除记录
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"删除航中外业调查人员记录错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'}), 500

@voyage_personnel_bp.route('/voyage-personnel/batch-delete', methods=['POST'])
def batch_delete_voyage_personnel():
    """批量删除航中外业调查人员记录"""
    try:
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'code': 401, 'msg': '未提供有效的认证令牌'}), 401
        
        token = token.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'msg': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 401, 'msg': '用户ID无效'}), 401
        
        # 获取要删除的记录ID列表
        data = request.get_json()
        if not data or 'ids' not in data:
            return jsonify({'code': 400, 'msg': '请提供要删除的记录ID列表'}), 400
        
        record_ids = data['ids']
        if not isinstance(record_ids, list) or not record_ids:
            return jsonify({'code': 400, 'msg': '记录ID列表不能为空'}), 400
        
        # 查找并删除记录
        deleted_count = 0
        for record_id in record_ids:
            record = VoyagePersonnel.query.filter_by(id=record_id, user_id=user_id).first()
            if record:
                db.session.delete(record)
                deleted_count += 1
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': f'成功删除{deleted_count}条记录'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"批量删除航中外业调查人员记录错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'}), 500

@voyage_personnel_bp.route('/voyage-personnel/upload', methods=['POST'])
def upload_voyage_personnel_attachment():
    """上传航中外业调查人员附件"""
    try:
        print("开始处理附件上传请求")
        print("请求头:", dict(request.headers))
        print("请求文件:", list(request.files.keys()))
        
        # 验证JWT token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            print("未提供有效的认证令牌")
            return jsonify({'code': 401, 'msg': '未提供有效的认证令牌'}), 401
        
        token = token.replace('Bearer ', '')
        payload = verify_token(token)
        if not payload:
            print("认证令牌无效或已过期")
            return jsonify({'code': 401, 'msg': '认证令牌无效或已过期'}), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            print("用户ID无效")
            return jsonify({'code': 401, 'msg': '用户ID无效'}), 401
        
        # 检查是否有文件
        if 'file' not in request.files:
            print("没有选择文件")
            return jsonify({'code': 400, 'msg': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            print("文件名为空")
            return jsonify({'code': 400, 'msg': '没有选择文件'}), 400
        
        print(f"上传文件: {file.filename}, 大小: {len(file.read())}")
        file.seek(0)  # 重置文件指针
        
        # 创建上传目录
        upload_dir = os.path.join(current_app.static_folder, 'uploads', 'voyage_personnel')
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(upload_dir, filename)
        
        # 保存文件
        file.save(filepath)
        
        # 生成文件URL
        file_url = f"http://localhost:5000/static/uploads/voyage_personnel/{filename}"
        
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
        print(f"上传航中外业调查人员附件错误: {str(e)}")
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'}), 500
