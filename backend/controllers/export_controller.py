"""
导出数据包控制器
负责生成任务相关的所有表单数据包（Excel和Word文档）
"""
import os
import zipfile
import tempfile
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from config.database import db
from models import TaskInfo, PersonnelQualification, Equipment, InvestigationProject, VoyagePersonnel, VoyageEquipment, VoyageInvestigationProject, SupervisorLog, OriginalRecords, ProcedureExecution, WorkLog, SampleStorage, PostInspection, PreSummary, OnboardInspection, PreVoyageInspection
from utils.jwt_utils import token_required
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

export_bp = Blueprint('export', __name__, url_prefix='/api/export')

def create_empty_excel(temp_dir, filename, headers, title):
    """创建空Excel表格"""
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = title
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
    except Exception as e:
        print(f"创建空表格失败: {e}")
        return None

def handle_preflight():
    """处理CORS预检请求"""
    response = jsonify({'message': 'OK'})
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@export_bp.before_request
def handle_preflight_request():
    if request.method == 'OPTIONS':
        return handle_preflight()

@export_bp.route('/data-package/<task_name>', methods=['GET'])
def export_data_package(task_name):
    """
    导出任务数据包
    生成包含所有表单的压缩包
    """
    try:
        # 手动检查认证
        from utils.jwt_utils import verify_token
        from flask import request as flask_request
        
        # 获取Authorization头
        auth_header = flask_request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'code': 401, 'message': '未找到Authorization头'}), 401
        
        token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'code': 401, 'message': 'Token为空'}), 401
        
        # 验证token
        current_user = verify_token(token)
        if not current_user:
            return jsonify({'code': 401, 'message': 'Token无效'}), 401
        
        print(f"开始导出任务数据包: {task_name}, 用户ID: {current_user.get('user_id')}")
        
        # 获取任务信息
        task = TaskInfo.query.filter_by(task_name=task_name, user_id=current_user.get('user_id')).first()
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        
        # 生成各种表单文件
        files_created = []
        
        # 1. 航前检查表单
        print("开始生成航前检查表单...")
        pre_voyage_files = generate_pre_voyage_forms(task, temp_dir)
        print(f"航前检查表单生成完成，文件数量: {len(pre_voyage_files)}")
        files_created.extend(pre_voyage_files)
        
        # 2. 航中检查表单
        print("开始生成航中检查表单...")
        during_voyage_files = generate_during_voyage_forms(task, temp_dir)
        print(f"航中检查表单生成完成，文件数量: {len(during_voyage_files)}")
        files_created.extend(during_voyage_files)
        
        # 3. 航后检查表单
        print("开始生成航后检查表单...")
        post_voyage_files = generate_post_voyage_forms(task, temp_dir)
        print(f"航后检查表单生成完成，文件数量: {len(post_voyage_files)}")
        files_created.extend(post_voyage_files)
        
        print(f"总共生成文件数量: {len(files_created)}")
        for i, file_path in enumerate(files_created):
            print(f"文件 {i+1}: {file_path}")
        
        # 创建压缩包
        zip_filename = f"{task_name}_数据包_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_created:
                if os.path.exists(file_path):
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
        
        # 返回文件
        from flask import make_response
        response = make_response(send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        ))
        
        # 添加CORS头
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'导出失败: {str(e)}'}), 500

def generate_pre_voyage_forms(task, temp_dir):
    """生成航前检查相关表单"""
    files = []
    
    # 1. 外业调查人员资质一览表
    print("生成外业调查人员资质一览表...")
    personnel_file = generate_personnel_qualification_excel(task, temp_dir)
    if personnel_file:
        files.append(personnel_file)
        print(f"✓ 外业调查人员资质一览表生成成功: {personnel_file}")
    else:
        print("✗ 外业调查人员资质一览表生成失败")
    
    # 2. 仪器设备一览表
    print("生成仪器设备一览表...")
    equipment_file = generate_equipment_excel(task, temp_dir)
    if equipment_file:
        files.append(equipment_file)
        print(f"✓ 仪器设备一览表生成成功: {equipment_file}")
    else:
        print("✗ 仪器设备一览表生成失败")
    
    # 3. 外业调查项目统计表
    print("生成外业调查项目统计表...")
    investigation_file = generate_investigation_excel(task, temp_dir)
    if investigation_file:
        files.append(investigation_file)
        print(f"✓ 外业调查项目统计表生成成功: {investigation_file}")
    else:
        print("✗ 外业调查项目统计表生成失败")
    
    # 4. 航前质量监督检查记录
    print("生成航前质量监督检查记录...")
    pre_voyage_inspection_file = generate_pre_voyage_inspection_excel(task, temp_dir)
    if pre_voyage_inspection_file:
        files.append(pre_voyage_inspection_file)
        print(f"✓ 航前质量监督检查记录生成成功: {pre_voyage_inspection_file}")
    else:
        print("✗ 航前质量监督检查记录生成失败")
    
    # 5. 航前质量监督情况汇总
    print("生成航前质量监督情况汇总...")
    pre_summary_file = generate_pre_summary_excel(task, temp_dir)
    if pre_summary_file:
        files.append(pre_summary_file)
        print(f"✓ 航前质量监督情况汇总生成成功: {pre_summary_file}")
    else:
        print("✗ 航前质量监督情况汇总生成失败")
    
    print(f"航前检查表单生成完成，共{len(files)}个文件")
    return files

def generate_during_voyage_forms(task, temp_dir):
    """生成航中检查相关表单"""
    files = []
    
    # 1. 外业调查人员资质一览表(航中)
    print("生成外业调查人员资质一览表(航中)...")
    voyage_personnel_file = generate_voyage_personnel_excel(task, temp_dir)
    if voyage_personnel_file:
        files.append(voyage_personnel_file)
        print(f"✓ 外业调查人员资质一览表(航中)生成成功: {voyage_personnel_file}")
    else:
        print("✗ 外业调查人员资质一览表(航中)生成失败")
    
    # 2. 仪器设备(工作计量器具)一览表(航中)
    print("生成仪器设备(工作计量器具)一览表(航中)...")
    voyage_equipment_file = generate_voyage_equipment_excel(task, temp_dir)
    if voyage_equipment_file:
        files.append(voyage_equipment_file)
        print(f"✓ 仪器设备(工作计量器具)一览表(航中)生成成功: {voyage_equipment_file}")
    else:
        print("✗ 仪器设备(工作计量器具)一览表(航中)生成失败")
    
    # 3. 外业调查项目/仪器比测统计表(航中)
    print("生成外业调查项目/仪器比测统计表(航中)...")
    voyage_investigation_file = generate_voyage_investigation_excel(task, temp_dir)
    if voyage_investigation_file:
        files.append(voyage_investigation_file)
        print(f"✓ 外业调查项目/仪器比测统计表(航中)生成成功: {voyage_investigation_file}")
    else:
        print("✗ 外业调查项目/仪器比测统计表(航中)生成失败")
    
    # 4. 监督员日志
    print("生成监督员日志...")
    supervisor_log_file = generate_supervisor_log_excel(task, temp_dir)
    if supervisor_log_file:
        files.append(supervisor_log_file)
        print(f"✓ 监督员日志生成成功: {supervisor_log_file}")
    else:
        print("✗ 监督员日志生成失败")
    
    # 5. 外业调查原始记录抽查表
    print("生成外业调查原始记录抽查表...")
    original_records_file = generate_original_records_excel(task, temp_dir)
    if original_records_file:
        files.append(original_records_file)
        print(f"✓ 外业调查原始记录抽查表生成成功: {original_records_file}")
    else:
        print("✗ 外业调查原始记录抽查表生成失败")
    
    # 6. 外业调查操作规程执行统计表
    print("生成外业调查操作规程执行统计表...")
    procedure_execution_file = generate_procedure_execution_excel(task, temp_dir)
    if procedure_execution_file:
        files.append(procedure_execution_file)
        print(f"✓ 外业调查操作规程执行统计表生成成功: {procedure_execution_file}")
    else:
        print("✗ 外业调查操作规程执行统计表生成失败")
    
    # 7. 外业调查工作日志抽查表
    print("生成外业调查工作日志抽查表...")
    work_log_file = generate_work_log_excel(task, temp_dir)
    if work_log_file:
        files.append(work_log_file)
        print(f"✓ 外业调查工作日志抽查表生成成功: {work_log_file}")
    else:
        print("✗ 外业调查工作日志抽查表生成失败")
    
    # 8. 外业调查样品储存记录抽查表
    print("生成外业调查样品储存记录抽查表...")
    sample_storage_file = generate_sample_storage_excel(task, temp_dir)
    if sample_storage_file:
        files.append(sample_storage_file)
        print(f"✓ 外业调查样品储存记录抽查表生成成功: {sample_storage_file}")
    else:
        print("✗ 外业调查样品储存记录抽查表生成失败")
    
    # 9. 随船质量监督检查表
    print("生成随船质量监督检查表...")
    onboard_inspection_file = generate_onboard_inspection_excel(task, temp_dir)
    if onboard_inspection_file:
        files.append(onboard_inspection_file)
        print(f"✓ 随船质量监督检查表生成成功: {onboard_inspection_file}")
    else:
        print("✗ 随船质量监督检查表生成失败")
    
    print(f"航中检查表单生成完成，共{len(files)}个文件")
    return files

def generate_post_voyage_forms(task, temp_dir):
    """生成航后检查相关表单"""
    files = []
    
    # 1. 航后检查表
    print("生成航后检查表...")
    post_inspection_file = generate_post_inspection_excel(task, temp_dir)
    if post_inspection_file:
        files.append(post_inspection_file)
        print(f"✓ 航后检查表生成成功: {post_inspection_file}")
    else:
        print("✗ 航后检查表生成失败")
    
    print(f"航后检查表单生成完成，共{len(files)}个文件")
    return files

def generate_personnel_qualification_excel(task, temp_dir):
    """生成人员资质Excel表"""
    try:
        # 获取人员资质数据
        personnel_data = PersonnelQualification.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not personnel_data:
            print(f"未找到人员资质数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 创建空表格
            filename = f"外业调查人员资质一览表_{task.task_name}.xlsx"
            headers = ['序号', '姓名', '性别', '出生年月', '职称', '工作单位', '从事专业', '本航次操作仪器', '培训情况', '备注']
            return create_empty_excel(temp_dir, filename, headers, "外业调查人员资质一览表")
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查人员资质一览表"
        
        # 设置表头
        headers = [
            '序号', '姓名', '性别', '出生年月', '职称', '工作单位', 
            '从事专业', '本航次操作仪器', '培训情况', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, personnel in enumerate(personnel_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=personnel.name)
            ws.cell(row=row, column=3, value=personnel.sex)
            ws.cell(row=row, column=4, value=personnel.birthdate.strftime('%Y-%m') if personnel.birthdate else '')
            ws.cell(row=row, column=5, value=personnel.professional_title)
            ws.cell(row=row, column=6, value=personnel.employer)
            ws.cell(row=row, column=7, value=personnel.specialty)
            ws.cell(row=row, column=8, value=personnel.instruments or '')
            ws.cell(row=row, column=9, value=personnel.training or '')
            ws.cell(row=row, column=10, value=personnel.remarks or '')
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"外业调查人员资质一览表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成人员资质表失败: {e}")
        # 即使出错也创建空表格
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "外业调查人员资质一览表"
            
            headers = ['序号', '姓名', '性别', '出生年月', '职称', '工作单位', '从事专业', '本航次操作仪器', '培训情况', '备注']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            filename = f"外业调查人员资质一览表_{task.task_name}.xlsx"
            filepath = os.path.join(temp_dir, filename)
            wb.save(filepath)
            return filepath
        except Exception as e2:
            print(f"创建空人员资质表也失败: {e2}")
            return None

def generate_equipment_excel(task, temp_dir):
    """生成设备Excel表"""
    try:
        # 获取设备数据
        print(f"查询设备数据，任务: {task.task_name}, 用户ID: {task.user_id}")
        equipment_data = Equipment.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        print(f"查询到设备数据数量: {len(equipment_data)}")
        for i, equipment in enumerate(equipment_data):
            print(f"设备 {i+1}: {equipment.name} - {equipment.model}")
        
        if not equipment_data:
            print(f"未找到设备数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 创建空表格
            filename = f"仪器设备一览表_{task.task_name}.xlsx"
            headers = ['序号', '仪器(标准物质)名称', '型号', '编号', '量值溯源方式', '检定/校准日期', '有效期', '检定/校准机构', '备注']
            return create_empty_excel(temp_dir, filename, headers, "仪器设备一览表")
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "仪器设备一览表"
        
        # 设置表头
        headers = [
            '序号', '仪器(标准物质)名称', '型号', '编号', '量值溯源方式', 
            '检定/校准日期', '有效期', '检定/校准机构', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, equipment in enumerate(equipment_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=equipment.name or '')  # 仪器（标准物质）名称
            ws.cell(row=row, column=3, value=equipment.model or '')  # 型号
            ws.cell(row=row, column=4, value=equipment.number or '')  # 编号
            ws.cell(row=row, column=5, value=equipment.traceability_method or '')  # 量值溯源方式
            ws.cell(row=row, column=6, value=equipment.calibration_date or '')  # 检定/校准日期
            ws.cell(row=row, column=7, value=equipment.validity_period or '')  # 有效期
            ws.cell(row=row, column=8, value=equipment.calibration_organization or '')  # 检定/校准机构
            ws.cell(row=row, column=9, value=equipment.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"仪器设备一览表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成设备表失败: {e}")
        # 即使出错也创建空表格
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "仪器设备一览表"
            
            headers = ['序号', '设备名称', '型号规格', '出厂编号', '制造厂家', '检定/校准日期', '有效期', '检定/校准机构', '备注']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            filename = f"仪器设备一览表_{task.task_name}.xlsx"
            filepath = os.path.join(temp_dir, filename)
            wb.save(filepath)
            return filepath
        except Exception as e2:
            print(f"创建空设备表也失败: {e2}")
            return None

def generate_investigation_excel(task, temp_dir):
    """生成调查项目Excel表"""
    try:
        # 获取调查项目数据
        investigation_data = InvestigationProject.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not investigation_data:
            print(f"未找到调查项目数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 创建空表格
            filename = f"外业调查项目统计表_{task.task_name}.xlsx"
            headers = ['序号', '项目名称', '仪器设备', '比测情况', '备注']
            return create_empty_excel(temp_dir, filename, headers, "外业调查项目统计表")
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查项目统计表"
        
        # 设置表头
        headers = [
            '序号', '项目名称', '仪器设备', '比测情况', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, project in enumerate(investigation_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=project.investigation_item or '')  # 调查项目/仪器
            ws.cell(row=row, column=3, value=project.unit_a_instrument or '')  # 比测单位甲仪器
            ws.cell(row=row, column=4, value=project.comparison_result or '')  # 比测结果
            ws.cell(row=row, column=5, value=project.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 20
        
        # 保存文件
        filename = f"外业调查项目统计表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成调查项目表失败: {e}")
        return None

def generate_voyage_personnel_excel(task, temp_dir):
    """生成航中人员资质Excel表"""
    try:
        # 获取航中人员数据
        voyage_personnel_data = VoyagePersonnel.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not voyage_personnel_data:
            print(f"未找到航中人员数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            voyage_personnel_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查人员资质一览表(航中)"
        
        # 设置表头
        headers = [
            '序号', '姓名', '性别', '出生年月', '职称', '工作单位', 
            '从事专业', '本航次操作仪器', '培训情况', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, personnel in enumerate(voyage_personnel_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=personnel.name)
            ws.cell(row=row, column=3, value=personnel.sex)
            ws.cell(row=row, column=4, value=personnel.birthdate.strftime('%Y-%m') if personnel.birthdate else '')
            ws.cell(row=row, column=5, value=personnel.professional_title)
            ws.cell(row=row, column=6, value=personnel.employer)
            ws.cell(row=row, column=7, value=personnel.specialty)
            ws.cell(row=row, column=8, value=personnel.instruments or '')
            ws.cell(row=row, column=9, value=personnel.training or '')
            ws.cell(row=row, column=10, value=personnel.remarks or '')
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"外业调查人员资质一览表(航中)_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航中人员资质表失败: {e}")
        return None

def generate_voyage_equipment_excel(task, temp_dir):
    """生成航中设备Excel表"""
    try:
        # 获取航中设备数据
        voyage_equipment_data = VoyageEquipment.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not voyage_equipment_data:
            print(f"未找到航中设备数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            voyage_equipment_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "仪器设备一览表(航中)"
        
        # 设置表头
        headers = [
            '序号', '仪器(标准物质)名称', '型号', '编号', '量值溯源方式', 
            '检定/校准日期', '有效期', '检定/校准机构', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, equipment in enumerate(voyage_equipment_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=equipment.name or '')  # 仪器（标准物质）名称
            ws.cell(row=row, column=3, value=equipment.model or '')  # 型号
            ws.cell(row=row, column=4, value=equipment.number or '')  # 编号
            ws.cell(row=row, column=5, value=equipment.traceability_method or '')  # 量值溯源方式
            ws.cell(row=row, column=6, value=equipment.calibration_date or '')  # 检定/校准日期
            ws.cell(row=row, column=7, value=equipment.validity_period or '')  # 有效期
            ws.cell(row=row, column=8, value=equipment.calibration_organization or '')  # 检定/校准机构
            ws.cell(row=row, column=9, value=equipment.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"仪器设备一览表(航中)_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航中设备表失败: {e}")
        return None

def generate_voyage_investigation_excel(task, temp_dir):
    """生成航中调查项目Excel表"""
    try:
        # 获取航中调查项目数据
        voyage_investigation_data = VoyageInvestigationProject.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not voyage_investigation_data:
            print(f"未找到航中调查项目数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            voyage_investigation_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查项目统计表(航中)"
        
        # 设置表头
        headers = [
            '序号', '项目名称', '仪器设备', '比测情况', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, project in enumerate(voyage_investigation_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=project.investigation_item_instrument or '')  # 调查项目/仪器
            ws.cell(row=row, column=3, value=project.comparison_unit_a_instrument or '')  # 比测单位甲及仪器
            ws.cell(row=row, column=4, value=project.comparison_result or '')  # 比测结果
            ws.cell(row=row, column=5, value=project.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 20
        
        # 保存文件
        filename = f"外业调查项目统计表(航中)_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航中调查项目表失败: {e}")
        return None

def generate_supervisor_log_excel(task, temp_dir):
    """生成监督员日志Excel表"""
    try:
        # 获取监督员日志数据
        supervisor_log_data = SupervisorLog.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not supervisor_log_data:
            print(f"未找到监督员日志数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            supervisor_log_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "监督员日志"
        
        # 设置表头
        headers = [
            '序号', '日期', '天气', '海况', '工作内容', '发现问题', '处理措施', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, log in enumerate(supervisor_log_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=log.inspection_date or '')  # 检查日期
            ws.cell(row=row, column=3, value='')  # 天气（数据库中没有此字段）
            ws.cell(row=row, column=4, value='')  # 海况（数据库中没有此字段）
            ws.cell(row=row, column=5, value=log.inspection_content or '')  # 检查内容
            ws.cell(row=row, column=6, value=log.existing_problems or '')  # 存在问题
            ws.cell(row=row, column=7, value=log.rectification_status or '')  # 整改情况
            ws.cell(row=row, column=8, value='')  # 备注（数据库中没有此字段）
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"监督员日志_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成监督员日志表失败: {e}")
        return None

def generate_original_records_excel(task, temp_dir):
    """生成原始记录抽查Excel表"""
    try:
        # 获取原始记录数据
        original_records_data = OriginalRecords.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not original_records_data:
            print(f"未找到原始记录数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            original_records_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查原始记录抽查表"
        
        # 设置表头
        headers = [
            '序号', '记录类型', '抽查日期', '抽查内容', '发现问题', '处理措施', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, record in enumerate(original_records_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=record.survey_item or '')  # 调查项目
            ws.cell(row=row, column=3, value=record.spot_check_time or '')  # 抽查时间
            ws.cell(row=row, column=4, value=f"站位: {record.station or ''}, 时间: {record.time or ''}, 地点: {record.location or ''}")  # 抽查内容
            ws.cell(row=row, column=5, value='')  # 发现问题（数据库中没有此字段）
            ws.cell(row=row, column=6, value=record.qualified_or_not or '')  # 合格与否
            ws.cell(row=row, column=7, value=record.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"外业调查原始记录抽查表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成原始记录抽查表失败: {e}")
        return None

def generate_procedure_execution_excel(task, temp_dir):
    """生成操作规程执行统计Excel表"""
    try:
        # 获取操作规程执行数据
        procedure_execution_data = ProcedureExecution.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not procedure_execution_data:
            print(f"未找到操作规程数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            procedure_execution_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查操作规程执行统计表"
        
        # 设置表头
        headers = [
            '序号', '操作规程名称', '执行日期', '是否具有操作规程', '调查项目/仪器', '任务承担单位', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, procedure in enumerate(procedure_execution_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=procedure.operating_procedure_name or '')  # 操作规程名称
            ws.cell(row=row, column=3, value='')  # 执行日期（数据库中没有此字段）
            ws.cell(row=row, column=4, value=procedure.has_operating_procedures or '')  # 是否具有操作规程
            ws.cell(row=row, column=5, value=procedure.investigation_item_instrument or '')  # 调查项目/仪器
            ws.cell(row=row, column=6, value=procedure.task_undertaking_unit or '')  # 任务承担单位
            ws.cell(row=row, column=7, value=procedure.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"外业调查操作规程执行统计表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成操作规程执行统计表失败: {e}")
        return None

def generate_work_log_excel(task, temp_dir):
    """生成工作日志抽查Excel表"""
    try:
        # 获取工作日志数据
        work_log_data = WorkLog.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not work_log_data:
            print(f"未找到工作日志数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            work_log_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查工作日志抽查表"
        
        # 设置表头
        headers = [
            '序号', '记录时间', '工作日志', '抽查时间', '调查项目', '任务承担单位', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, log in enumerate(work_log_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=log.record_time or '')  # 记录时间
            ws.cell(row=row, column=3, value=log.work_log or '')  # 工作日志
            ws.cell(row=row, column=4, value=log.spot_check_time or '')  # 抽查时间
            ws.cell(row=row, column=5, value=log.survey_project or '')  # 调查项目
            ws.cell(row=row, column=6, value=log.task_undertaking_unit or '')  # 任务承担单位
            ws.cell(row=row, column=7, value=log.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"外业调查工作日志抽查表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成工作日志抽查表失败: {e}")
        return None

def generate_sample_storage_excel(task, temp_dir):
    """生成样品储存记录抽查Excel表"""
    try:
        # 获取样品储存数据
        sample_storage_data = SampleStorage.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not sample_storage_data:
            print(f"未找到样品储存数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            sample_storage_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "外业调查样品储存记录抽查表"
        
        # 设置表头
        headers = [
            '序号', '储存样品', '记录时间', '调查项目', '抽查时间', '合格与否', '任务承担单位', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, sample in enumerate(sample_storage_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=sample.stored_samples or '')  # 储存样品
            ws.cell(row=row, column=3, value=sample.record_time.strftime('%Y-%m-%d') if sample.record_time else '')  # 记录时间
            ws.cell(row=row, column=4, value=sample.survey_item or '')  # 调查项目
            ws.cell(row=row, column=5, value=sample.spot_check_time.strftime('%Y-%m-%d') if sample.spot_check_time else '')  # 抽查时间
            ws.cell(row=row, column=6, value=sample.qualified_or_not or '')  # 合格与否
            ws.cell(row=row, column=7, value=sample.task_undertaking_unit or '')  # 任务承担单位
            ws.cell(row=row, column=8, value=sample.remarks or '')  # 备注
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"外业调查样品储存记录抽查表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成样品储存记录抽查表失败: {e}")
        return None

def generate_onboard_inspection_excel(task, temp_dir):
    """生成随船质量监督检查Excel表"""
    try:
        # 获取随船检查数据
        onboard_inspection_data = OnboardInspection.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not onboard_inspection_data:
            print(f"未找到随船检查数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            onboard_inspection_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "随船质量监督检查表"
        
        # 设置表头
        headers = [
            '序号', '检查日期', '被检查承担单位', '被检查参加单位', '航次首席科学家', '随船质量监督员', '被检查单位主要参与人员'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, inspection in enumerate(onboard_inspection_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=inspection.inspection_date or '')  # 检查日期
            ws.cell(row=row, column=3, value=inspection.inspected_unit or '')  # 被检查承担单位
            ws.cell(row=row, column=4, value=inspection.participating_unit or '')  # 被检查参加单位
            ws.cell(row=row, column=5, value=inspection.chief_scientist or '')  # 航次首席科学家
            ws.cell(row=row, column=6, value=inspection.onboard_supervisor or '')  # 随船质量监督员
            ws.cell(row=row, column=7, value=inspection.inspected_unit_personnel or '')  # 被检查单位主要参与人员
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"随船质量监督检查表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成随船质量监督检查表失败: {e}")
        return None

def generate_post_inspection_excel(task, temp_dir):
    """生成航后检查Excel表"""
    try:
        # 获取航后检查数据
        post_inspection_data = PostInspection.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not post_inspection_data:
            print(f"未找到航后检查数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            post_inspection_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "航后检查表"
        
        # 设置表头
        headers = [
            '序号', '检查日期', '检查内容', '存在问题', '整改情况', '填表时间', '备注'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, inspection in enumerate(post_inspection_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=inspection.inspection_date.strftime('%Y-%m-%d') if inspection.inspection_date else '')  # 检查日期
            ws.cell(row=row, column=3, value=inspection.inspection_content or '')  # 检查内容
            ws.cell(row=row, column=4, value=inspection.existing_problems or '')  # 存在问题
            ws.cell(row=row, column=5, value=inspection.rectification_status or '')  # 整改情况
            ws.cell(row=row, column=6, value=inspection.form_filling_time.strftime('%Y-%m-%d') if inspection.form_filling_time else '')  # 填表时间
            ws.cell(row=row, column=7, value='')  # 备注（数据库中没有此字段）
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"航后检查表_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航后检查表失败: {e}")
        return None

def generate_pre_voyage_inspection_excel(task, temp_dir):
    """生成航前质量监督检查记录Excel表"""
    try:
        # 获取航前质量监督检查记录数据
        pre_voyage_inspection_data = PreVoyageInspection.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not pre_voyage_inspection_data:
            print(f"未找到航前质量监督检查记录数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            pre_voyage_inspection_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "航前质量监督检查记录"
        
        # 设置表头
        headers = [
            '序号', '检查日期', '监督员', '被监督单位', '检查项目1', '问题1', '检查项目2', '问题2', 
            '检查项目3', '问题3', '检查项目4', '问题4', '检查项目5', '问题5', '检查项目6', '问题6',
            '检查项目7', '问题7', '检查项目8', '问题8', '检查项目9', '问题9', '检查项目10', '问题10',
            '检查项目11', '问题11', '检查详情', '检查结果', '首席科学家签名', '首席科学家签名日期',
            '检查负责人签名', '检查负责人签名日期'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, inspection in enumerate(pre_voyage_inspection_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=inspection.check_date or '')  # 检查日期
            ws.cell(row=row, column=3, value=inspection.superintendent or '')  # 监督员
            ws.cell(row=row, column=4, value=inspection.superintended or '')  # 被监督单位
            ws.cell(row=row, column=5, value=inspection.check_1 or '')  # 检查项目1
            ws.cell(row=row, column=6, value=inspection.check_1_problem or '')  # 问题1
            ws.cell(row=row, column=7, value=inspection.check_2 or '')  # 检查项目2
            ws.cell(row=row, column=8, value=inspection.check_2_problem or '')  # 问题2
            ws.cell(row=row, column=9, value=inspection.check_3 or '')  # 检查项目3
            ws.cell(row=row, column=10, value=inspection.check_3_problem or '')  # 问题3
            ws.cell(row=row, column=11, value=inspection.check_4 or '')  # 检查项目4
            ws.cell(row=row, column=12, value=inspection.check_4_problem or '')  # 问题4
            ws.cell(row=row, column=13, value=inspection.check_5 or '')  # 检查项目5
            ws.cell(row=row, column=14, value=inspection.check_5_problem or '')  # 问题5
            ws.cell(row=row, column=15, value=inspection.check_6 or '')  # 检查项目6
            ws.cell(row=row, column=16, value=inspection.check_6_problem or '')  # 问题6
            ws.cell(row=row, column=17, value=inspection.check_7 or '')  # 检查项目7
            ws.cell(row=row, column=18, value=inspection.check_7_problem or '')  # 问题7
            ws.cell(row=row, column=19, value=inspection.check_8 or '')  # 检查项目8
            ws.cell(row=row, column=20, value=inspection.check_8_problem or '')  # 问题8
            ws.cell(row=row, column=21, value=inspection.check_9 or '')  # 检查项目9
            ws.cell(row=row, column=22, value=inspection.check_9_problem or '')  # 问题9
            ws.cell(row=row, column=23, value=inspection.check_10 or '')  # 检查项目10
            ws.cell(row=row, column=24, value=inspection.check_10_problem or '')  # 问题10
            ws.cell(row=row, column=25, value=inspection.check_11 or '')  # 检查项目11
            ws.cell(row=row, column=26, value=inspection.check_11_problem or '')  # 问题11
            ws.cell(row=row, column=27, value=inspection.check_detail or '')  # 检查详情
            ws.cell(row=row, column=28, value=inspection.check_result or '')  # 检查结果
            ws.cell(row=row, column=29, value=inspection.chief_scientist_sign or '')  # 首席科学家签名
            ws.cell(row=row, column=30, value=inspection.chief_scientist_signdate or '')  # 首席科学家签名日期
            ws.cell(row=row, column=31, value=inspection.check_leader_sign or '')  # 检查负责人签名
            ws.cell(row=row, column=32, value=inspection.check_leader_signdate or '')  # 检查负责人签名日期
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"航前质量监督检查记录_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航前质量监督检查记录表失败: {e}")
        return None

def generate_pre_summary_excel(task, temp_dir):
    """生成航前质量监督情况汇总Excel表"""
    try:
        # 获取航前质量监督情况汇总数据
        pre_summary_data = PreSummary.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        if not pre_summary_data:
            print(f"未找到航前质量监督情况汇总数据，任务: {task.task_name}, 用户ID: {task.user_id}")
            # 即使没有数据也创建空表格
            pre_summary_data = []
        
        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "航前质量监督情况汇总"
        
        # 设置表头
        headers = [
            '序号', '航次任务名称', '航次承担单位', '航次参与单位', '航次任务编号', '调查船', 
            '任务负责人', '监督检查人员', '受检查单位主要参与人员', '检查日期', '检查情况', 
            '检查结果', '相关资料', '创建时间', '更新时间'
        ]
        
        # 写入表头
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 写入数据
        for row, summary in enumerate(pre_summary_data, 2):
            ws.cell(row=row, column=1, value=row-1)  # 序号
            ws.cell(row=row, column=2, value=summary.task_name or '')  # 航次任务名称
            ws.cell(row=row, column=3, value=summary.undertaking_unit or '')  # 航次承担单位
            ws.cell(row=row, column=4, value=summary.participating_unit or '')  # 航次参与单位
            ws.cell(row=row, column=5, value=summary.task_code or '')  # 航次任务编号
            ws.cell(row=row, column=6, value=summary.survey_vessel or '')  # 调查船
            ws.cell(row=row, column=7, value=summary.task_leader or '')  # 任务负责人
            ws.cell(row=row, column=8, value=summary.supervision_personnel or '')  # 监督检查人员
            ws.cell(row=row, column=9, value=summary.main_participants or '')  # 受检查单位主要参与人员
            ws.cell(row=row, column=10, value=summary.inspection_date.strftime('%Y-%m-%d') if summary.inspection_date else '')  # 检查日期
            ws.cell(row=row, column=11, value=summary.inspection_details or '')  # 检查情况
            ws.cell(row=row, column=12, value=summary.inspection_results or '')  # 检查结果
            ws.cell(row=row, column=13, value=summary.related_materials or '')  # 相关资料
            ws.cell(row=row, column=14, value=summary.created_at.strftime('%Y-%m-%d %H:%M:%S') if summary.created_at else '')  # 创建时间
            ws.cell(row=row, column=15, value=summary.updated_at.strftime('%Y-%m-%d %H:%M:%S') if summary.updated_at else '')  # 更新时间
        
        # 调整列宽
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
        
        # 保存文件
        filename = f"航前质量监督情况汇总_{task.task_name}.xlsx"
        filepath = os.path.join(temp_dir, filename)
        wb.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航前质量监督情况汇总表失败: {e}")
        return None
