#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务管理路由
"""

from flask import Blueprint, request, jsonify
from models_task import db, TaskInfo
from models_inspection import PreVoyageInspection as PreInspectionRecord

# 创建蓝图
task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')

# 获取所有任务（支持搜索）
@task_bp.route('', methods=['GET'])
def get_tasks():
    try:
        # 获取搜索参数
        task_name = request.args.get('task_name', '')
        
        # 如果有搜索条件，则按任务名称模糊搜索
        if task_name:
            tasks = TaskInfo.query.filter(TaskInfo.task_name.like(f'%{task_name}%')).all()
        else:
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

# 创建新任务
@task_bp.route('', methods=['POST'])
def create_task():
    try:
        data = request.json
        
        # 检查任务名称是否已存在
        existing_task = TaskInfo.query.filter_by(task_name=data.get('task_name')).first()
        if existing_task:
            return jsonify({'code': 400, 'message': '任务名称已存在'}), 400
        
        # 创建新任务
        new_task = TaskInfo(
            task_name=data.get('task_name'),
            project=data.get('project'),
            task_code=data.get('task_code'),
            undertake=data.get('undertake'),
            participant=data.get('participant'),
            ship=data.get('ship'),
            leader=data.get('leader'),
            chief_scientist=data.get('chief_scientist'),
            superintendent=data.get('superintendent'),
            superintended=data.get('superintended'),
            executiontime=data.get('executiontime'),
            subject=data.get('subject')
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        # 自动创建对应的检查记录（初始为空）
        try:
            new_inspection = PreInspectionRecord(task_name=data.get('task_name'))
            db.session.add(new_inspection)
            db.session.commit()
        except Exception as e:
            print(f'创建检查记录失败: {e}')
        
        return jsonify({
            'code': 200,
            'message': '创建成功',
            'data': new_task.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

# 更新任务
@task_bp.route('/<task_name>', methods=['PUT'])
def update_task(task_name):
    try:
        task = TaskInfo.query.filter_by(task_name=task_name).first()
        
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        data = request.json
        
        # 更新字段
        if 'project' in data:
            task.project = data['project']
        if 'task_code' in data:
            task.task_code = data['task_code']
        if 'undertake' in data:
            task.undertake = data['undertake']
        if 'participant' in data:
            task.participant = data['participant']
        if 'ship' in data:
            task.ship = data['ship']
        if 'leader' in data:
            task.leader = data['leader']
        if 'chief_scientist' in data:
            task.chief_scientist = data['chief_scientist']
        if 'superintendent' in data:
            task.superintendent = data['superintendent']
        if 'superintended' in data:
            task.superintended = data['superintended']
        if 'executiontime' in data:
            task.executiontime = data['executiontime']
        if 'subject' in data:
            task.subject = data['subject']
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': task.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

# 删除任务
@task_bp.route('/<task_name>', methods=['DELETE'])
def delete_task(task_name):
    try:
        task = TaskInfo.query.filter_by(task_name=task_name).first()
        
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        # 同时删除对应的检查记录
        try:
            inspection = PreInspectionRecord.query.get(task_name)
            if inspection:
                db.session.delete(inspection)
        except Exception as e:
            print(f'删除检查记录失败: {e}')
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
