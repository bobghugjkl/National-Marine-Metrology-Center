"""
航前质量监督检查记录表 API 路由
"""
from flask import Blueprint, request, jsonify
from models_inspection import db, PreVoyageInspection as PreInspectionRecord
from urllib.parse import unquote

inspection_bp = Blueprint('inspection_bp', __name__, url_prefix='/api/inspections')

# ==================== 检查记录 CRUD ====================

@inspection_bp.route('', methods=['GET'])
def get_inspections():
    """获取所有检查记录（与任务关联）"""
    try:
        inspections = PreInspectionRecord.query.all()
        inspection_list = [i.to_dict() for i in inspections]
        return jsonify({
            'code': 200,
            'data': {
                'list': inspection_list,
                'pageTotal': len(inspection_list)
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500


@inspection_bp.route('/<task_name>', methods=['GET'])
def get_inspection_by_task(task_name):
    """根据任务名称获取检查记录"""
    try:
        decoded_task_name = unquote(task_name)
        inspection = PreInspectionRecord.query.get(decoded_task_name)
        
        if not inspection:
            return jsonify({'code': 404, 'message': '未找到该任务的检查记录'}), 404
        
        return jsonify({
            'code': 200,
            'data': inspection.to_dict()
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500


@inspection_bp.route('/<task_name>', methods=['PUT'])
def update_inspection(task_name):
    """更新检查记录（只允许编辑，不允许修改 task_name）"""
    try:
        decoded_task_name = unquote(task_name)
        inspection = PreInspectionRecord.query.get(decoded_task_name)
        
        if not inspection:
            return jsonify({'code': 404, 'message': '未找到该任务的检查记录'}), 404
        
        data = request.json
        
        # task_name 作为主键，不允许修改
        if 'task_name' in data and data['task_name'] != decoded_task_name:
            return jsonify({'code': 400, 'message': '任务名称（主键）不允许修改'}), 400
        
        # 更新所有可编辑字段
        for key, value in data.items():
            if key != 'task_name' and hasattr(inspection, key):
                setattr(inspection, key, value)
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '检查记录更新成功',
            'data': inspection.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500


@inspection_bp.route('', methods=['POST'])
def create_inspection():
    """创建检查记录（自动创建，一般由任务创建时触发）"""
    try:
        data = request.json
        task_name = data.get('task_name')
        
        if not task_name:
            return jsonify({'code': 400, 'message': '任务名称不能为空'}), 400
        
        # 检查是否已存在
        existing = PreInspectionRecord.query.get(task_name)
        if existing:
            return jsonify({'code': 400, 'message': '该任务的检查记录已存在'}), 400
        
        # 创建新记录（默认所有字段为空）
        new_inspection = PreInspectionRecord(task_name=task_name)
        
        db.session.add(new_inspection)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '检查记录创建成功',
            'data': new_inspection.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500


@inspection_bp.route('/<task_name>', methods=['DELETE'])
def delete_inspection(task_name):
    """删除检查记录（自动删除，一般由任务删除时触发）"""
    try:
        decoded_task_name = unquote(task_name)
        inspection = PreInspectionRecord.query.get(decoded_task_name)
        
        if not inspection:
            return jsonify({'code': 404, 'message': '未找到该任务的检查记录'}), 404
        
        db.session.delete(inspection)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '检查记录删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
