"""
调查人员控制器（只读汇总模块）
联查外业调查人员资质一览表和航中外业调查人员表
"""
from flask import Blueprint, request, jsonify, current_app
from config.database import db
from models.personnel import PersonnelQualification
from models.voyage_personnel import VoyagePersonnel
from utils.jwt_utils import verify_token
from sqlalchemy import text
import json

investigation_personnel_bp = Blueprint('investigation_personnel', __name__, url_prefix='/api')

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

@investigation_personnel_bp.before_request
def handle_preflight_request():
    if request.method == 'OPTIONS':
        return handle_preflight()

@investigation_personnel_bp.route('/investigation-personnel', methods=['GET'])
def get_investigation_personnel_list():
    """获取调查人员列表（联查两个表）"""
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
        sex = request.args.get('sex', '').strip()
        professional_title = request.args.get('professional_title', '').strip()
        employer = request.args.get('employer', '').strip()
        specialty = request.args.get('specialty', '').strip()
        instruments = request.args.get('instruments', '').strip()
        task_name = request.args.get('task_name', '').strip()
        birthdate_start = request.args.get('birthdate_start', '').strip()
        birthdate_end = request.args.get('birthdate_end', '').strip()
        
        # 构建联查SQL - 先获取所有数据，然后在Python中处理合并逻辑
        sql = """
        SELECT 
            'pre_voyage' as source_type,
            id,
            task_name,
            name,
            sex,
            birthdate,
            professional_title,
            employer,
            specialty,
            instruments,
            training,
            remarks,
            attachments,
            user_id,
            create_time,
            update_time
        FROM tb_personnel_qualifications 
        WHERE user_id = :user_id
        
        UNION ALL
        
        SELECT 
            'during_voyage' as source_type,
            id,
            task_name,
            name,
            sex,
            birthdate,
            professional_title,
            employer,
            specialty,
            instruments,
            training,
            remarks,
            attachments,
            user_id,
            create_time,
            update_time
        FROM tb_voyage_personnel 
        WHERE user_id = :user_id
        """
        
        # 添加筛选条件
        where_conditions = []
        params = {'user_id': user_id}
        
        if name:
            where_conditions.append("name LIKE :name")
            params['name'] = f'%{name}%'
        
        if sex:
            where_conditions.append("sex = :sex")
            params['sex'] = sex
            
        if professional_title:
            where_conditions.append("professional_title LIKE :professional_title")
            params['professional_title'] = f'%{professional_title}%'
            
        if employer:
            where_conditions.append("employer LIKE :employer")
            params['employer'] = f'%{employer}%'
            
        if specialty:
            where_conditions.append("specialty LIKE :specialty")
            params['specialty'] = f'%{specialty}%'
            
        if instruments:
            where_conditions.append("instruments LIKE :instruments")
            params['instruments'] = f'%{instruments}%'
            
        if task_name:
            where_conditions.append("task_name LIKE :task_name")
            params['task_name'] = f'%{task_name}%'
            
        if birthdate_start:
            where_conditions.append("birthdate >= :birthdate_start")
            params['birthdate_start'] = birthdate_start
            
        if birthdate_end:
            where_conditions.append("birthdate <= :birthdate_end")
            params['birthdate_end'] = birthdate_end
        
        # 如果有筛选条件，需要重新构建查询
        if where_conditions:
            sql = f"""
            SELECT * FROM (
                {sql}
            ) as combined_data
            WHERE {' AND '.join(where_conditions)}
            """
        
        # 添加排序
        sql += " ORDER BY create_time DESC"
        
        # 执行查询获取所有数据
        result = db.session.execute(text(sql), params).fetchall()
        
        # 处理数据合并逻辑
        personnel_dict = {}
        for row in result:
            key = f"{row.task_name}_{row.name}"  # 使用task_name和name作为唯一键
            
            if key not in personnel_dict:
                personnel_dict[key] = {
                    'id': row.id,
                    'task_name': row.task_name,
                    'name': row.name,
                    'sex': row.sex,
                    'birthdate': row.birthdate.strftime('%Y-%m-%d') if row.birthdate else None,
                    'professional_title': row.professional_title,
                    'employer': row.employer,
                    'specialty': row.specialty,
                    'instruments': row.instruments,
                    'training': row.training,
                    'remarks': row.remarks,
                    'attachments': row.attachments,
                    'user_id': row.user_id,
                    'create_time': row.create_time.strftime('%Y-%m-%d %H:%M:%S') if row.create_time else None,
                    'update_time': row.update_time.strftime('%Y-%m-%d %H:%M:%S') if row.update_time else None,
                    'pre_voyage': False,
                    'during_voyage': False
                }
            
            # 标记数据来源
            if row.source_type == 'pre_voyage':
                personnel_dict[key]['pre_voyage'] = True
            elif row.source_type == 'during_voyage':
                personnel_dict[key]['during_voyage'] = True
        
        # 转换结果并确定数据来源
        all_personnel_list = []
        for key, person in personnel_dict.items():
            # 确定数据来源
            if person['pre_voyage'] and person['during_voyage']:
                person['source_type'] = '航前+航中'
            elif person['pre_voyage']:
                person['source_type'] = '航前'
            elif person['during_voyage']:
                person['source_type'] = '航中'
            else:
                person['source_type'] = '未知'
            
            # 移除临时字段
            del person['pre_voyage']
            del person['during_voyage']
            
            all_personnel_list.append(person)
        
        # 应用筛选条件（在合并后的数据上）
        filtered_list = all_personnel_list
        
        if name and name.strip():
            filtered_list = [p for p in filtered_list if name.lower() in p['name'].lower()]
        if sex and sex.strip():
            filtered_list = [p for p in filtered_list if p['sex'] == sex]
        if professional_title and professional_title.strip():
            filtered_list = [p for p in filtered_list if professional_title.lower() in p['professional_title'].lower()]
        if employer and employer.strip():
            filtered_list = [p for p in filtered_list if employer.lower() in p['employer'].lower()]
        if specialty and specialty.strip():
            filtered_list = [p for p in filtered_list if specialty.lower() in p['specialty'].lower()]
        if instruments and instruments.strip():
            filtered_list = [p for p in filtered_list if instruments.lower() in (p['instruments'] or '').lower()]
        if task_name and task_name.strip():
            filtered_list = [p for p in filtered_list if task_name.lower() in p['task_name'].lower()]
        if birthdate_start and birthdate_start.strip():
            filtered_list = [p for p in filtered_list if p['birthdate'] and p['birthdate'] >= birthdate_start]
        if birthdate_end and birthdate_end.strip():
            filtered_list = [p for p in filtered_list if p['birthdate'] and p['birthdate'] <= birthdate_end]
        
        # 获取总数
        total = len(filtered_list)
        
        # 应用分页
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        personnel_list = filtered_list[start_index:end_index]
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'list': personnel_list,
                'total': total,
                'page': page,
                'page_size': page_size
            }
        })
        
    except Exception as e:
        current_app.logger.error(f'获取调查人员列表失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500

@investigation_personnel_bp.route('/investigation-personnel/export', methods=['GET'])
def export_investigation_personnel():
    """导出调查人员数据"""
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
        
        # 获取所有数据（不分页）
        sql = """
        SELECT 
            'pre_voyage' as source_type,
            task_name,
            name,
            sex,
            birthdate,
            professional_title,
            employer,
            specialty,
            instruments,
            training,
            remarks
        FROM tb_personnel_qualifications 
        WHERE user_id = :user_id
        
        UNION ALL
        
        SELECT 
            'during_voyage' as source_type,
            task_name,
            name,
            sex,
            birthdate,
            professional_title,
            employer,
            specialty,
            instruments,
            training,
            remarks
        FROM tb_voyage_personnel 
        WHERE user_id = :user_id
        
        ORDER BY create_time DESC
        """
        
        result = db.session.execute(text(sql), {'user_id': user_id}).fetchall()
        
        # 转换结果
        export_data = []
        for row in result:
            export_data.append({
                '航次名称': row.task_name,
                '姓名': row.name,
                '性别': row.sex,
                '出生年月': row.birthdate.strftime('%Y-%m-%d') if row.birthdate else '',
                '职称': row.professional_title,
                '工作单位': row.employer,
                '从事专业': row.specialty,
                '操作仪器': row.instruments,
                '培训情况': row.training,
                '备注': row.remarks,
                '数据来源': '航前' if row.source_type == 'pre_voyage' else '航中'
            })
        
        return jsonify({
            'code': 200,
            'message': '导出成功',
            'data': export_data
        })
        
    except Exception as e:
        current_app.logger.error(f'导出调查人员数据失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'服务器内部错误: {str(e)}'}), 500
