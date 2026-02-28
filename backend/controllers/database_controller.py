"""
数据库动态管理控制器 (仅限 super_admin)
"""
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from sqlalchemy import text
from config.database import db
from utils.jwt_utils import token_required
from models import User

database_bp = Blueprint('database', __name__, url_prefix='/api/db')
CORS(database_bp, resources={r"/*": {"origins": "*"}})  # 给这个蓝图单独加上跨域

def check_super_admin(user_id):
    user = User.query.get(user_id)
    if not user or user.role != 'super_admin':
        return False
    return True

@database_bp.route('/tables', methods=['GET'])
@token_required
def get_tables(current_user):
    if not check_super_admin(current_user['user_id']):
        return jsonify({'code': 403, 'message': '无权限访问'}), 403
    
    try:
        result = db.session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return jsonify({'code': 200, 'data': tables})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@database_bp.route('/table/<table_name>', methods=['GET'])
@token_required
def get_table_data(current_user, table_name):
    if not check_super_admin(current_user['user_id']):
        return jsonify({'code': 403, 'message': '无权限访问'}), 403
        
    try:
        # 获取表结构
        columns_result = db.session.execute(text(f"SHOW COLUMNS FROM `{table_name}`"))
        columns = [{'field': row[0], 'type': row[1], 'key': row[3]} for row in columns_result]
        
        # 获取主键列名
        pk_column = next((col['field'] for col in columns if col['key'] == 'PRI'), None)
        if not pk_column and columns:
            pk_column = columns[0]['field']
            
        # 获取数据
        data_result = db.session.execute(text(f"SELECT * FROM `{table_name}` LIMIT 1000"))
        
        # 转换数据格式
        rows = []
        for row in data_result:
            row_dict = {}
            for idx, col in enumerate(columns):
                row_dict[col['field']] = row[idx]
            rows.append(row_dict)
            
        return jsonify({
            'code': 200, 
            'data': {
                'columns': columns,
                'rows': rows,
                'primaryKey': pk_column
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@database_bp.route('/table/<table_name>', methods=['POST'])
@token_required
def insert_table_data(current_user, table_name):
    if not check_super_admin(current_user['user_id']):
        return jsonify({'code': 403, 'message': '无权限访问'}), 403
        
    try:
        data = request.json
        if not data:
            return jsonify({'code': 400, 'message': '数据不能为空'}), 400
            
        columns = '`, `'.join(data.keys())
        placeholders = ', '.join([f":{k}" for k in data.keys()])
        
        sql = f"INSERT INTO `{table_name}` (`{columns}`) VALUES ({placeholders})"
        db.session.execute(text(sql), data)
        db.session.commit()
        
        return jsonify({'code': 200, 'message': '添加成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@database_bp.route('/table/<table_name>/<pk_column>/<pk_value>', methods=['PUT'])
@token_required
def update_table_data(current_user, table_name, pk_column, pk_value):
    if not check_super_admin(current_user['user_id']):
        return jsonify({'code': 403, 'message': '无权限访问'}), 403
        
    try:
        data = request.json
        if not data:
            return jsonify({'code': 400, 'message': '数据不能为空'}), 400
            
        # 不要更新主键
        if pk_column in data:
            del data[pk_column]
            
        set_clause = ', '.join([f"`{k}` = :{k}" for k in data.keys()])
        sql = f"UPDATE `{table_name}` SET {set_clause} WHERE `{pk_column}` = :pk_value"
        
        params = {**data, 'pk_value': pk_value}
        db.session.execute(text(sql), params)
        db.session.commit()
        
        return jsonify({'code': 200, 'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

@database_bp.route('/table/<table_name>/<pk_column>/<pk_value>', methods=['DELETE'])
@token_required
def delete_table_data(current_user, table_name, pk_column, pk_value):
    if not check_super_admin(current_user['user_id']):
        return jsonify({'code': 403, 'message': '无权限访问'}), 403
        
    try:
        sql = f"DELETE FROM `{table_name}` WHERE `{pk_column}` = :pk_value"
        db.session.execute(text(sql), {'pk_value': pk_value})
        db.session.commit()
        
        return jsonify({'code': 200, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500
