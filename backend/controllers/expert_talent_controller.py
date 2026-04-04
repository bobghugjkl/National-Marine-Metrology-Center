"""
专家人才控制器
"""
from flask import Blueprint, request, jsonify, current_app
from config.database import db
from models.expert_talent import ExpertTalent
from utils.jwt_utils import verify_token
import json

expert_talent_bp = Blueprint('expert_talent', __name__, url_prefix='/api')

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

@expert_talent_bp.before_request
def handle_preflight_request():
    if request.method == 'OPTIONS':
        return handle_preflight()

@expert_talent_bp.route('/expert-talent', methods=['GET'])
def get_expert_talent_list():
    """获取专家人才列表"""
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
        name = request.args.get('name', '').strip()
        gender = request.args.get('gender', '').strip()
        job_title = request.args.get('job_title', '').strip()
        work_unit = request.args.get('work_unit', '').strip()
        specialty = request.args.get('specialty', '').strip()
        
        # 构建查询
        query = ExpertTalent.query.filter_by(user_id=user_id)
        
        # 应用筛选条件
        if name:
            query = query.filter(ExpertTalent.name.like(f'%{name}%'))
        if gender:
            query = query.filter(ExpertTalent.gender == gender)
        if job_title:
            query = query.filter(ExpertTalent.job_title.like(f'%{job_title}%'))
        if work_unit:
            query = query.filter(ExpertTalent.work_unit.like(f'%{work_unit}%'))
        if specialty:
            query = query.filter(ExpertTalent.specialty.like(f'%{specialty}%'))
        
        # 分页
        total = query.count()
        experts = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'list': [expert.to_dict() for expert in experts],
                'total': total,
                'page': page,
                'page_size': page_size
            }
        })
        
    except Exception as e:
        current_app.logger.error(f'获取专家人才列表失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@expert_talent_bp.route('/expert-talent', methods=['POST'])
def create_expert_talent():
    """创建专家人才"""
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
        if not data.get('name'):
            return jsonify({'code': 400, 'message': '姓名不能为空'}), 400
        
        # 创建专家人才记录
        expert = ExpertTalent(
            name=data.get('name'),
            gender=data.get('gender', ''),
            birth_date=data.get('birth_date', ''),
            job_title=data.get('job_title', ''),
            work_unit=data.get('work_unit', ''),
            specialty=data.get('specialty', ''),
            contact_info=data.get('contact_info', ''),
            id_number=data.get('id_number', ''),
            bank_card_number=data.get('bank_card_number', ''),
            opening_bank=data.get('opening_bank', ''),
            remarks=data.get('remarks', ''),
            user_id=user_id
        )
        
        db.session.add(expert)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '创建成功',
            'data': expert.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'创建专家人才失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@expert_talent_bp.route('/expert-talent/<int:expert_id>', methods=['PUT'])
def update_expert_talent(expert_id):
    """更新专家人才"""
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
        
        # 查找专家人才记录
        expert = ExpertTalent.query.filter_by(id=expert_id, user_id=user_id).first()
        if not expert:
            return jsonify({'code': 404, 'message': '专家人才不存在'}), 404
        
        # 更新字段
        for key, value in data.items():
            if hasattr(expert, key) and key != 'id' and key != 'user_id':
                setattr(expert, key, value)
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': expert.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'更新专家人才失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@expert_talent_bp.route('/expert-talent/<int:expert_id>', methods=['DELETE'])
def delete_expert_talent(expert_id):
    """删除专家人才"""
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
        
        # 查找专家人才记录
        expert = ExpertTalent.query.filter_by(id=expert_id, user_id=user_id).first()
        if not expert:
            return jsonify({'code': 404, 'message': '专家人才不存在'}), 404
        
        db.session.delete(expert)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'删除专家人才失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@expert_talent_bp.route('/expert-talent/batch-delete', methods=['POST'])
def batch_delete_expert_talent():
    """批量删除专家人才"""
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
        
        expert_ids = data.get('ids', [])
        if not expert_ids:
            return jsonify({'code': 400, 'message': '请选择要删除的记录'}), 400
        
        # 删除选中的专家人才记录
        deleted_count = ExpertTalent.query.filter(
            ExpertTalent.id.in_(expert_ids),
            ExpertTalent.user_id == user_id
        ).delete(synchronize_session=False)
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': f'成功删除 {deleted_count} 条记录'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'批量删除专家人才失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500
