"""
外业调查人员资质管理控制器
"""
from flask import Blueprint, request, jsonify, current_app
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models.personnel import PersonnelQualification
from config.database import db
from utils.jwt_utils import token_required

personnel_bp = Blueprint('personnel', __name__, url_prefix='/api')

@personnel_bp.route('/personnel-qualifications', methods=['GET'])
@token_required
def get_personnel_qualifications(current_user):
    """获取外业调查人员资质列表（用户隔离 - JWT认证）"""
    try:
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 获取查询参数
        task_name = request.args.get('task_name')
        name = request.args.get('name')
        
        # 构建查询
        query = PersonnelQualification.query
        
        # 非管理员只能查看自己创建的记录
        if user_role != 'admin':
            query = query.filter(PersonnelQualification.user_id == user_id)
            
        # 按任务名称筛选
        if task_name:
            query = query.filter(PersonnelQualification.task_name == task_name)
            
        # 按人员姓名筛选
        if name:
            query = query.filter(PersonnelQualification.name.like(f'%{name}%'))
            
        # 执行查询
        personnel_list = query.all()
        
        # 转换为字典列表
        result = [personnel.to_dict() for personnel in personnel_list]
        
        return jsonify({
            'code': 200,
            'msg': '获取成功',
            'data': result
        })
    except Exception as e:
        current_app.logger.error(f"获取人员资质列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'获取人员资质列表失败: {str(e)}',
            'data': None
        })

@personnel_bp.route('/personnel-qualifications', methods=['POST'])
@token_required
def create_personnel_qualification(current_user):
    """创建外业调查人员资质记录"""
    try:
        # 从 JWT token 中获取用户ID
        user_id = current_user['user_id']
        
        # 获取请求数据
        data = request.json
        
        # 创建新记录
        personnel = PersonnelQualification.from_dict(data, user_id)
        
        # 保存到数据库
        db.session.add(personnel)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': personnel.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建人员资质记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'创建人员资质记录失败: {str(e)}',
            'data': None
        })

@personnel_bp.route('/personnel-qualifications/<int:personnel_id>', methods=['PUT'])
@token_required
def update_personnel_qualification(current_user, personnel_id):
    """更新外业调查人员资质记录"""
    try:
        # 从 JWT token 中获取用户ID和角色
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 查找记录
        personnel = PersonnelQualification.query.get(personnel_id)
        
        # 检查记录是否存在
        if not personnel:
            return jsonify({
                'code': 404,
                'msg': '记录不存在',
                'data': None
            })
            
        # 检查权限（只有管理员或记录创建者可以修改）
        if user_role != 'admin' and personnel.user_id != user_id:
            return jsonify({
                'code': 403,
                'msg': '无权限修改此记录',
                'data': None
            })
            
        # 获取请求数据
        data = request.json
        
        # 更新字段
        personnel.task_name = data.get('task_name', personnel.task_name)
        personnel.name = data.get('name', personnel.name)
        personnel.sex = data.get('gender', personnel.sex)  # 前端使用gender字段
        
        # 处理日期字段
        birth_date = data.get('birth_date')
        if birth_date:
            if len(birth_date) == 7:  # 只有年月 YYYY-MM
                birth_date = f"{birth_date}-01"  # 添加日期
            personnel.birthdate = datetime.strptime(birth_date, '%Y-%m-%d').date()
            
        personnel.professional_title = data.get('title', personnel.professional_title)  # 前端使用title字段
        personnel.employer = data.get('work_unit', personnel.employer)  # 前端使用work_unit字段
        personnel.specialty = data.get('major', personnel.specialty)  # 前端使用major字段
        personnel.instruments = data.get('instruments', personnel.instruments)
        personnel.training = data.get('training', personnel.training)
        personnel.remarks = data.get('remark', personnel.remarks)  # 前端使用remark字段
        
        # 处理附件列表
        attachment_list = data.get('attachmentList')
        if attachment_list is not None:
            personnel.attachments = json.dumps(attachment_list)
        
        # 保存到数据库
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': personnel.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新人员资质记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'更新人员资质记录失败: {str(e)}',
            'data': None
        })

@personnel_bp.route('/personnel-qualifications/<int:personnel_id>', methods=['DELETE'])
@token_required
def delete_personnel_qualification(current_user, personnel_id):
    """删除外业调查人员资质记录"""
    try:
        # 从 JWT token 中获取用户ID和角色
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 查找记录
        personnel = PersonnelQualification.query.get(personnel_id)
        
        # 检查记录是否存在
        if not personnel:
            return jsonify({
                'code': 404,
                'msg': '记录不存在',
                'data': None
            })
            
        # 检查权限（只有管理员或记录创建者可以删除）
        if user_role != 'admin' and personnel.user_id != user_id:
            return jsonify({
                'code': 403,
                'msg': '无权限删除此记录',
                'data': None
            })
            
        # 删除记录
        db.session.delete(personnel)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '删除成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除人员资质记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'删除人员资质记录失败: {str(e)}',
            'data': None
        })

@personnel_bp.route('/personnel-qualifications/batch', methods=['DELETE'])
@token_required
def batch_delete_personnel_qualifications(current_user):
    """批量删除外业调查人员资质记录"""
    try:
        # 从 JWT token 中获取用户ID和角色
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 获取要删除的ID列表
        data = request.json
        ids = data.get('ids', [])
        
        if not ids:
            return jsonify({
                'code': 400,
                'msg': '未提供要删除的ID列表',
                'data': None
            })
            
        # 查找记录
        personnel_list = PersonnelQualification.query.filter(PersonnelQualification.id.in_(ids)).all()
        
        # 检查权限（只有管理员或记录创建者可以删除）
        if user_role != 'admin':
            for personnel in personnel_list:
                if personnel.user_id != user_id:
                    return jsonify({
                        'code': 403,
                        'msg': f'无权限删除ID为{personnel.id}的记录',
                        'data': None
                    })
                    
        # 删除记录
        for personnel in personnel_list:
            db.session.delete(personnel)
            
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': f'成功删除{len(personnel_list)}条记录',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"批量删除人员资质记录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'批量删除人员资质记录失败: {str(e)}',
            'data': None
        })

@personnel_bp.route('/personnel-qualifications/upload', methods=['POST'])
@token_required
def upload_attachment(current_user):
    """上传附件"""
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
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'personnel_attachments')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{user_id}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)
        
        # 保存文件
        file.save(filepath)
        
        # 生成访问URL
        file_url = f"http://localhost:5000/static/uploads/personnel_attachments/{unique_filename}"
        
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
        current_app.logger.error(f"上传附件失败: {str(e)}")
        return jsonify({
            'code': 500,
            'msg': f'上传附件失败: {str(e)}',
            'data': None
        })
