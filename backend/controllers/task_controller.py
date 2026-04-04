"""
任务管理控制器
"""
from flask import Blueprint, request, jsonify
from urllib.parse import unquote
from models import TaskInfo, PreVoyageInspection, User
from config.database import db
from utils.jwt_utils import token_required

task_bp = Blueprint('task', __name__, url_prefix='/api')

@task_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    """获取任务列表（用户隔离 - JWT认证，支持按任务名称模糊搜索）"""
    try:
        # 从 JWT token 中获取用户ID与角色
        user_id = current_user['user_id']
        user_role = current_user['role']

        # 查询参数
        task_name = request.args.get('task_name', type=str)

        # 基础查询（管理员、中心管理员可看全部，项目管理员看本公司全部，否则仅看本人）
        if user_role in ['super_admin', '管理员', '中心管理员']:
            query = TaskInfo.query
        elif user_role == '项目管理员':
            # 获取当前用户的公司信息
            curr_user_obj = User.query.get(user_id)
            if curr_user_obj and curr_user_obj.company:
                # 查询该公司下的所有用户的 user_id
                company_users = User.query.filter_by(company=curr_user_obj.company).all()
                company_user_ids = [u.id for u in company_users]
                query = TaskInfo.query.filter(TaskInfo.user_id.in_(company_user_ids))
            else:
                # 如果没有公司信息，退级为只看本人
                query = TaskInfo.query.filter_by(user_id=user_id)
        else:
            query = TaskInfo.query.filter_by(user_id=user_id)

        # 按任务名称模糊搜索
        if task_name:
            query = query.filter(TaskInfo.task_name.like(f"%{task_name}%"))

        tasks = query.all()

        task_list = [t.to_dict() for t in tasks]
        return jsonify({
            'code': 200,
            'data': {
                'list': task_list,
                'pageTotal': len(task_list)
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@task_bp.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    """创建任务（同时创建检查记录 - JWT认证）"""
    try:
        data = request.json
        print(f'创建任务，接收到的数据: {data}')
        
        # 从 JWT token 中获取用户ID（安全，无法伪造）
        user_id = current_user['user_id']
        
        task_name = data.get('task_name')
        print(f'任务名称: {task_name}')
        
        # 检查任务是否已存在
        existing_task = db.session.get(TaskInfo, task_name)
        if existing_task:
            print(f'任务已存在: {task_name}')
            return jsonify({'code': 400, 'message': f'任务"{task_name}"已存在，请使用不同的任务名称'}), 400
        
        new_task = TaskInfo(
            task_name=task_name,
            project=data.get('project', ''),
            task_code=data.get('task_code', ''),
            undertake=data.get('undertake', ''),
            participant=data.get('participant', ''),
            ship=data.get('ship', ''),
            leader=data.get('leader', ''),
            chief_scientist=data.get('chief_scientist', ''),
            superintendent=data.get('superintendent', ''),
            superintended=data.get('superintended', ''),
            executiontime=data.get('executiontime', ''),
            subject=data.get('subject', ''),
            user_id=user_id  # 使用 token 中的用户ID
        )
        db.session.add(new_task)
        print(f'任务已添加到会话: {task_name}')
        
        # 检查检查记录是否已存在
        existing_inspection = db.session.get(PreVoyageInspection, task_name)
        if existing_inspection:
            print(f'检查记录已存在，跳过创建: {task_name}')
        else:
            # 自动创建对应的检查记录
            new_inspection = PreVoyageInspection(
                task_name=task_name,
                check_date='',
                superintendent=data.get('superintendent', ''),
                superintended=data.get('superintended', ''),
                user_id=user_id  # 使用 token 中的用户ID
            )
            db.session.add(new_inspection)
            print(f'检查记录已添加到会话: {task_name}')
        
        db.session.commit()
        print(f'任务创建成功: {task_name}')
        return jsonify({'code': 200, 'message': '创建成功', 'data': new_task.to_dict()})
    except Exception as e:
        import traceback
        print(f'创建任务时出错: {e}')
        print(f'错误详情: {traceback.format_exc()}')
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@task_bp.route('/tasks/<task_name>', methods=['PUT'])
@token_required
def update_task(current_user, task_name):
    """更新任务（JWT认证 + 权限验证）"""
    try:
        decoded_name = unquote(task_name)
        task = db.session.get(TaskInfo, decoded_name)
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 验证权限：只能修改自己的任务（管理员可改所有，中心/项目管理员可改本公司成员的任务）
        can_edit = False
        if task.user_id == user_id or user_role in ['super_admin', '管理员']:
            can_edit = True
        elif user_role in ['中心管理员', '项目管理员']:
            curr_user_obj = User.query.get(user_id)
            task_owner_obj = User.query.get(task.user_id)
            if curr_user_obj and task_owner_obj and curr_user_obj.company == task_owner_obj.company:
                can_edit = True
                
        if not can_edit:
            return jsonify({'code': 403, 'message': '无权修改其他用户的任务'}), 403
        
        data = request.json
        for key, value in data.items():
            if key not in ['task_name', 'user_id'] and hasattr(task, key):  # 禁止修改 user_id
                setattr(task, key, value)
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@task_bp.route('/tasks/<task_name>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_name):
    """删除任务（同时删除检查记录 - JWT认证 + 权限验证）"""
    try:
        decoded_name = unquote(task_name)
        print(f'尝试删除任务: {decoded_name}')
        task = db.session.get(TaskInfo, decoded_name)
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 验证权限：只能删除自己的任务（管理员可删所有，中心/项目管理员可删本公司成员的任务）
        can_delete = False
        if task.user_id == user_id or user_role in ['super_admin', '管理员']:
            can_delete = True
        elif user_role in ['中心管理员', '项目管理员']:
            curr_user_obj = User.query.get(user_id)
            task_owner_obj = User.query.get(task.user_id)
            if curr_user_obj and task_owner_obj and curr_user_obj.company == task_owner_obj.company:
                can_delete = True
                
        if not can_delete:
            return jsonify({'code': 403, 'message': '无权删除其他用户的任务'}), 403
        
        # 删除对应的检查记录
        inspection = db.session.get(PreVoyageInspection, decoded_name)
        if inspection:
            db.session.delete(inspection)
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
