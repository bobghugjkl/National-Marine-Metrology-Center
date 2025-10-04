"""
航前检查记录控制器
"""
from flask import Blueprint, request, jsonify
from urllib.parse import unquote
from models import PreVoyageInspection
from config.database import db
from utils.jwt_utils import token_required

inspection_bp = Blueprint('inspection', __name__, url_prefix='/api')

@inspection_bp.route('/inspections/task/<task_name>', methods=['GET'])
@token_required
def get_inspection_by_task(current_user, task_name):
    """根据任务名获取检查记录（JWT认证 + 权限验证）"""
    try:
        decoded_name = unquote(task_name)
        inspection = db.session.get(PreVoyageInspection, decoded_name)

        if not inspection:
            return jsonify({'code': 404, 'message': '检查记录不存在'}), 404

        user_id = current_user['user_id']
        user_role = current_user['role']

        # 验证权限：只能查看自己的检查记录（管理员除外）
        if inspection.user_id != user_id and user_role not in ['super_admin', '管理员']:
            return jsonify({'code': 403, 'message': '无权查看其他用户的检查记录'}), 403

        return jsonify({
            'code': 200,
            'data': inspection.to_dict()
        })
    except Exception as e:
        import traceback
        print(f'获取检查记录时出错: {e}')
        print(f'错误详情: {traceback.format_exc()}')
        return jsonify({'code': 500, 'message': str(e)}), 500

@inspection_bp.route('/inspections/<task_name>', methods=['PUT'])
@token_required
def update_inspection(current_user, task_name):
    """更新检查记录（JWT认证 + 权限验证）"""
    try:
        decoded_name = unquote(task_name)
        inspection = db.session.get(PreVoyageInspection, decoded_name)

        if not inspection:
            return jsonify({'code': 404, 'message': '检查记录不存在'}), 404

        user_id = current_user['user_id']
        user_role = current_user['role']

        # 验证权限：只能修改自己的检查记录（管理员除外）
        if inspection.user_id != user_id and user_role not in ['super_admin', '管理员']:
            return jsonify({'code': 403, 'message': '无权修改其他用户的检查记录'}), 403

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
        import traceback
        print(f'更新检查记录时出错: {e}')
        print(f'错误详情: {traceback.format_exc()}')
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
