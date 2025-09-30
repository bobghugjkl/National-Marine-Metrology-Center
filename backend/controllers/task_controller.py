"""
任务管理控制器
"""
from flask import Blueprint, request, jsonify
from urllib.parse import unquote
from models import TaskInfo, PreVoyageInspection
from config.database import db

task_bp = Blueprint('task', __name__, url_prefix='/api')

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """获取任务列表（用户隔离）"""
    try:
        # 从请求头或参数获取当前用户ID
        user_id = request.args.get('user_id') or request.headers.get('X-User-ID')
        
        if user_id:
            # 只返回当前用户的任务
            tasks = TaskInfo.query.filter_by(user_id=int(user_id)).all()
        else:
            # 如果没有提供user_id，返回所有任务（向后兼容）
            tasks = TaskInfo.query.all()
        
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
def create_task():
    """创建任务（同时创建检查记录）"""
    try:
        data = request.json
        # 从请求头或参数获取当前用户ID
        user_id = data.get('user_id') or request.headers.get('X-User-ID') or 3  # 默认为ID=3的用户
        
        new_task = TaskInfo(
            task_name=data.get('task_name'),
            project=data.get('project'),
            participant=data.get('participant', ''),
            chief_scientist=data.get('chief_scientist', ''),
            superintendent=data.get('superintendent', ''),
            superintended=data.get('superintended', ''),
            executiontime=data.get('executiontime', ''),
            subject=data.get('subject', ''),
            user_id=int(user_id)  # 关联到当前用户
        )
        db.session.add(new_task)
        
        # 自动创建对应的检查记录
        new_inspection = PreVoyageInspection(
            task_name=data.get('task_name'),
            check_date='',
            superintendent=data.get('superintendent', ''),
            superintended=data.get('superintended', ''),
            user_id=int(user_id)  # 关联到当前用户
        )
        db.session.add(new_inspection)
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '创建成功', 'data': new_task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@task_bp.route('/tasks/<task_name>', methods=['PUT'])
def update_task(task_name):
    """更新任务"""
    try:
        decoded_name = unquote(task_name)
        task = db.session.get(TaskInfo, decoded_name)
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
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
def delete_task(task_name):
    """删除任务（同时删除检查记录）"""
    try:
        decoded_name = unquote(task_name)
        task = db.session.get(TaskInfo, decoded_name)
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        # 删除对应的检查记录
        inspection = db.session.get(PreVoyageInspection, decoded_name)
        if inspection:
            db.session.delete(inspection)
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
