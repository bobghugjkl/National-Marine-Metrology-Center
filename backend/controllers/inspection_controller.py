"""
航前检查记录控制器
"""
from flask import Blueprint, request, jsonify
from urllib.parse import unquote
from models import PreVoyageInspection
from config.database import db

inspection_bp = Blueprint('inspection', __name__, url_prefix='/api')

@inspection_bp.route('/inspections/task/<task_name>', methods=['GET'])
def get_inspection_by_task(task_name):
    """根据任务名获取检查记录"""
    try:
        decoded_name = unquote(task_name)
        inspection = db.session.get(PreVoyageInspection, decoded_name)
        
        if not inspection:
            return jsonify({'code': 404, 'message': '检查记录不存在'}), 404
        
        return jsonify({
            'code': 200,
            'data': inspection.to_dict()
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@inspection_bp.route('/inspections/<task_name>', methods=['PUT'])
def update_inspection(task_name):
    """更新检查记录"""
    try:
        decoded_name = unquote(task_name)
        inspection = db.session.get(PreVoyageInspection, decoded_name)
        
        if not inspection:
            return jsonify({'code': 404, 'message': '检查记录不存在'}), 404
        
        data = request.json
        for key, value in data.items():
            if key != 'task_name' and hasattr(inspection, key):
                setattr(inspection, key, value)
        
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': '保存成功',
            'data': inspection.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
