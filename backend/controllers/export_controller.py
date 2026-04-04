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
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL

export_bp = Blueprint('export', __name__, url_prefix='/api/export')

def apply_header_style(ws, headers):
    """应用统一的表头样式：黄色背景、黑色加粗字体、大字号、黑色边框"""
    # 定义样式
    header_font = Font(name='黑体', size=14, bold=True, color='000000')  # 黑体、14号、加粗、黑色
    header_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')  # 黄色背景
    header_alignment = Alignment(horizontal='center', vertical='center')
    
    # 定义边框样式
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
    
    # 应用样式到表头行
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
        
def apply_onboard_inspection_header_style(ws, headers):
    """应用随船质量监督检查表头样式：与第一张图片一致"""
    # 定义样式
    header_font = Font(name='黑体', size=12, bold=True, color='000000')  # 黑体、12号、加粗、黑色
    header_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')  # 黄色背景
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)  # 自动换行
    
    # 应用样式到表头行（无边框）
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        # 注意：这里不添加边框，与第一张图片一致

def apply_pre_voyage_inspection_header_style(ws, headers):
    """应用航前质量监督检查记录表头样式：与第二张图片一致"""
    # 定义样式
    header_font = Font(name='黑体', size=12, bold=True, color='000000')  # 黑体、12号、加粗、黑色
    header_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')  # 黄色背景
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)  # 自动换行
    
    # 定义边框样式
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
    
    # 应用样式到表头行（有边框）
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border

def create_empty_excel(temp_dir, filename, headers, title):
    """创建空Excel表格"""
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = title
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
    
    # 6. 航前检查Word文档
    print("生成航前检查Word文档...")
    pre_voyage_word_file = generate_pre_voyage_word_document(task, temp_dir)
    if pre_voyage_word_file:
        files.append(pre_voyage_word_file)
        print(f"✓ 航前检查Word文档生成成功: {pre_voyage_word_file}")
    else:
        print("✗ 航前检查Word文档生成失败")
    
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
    
    # 10. 航中检查Word文档
    print("生成航中检查Word文档...")
    during_voyage_word_file = generate_during_voyage_word_document(task, temp_dir)
    if during_voyage_word_file:
        files.append(during_voyage_word_file)
        print(f"✓ 航中检查Word文档生成成功: {during_voyage_word_file}")
    else:
        print("✗ 航中检查Word文档生成失败")
    
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
            # 应用统一的表头样式
            apply_header_style(ws, headers)
            
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
            # 应用统一的表头样式
            apply_header_style(ws, headers)
            
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
    """生成随船质量监督检查Excel表，与第二张图片完全一致"""
    try:
        # 定义检查情况标题数组
        check_situation_headers = [
            '', '', '', '', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题'
        ]

        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "随船质量监督检查表"

        # 第一行：标题行（使用合并单元格）
        ws.merge_cells('A1:D1')
        title_cell = ws.cell(row=1, column=1, value="航次任务基础信息")
        title_cell.font = Font(name='黑体', size=12, bold=True)
        title_cell.alignment = Alignment(horizontal='center', vertical='center')
        title_cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        ws.merge_cells('E1:AB1')
        check_title_cell = ws.cell(row=1, column=5, value="检查情况")
        check_title_cell.font = Font(name='黑体', size=12, bold=True)
        check_title_cell.alignment = Alignment(horizontal='center', vertical='center')
        check_title_cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        # 第二行：表头字段，前4个占一列，其余检查项目占两列
        headers = [
            '航次任务名称', '检查日期', '监督检查人员', '被检查单位（部门）主要参与人员',
            '是否成立了质量保障组织机构',
            '是否依据质量保障实施方案开展外业质量保证工作',
            '人员持证上岗及岗前培训考核相关记录',
            '所有仪器设备的检定/校准证书',
            '航次过程中质量监督及整改记录',
            '样品的现场采集、处理及储存是否执行专项调查技术规程的要求',
            '工作日志、班报及原始记录是否齐全',
            '所有技术文件和成果资料中的单位是否使用法定计量单位',
            '航次任务中发生的设计仪器设备故障情况及解决措施记录是否清晰、完整',
            '原始记录是否清晰完整，是否符合技术规程规定',
            '原始记录签字是否完整、规范',
            '形成的原始记录是否经过了内部质量检查，是否有质量检查记录'
        ]

        # 第二行表头
        col = 1
        for i, header in enumerate(headers):
            if i < 4:  # 前4个基本信息字段，每个占一列，且占据两行高度
                # 合并第二行和第三行，形成高单元格
                ws.merge_cells(start_row=2, end_row=3, start_column=col, end_column=col)
                cell = ws.cell(row=2, column=col, value=header)
                cell.font = Font(name='黑体', size=10, bold=True)
                cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
                col += 1
            else:  # 检查项目字段，每个占两列
                # 合并两个单元格作为表头字段
                ws.merge_cells(start_row=2, end_row=2, start_column=col, end_column=col+1)
                cell = ws.cell(row=2, column=col, value=header)
                cell.font = Font(name='黑体', size=10, bold=True)
                cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
                ws.column_dimensions[openpyxl.utils.get_column_letter(col+1)].width = 15
                col += 2

        # 添加黑色边框
        thin_border = Border(
            left=Side(style='thin', color='000000'),
            right=Side(style='thin', color='000000'),
            top=Side(style='thin', color='000000'),
            bottom=Side(style='thin', color='000000')
        )

        # 为第二行和第三行所有单元格添加边框（前4列已经被合并，所以只需要处理第二行）
        for c in range(1, col):
            # 为第二行添加边框
            cell = ws.cell(row=2, column=c)
            cell.border = thin_border

            # 为第三行添加边框（前4列已经被合并，所以第三行前4列也需要边框）
            if c <= 4:  # 前4列的第三行部分也需要边框
                cell_third = ws.cell(row=3, column=c)
                cell_third.border = thin_border

        # 第三行：检查情况和存在问题标题（只为检查项目部分设置）
        # 前4列留空，从第5列开始为检查项目提供检查情况和存在问题
        check_situation_headers = [
            '', '', '', '', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题'
        ]

        # 第三行：检查情况和存在问题标题（前4列已经被合并，所以从第5列开始）
        # 从第5列开始为检查项目提供检查情况和存在问题标题
        for c in range(5, col):  # 从第5列开始
            header_index = c - 1  # 计算对应的标题索引（c=5对应索引4）
            if header_index < len(check_situation_headers):  # 确保不越界
                header = check_situation_headers[header_index]
                cell = ws.cell(row=3, column=c, value=header)
                cell.font = Font(name='黑体', size=10, bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                cell.border = thin_border

                # 交替设置浅蓝色和浅褐色背景
                if header == '检查情况':
                    cell.fill = PatternFill(start_color='ADD8E6', end_color='ADD8E6', fill_type='solid')  # 浅蓝色
                elif header == '存在问题':
                    cell.fill = PatternFill(start_color='DEB887', end_color='DEB887', fill_type='solid')  # 浅褐色

        # 从第四行开始添加数据
        # 查询数据库中的随船质量监督检查数据
        onboard_inspection_data = OnboardInspection.query.filter_by(
            task_name=task.task_name,
            user_id=task.user_id
        ).all()

        # 如果有数据，添加到第四行开始的行中
        if onboard_inspection_data:
            for row_idx, inspection in enumerate(onboard_inspection_data, 4):  # 从第四行开始
                col = 1

                # 前4个基本信息字段（占一列）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'task_name', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'inspection_date', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'onboard_supervisor', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'inspected_unit_personnel', ''))
                col += 1

                # 检查项目字段（每个占两列，对应检查情况和存在问题）
                # 第1个检查项目：是否成立了质量保障组织机构（check_1）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_1', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_1_problem', ''))
                col += 1

                # 第2个检查项目：是否依据质量保障实施方案开展外业质量保证工作（check_2）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_2', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_2_problem', ''))
                col += 1

                # 第3个检查项目：人员持证上岗及岗前培训考核相关记录（check_3）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_3', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_3_problem', ''))
                col += 1

                # 第4个检查项目：所有仪器设备的检定/校准证书（check_4）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_4', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_4_problem', ''))
                col += 1

                # 第5个检查项目：航次过程中质量监督及整改记录（check_5）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_5', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_5_problem', ''))
                col += 1

                # 第6个检查项目：样品的现场采集、处理及储存是否执行专项调查技术规程的要求（check_6）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_6', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_6_problem', ''))
                col += 1

                # 第7个检查项目：工作日志、班报及原始记录是否齐全（check_7）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_7', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_7_problem', ''))
                col += 1

                # 第8个检查项目：所有技术文件和成果资料中的单位是否使用法定计量单位（check_8）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_8', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_8_problem', ''))
                col += 1

                # 第9个检查项目：航次任务中发生的设计仪器设备故障情况及解决措施记录是否清晰、完整（check_9）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_9', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_9_problem', ''))
                col += 1

                # 第10个检查项目：原始记录是否清晰完整，是否符合技术规程规定（check_10）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_10', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_10_problem', ''))
                col += 1

                # 第11个检查项目：原始记录签字是否完整、规范（check_11）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_11', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_11_problem', ''))
                col += 1

                # 第12个检查项目：形成的原始记录是否经过了内部质量检查，是否有质量检查记录（check_12）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_12', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_12_problem', ''))
                col += 1

                # 为数据行添加边框
                for c in range(1, col):
                    cell = ws.cell(row=row_idx, column=c)
                    cell.border = thin_border

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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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
    """生成航前质量监督检查记录Excel表，11个检查项"""
    try:
        # 定义检查情况标题数组（前4列留空，从第5列开始，11个检查项×2列）
        check_situation_headers = [
            '', '', '', '', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题',
            '检查情况', '存在问题', '检查情况', '存在问题', '检查情况', '存在问题'
        ]

        # 创建工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "航前质量监督检查记录"

        # 第一行：标题行（使用合并单元格）
        ws.merge_cells('A1:D1')
        title_cell = ws.cell(row=1, column=1, value="航次任务基础信息")
        title_cell.font = Font(name='黑体', size=12, bold=True)
        title_cell.alignment = Alignment(horizontal='center', vertical='center')
        title_cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        ws.merge_cells('E1:Z1')
        check_title_cell = ws.cell(row=1, column=5, value="检查情况")
        check_title_cell.font = Font(name='黑体', size=12, bold=True)
        check_title_cell.alignment = Alignment(horizontal='center', vertical='center')
        check_title_cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

        # 第二行：表头字段，前4个占一列，其余检查项目占两列（11个检查项）
        headers = [
            '航次任务名称', '检查日期', '监督单位监督人员', '被检查单位（部门）主要参与人员',
            '是否有证了解航企安全方面、指定了替代性备选项',
            '调查人员是否持有上岗证或培训证明',
            '航次主管仪器设备是否齐备有效',
            '航次所用仪器设备是否都在检定后规定有效期',
            '航次所用仪器设备检定/校准/检测费',
            '不具备检定/校准/检测条件的仪器设备是否经过了相应的比对方法记录',
            '所使用检定等数据是否备齐',
            '船运记录单或质检显示是否按其标出有效期',
            '随船内质量新格是及见效记录',
            '所有工作日志、班组、监据记录提交组织交代并签字须知',
            '海员开展检验的器体、指定案签记录起点对长期照'
        ]

        # 第二行表头
        col = 1
        for i, header in enumerate(headers):
            if i < 4:  # 前4个基本信息字段，每个占一列，且占据两行高度
                # 合并第二行和第三行，形成高单元格
                ws.merge_cells(start_row=2, end_row=3, start_column=col, end_column=col)
                cell = ws.cell(row=2, column=col, value=header)
                cell.font = Font(name='黑体', size=10, bold=True)
                cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
                col += 1
            else:  # 检查项目字段，每个占两列
                # 合并两个单元格作为表头字段
                ws.merge_cells(start_row=2, end_row=2, start_column=col, end_column=col+1)
                cell = ws.cell(row=2, column=col, value=header)
                cell.font = Font(name='黑体', size=10, bold=True)
                cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
                ws.column_dimensions[openpyxl.utils.get_column_letter(col+1)].width = 15
                col += 2

        # 添加黑色边框
        thin_border = Border(
            left=Side(style='thin', color='000000'),
            right=Side(style='thin', color='000000'),
            top=Side(style='thin', color='000000'),
            bottom=Side(style='thin', color='000000')
        )

        # 为第二行和第三行所有单元格添加边框（前4列已经被合并，所以只需要处理第二行）
        for c in range(1, col):
            # 为第二行添加边框
            cell = ws.cell(row=2, column=c)
            cell.border = thin_border

            # 为第三行添加边框（前4列已经被合并，所以第三行前4列也需要边框）
            if c <= 4:  # 前4列的第三行部分也需要边框
                cell_third = ws.cell(row=3, column=c)
                cell_third.border = thin_border

        # 第三行：检查情况和存在问题标题（为所有检查项目设置，包括航次作业）
        # 从第5列开始为检查项目提供检查情况和存在问题标题
        for c in range(5, col):  # 从第5列开始
            header_index = c - 5  # 计算对应的标题索引
            if header_index < len(check_situation_headers) - 4:  # 确保不越界
                header = check_situation_headers[header_index + 4]
                cell = ws.cell(row=3, column=c, value=header)
                cell.font = Font(name='黑体', size=10, bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                cell.border = thin_border

                # 交替设置浅蓝色和浅褐色背景
                if header == '检查情况':
                    cell.fill = PatternFill(start_color='ADD8E6', end_color='ADD8E6', fill_type='solid')  # 浅蓝色
                elif header == '存在问题':
                    cell.fill = PatternFill(start_color='DEB887', end_color='DEB887', fill_type='solid')  # 浅褐色

        # 从第四行开始添加数据
        # 查询数据库中的航前质量监督检查数据
        pre_voyage_inspection_data = PreVoyageInspection.query.filter_by(
            task_name=task.task_name,
            user_id=task.user_id
        ).all()

        # 如果有数据，添加到第四行开始的行中
        if pre_voyage_inspection_data:
            for row_idx, inspection in enumerate(pre_voyage_inspection_data, 4):  # 从第四行开始
                col = 1

                # 前4个基本信息字段（占一列）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'task_name', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_date', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'superintendent', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'superintended', ''))
                col += 1

                # 检查项目字段（每个占两列，对应检查情况和存在问题）
                # 第1个检查项目：是否成立了质量保障组织机构（check_1）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_1', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_1_problem', ''))
                col += 1

                # 第2个检查项目：是否依据质量保障实施方案开展外业质量保证工作（check_2）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_2', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_2_problem', ''))
                col += 1

                # 第3个检查项目：人员持证上岗及岗前培训考核相关记录（check_3）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_3', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_3_problem', ''))
                col += 1

                # 第4个检查项目：所有仪器设备的检定/校准证书（check_4）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_4', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_4_problem', ''))
                col += 1

                # 第5个检查项目：航次过程中质量监督及整改记录（check_5）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_5', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_5_problem', ''))
                col += 1

                # 第6个检查项目：样品的现场采集、处理及储存是否执行专项调查技术规程的要求（check_6）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_6', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_6_problem', ''))
                col += 1

                # 第7个检查项目：工作日志、班报及原始记录是否齐全（check_7）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_7', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_7_problem', ''))
                col += 1

                # 第8个检查项目：所有技术文件和成果资料中的单位是否使用法定计量单位（check_8）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_8', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_8_problem', ''))
                col += 1

                # 第9个检查项目：船舶记录表单是否显示测量结果与有效期（check_9）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_9', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_9_problem', ''))
                col += 1

                # 第10个检查项目：海况记录是否齐全完整，规范（check_10）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_10', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_10_problem', ''))
                col += 1

                # 第11个检查项目：航次作业是否按照要求填写了相关记录（check_11）
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_11', ''))
                col += 1
                ws.cell(row=row_idx, column=col, value=getattr(inspection, 'check_11_problem', ''))
                col += 1

                # 为数据行添加边框
                for c in range(1, col):
                    cell = ws.cell(row=row_idx, column=c)
                    cell.border = thin_border

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
        
        # 应用统一的表头样式
        apply_header_style(ws, headers)
        
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

def generate_pre_voyage_word_document(task, temp_dir):
    """生成航前检查Word文档，包含所有航前检查表单"""
    try:
        # 创建Word文档
        doc = Document()
        
        # 设置文档标题
        title = doc.add_heading('航前质量监督检查记录表', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 添加空行增加间距
        doc.add_paragraph()
        doc.add_paragraph()
        
        # 添加任务信息
        doc.add_heading('任务信息', level=1)
        task_info_table = doc.add_table(rows=3, cols=2)
        task_info_table.style = 'Table Grid'
        
        # 设置任务信息表格内容
        task_info_table.cell(0, 0).text = '任务名称'
        task_info_table.cell(0, 1).text = task.task_name or ''
        task_info_table.cell(1, 0).text = '任务编号'
        task_info_table.cell(1, 1).text = task.task_code or ''
        task_info_table.cell(2, 0).text = '执行时间'
        task_info_table.cell(2, 1).text = task.executiontime or ''
        
        # 添加分页符，确保附表1另起一页
        doc.add_page_break()
        
        # 1. 专项调查航前质量监督情况汇总表（附表1）
        # 添加附表1标题（左上角）
        appendix1_para = doc.add_paragraph()
        appendix1_run = appendix1_para.add_run('附表1')
        appendix1_run.font.size = 12
        appendix1_run.font.bold = True
        
        # 添加主标题（居中）
        main_title_para = doc.add_paragraph()
        main_title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        main_title_run = main_title_para.add_run('专项调查航前质量监督情况汇总表')
        main_title_run.font.size = 16
        main_title_run.font.bold = True
        
        # 添加空行
        
        doc.add_heading('附表1: 航前质量监督情况汇总', level=1)
        # 获取航前质量监督情况汇总数据
        pre_summary_data = PreSummary.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).first()
        
        # 创建一个大表格，包含所有内容（4列以支持复杂布局）
        main_table = doc.add_table(rows=9, cols=4)
        main_table.style = 'Table Grid'
        
        # 设置表格样式
        for row in main_table.rows:
            for cell in row.cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.space_before = 0
                    paragraph.paragraph_format.space_after = 0
                    paragraph.paragraph_format.line_spacing = 1.0

        # 第一行：附表1标题 + 航次承担(参与)单位
        main_table.cell(0, 0).text = '附表1'
        main_table.cell(0, 1).text = '航次承担(参与)单位'
        main_table.cell(0, 2).text = pre_summary_data.undertaking_unit if pre_summary_data else ''
        main_table.cell(0, 2).merge(main_table.cell(0, 3))

        # 第二行：专项任务名称及编号 | 任务内容 | 调查船 | 调查船内容
        main_table.cell(1, 0).text = '专项任务名称及编号'
        main_table.cell(1, 1).text = pre_summary_data.task_name if pre_summary_data else ''
        main_table.cell(1, 2).text = '调查船'
        main_table.cell(1, 3).text = pre_summary_data.survey_vessel if pre_summary_data else ''

        # 第三行：专项任务负责人 | 负责人内容 | 检查日期 | 日期内容
        main_table.cell(2, 0).text = '专项任务负责人'
        main_table.cell(2, 1).text = pre_summary_data.task_leader if pre_summary_data else ''
        main_table.cell(2, 2).text = '检查日期'
        main_table.cell(2, 3).text = pre_summary_data.inspection_date.strftime('%Y-%m-%d') if pre_summary_data and pre_summary_data.inspection_date else ''

        # 第四行：监督检查人员（合并后三列）
        main_table.cell(3, 0).text = '监督检查人员'
        main_table.cell(3, 1).text = pre_summary_data.supervision_personnel if pre_summary_data else ''
        main_table.cell(3, 1).merge(main_table.cell(3, 3))

        # 第五行：受检单位（合并后三列）
        main_table.cell(4, 0).text = '受检单位'
        main_table.cell(4, 1).text = pre_summary_data.participating_unit if pre_summary_data else ''
        main_table.cell(4, 1).merge(main_table.cell(4, 3))

        # 第六行：主要参加人员（合并后三列）
        main_table.cell(5, 0).text = '主要参加人员'
        main_table.cell(5, 1).text = pre_summary_data.main_participants if pre_summary_data else ''
        main_table.cell(5, 1).merge(main_table.cell(5, 3))

        # 第七行：检查情况（合并所有列，大矩形框）
        main_table.cell(6, 0).text = '检查情况:'
        main_table.cell(6, 1).text = pre_summary_data.inspection_details if pre_summary_data else ''
        main_table.cell(6, 0).merge(main_table.cell(6, 3))

        # 第八行：检查结果（合并所有列，大矩形框）
        main_table.cell(7, 0).text = '检查结果:'
        main_table.cell(7, 1).text = pre_summary_data.inspection_results if pre_summary_data else ''
        main_table.cell(7, 0).merge(main_table.cell(7, 3))

        # 第九行：签名区域（合并所有列）
        signature_cell = main_table.cell(8, 0)
        signature_cell.text = '首席科学家(技术负责人)签字:                    年    月    日\n\n检查小组组长签字:                    年    月    日'
        main_table.cell(8, 0).merge(main_table.cell(8, 3))

        # 设置单元格高度以匹配图片中的比例
        # 检查情况占较大空间，但调整为一页内显示
        main_table.rows[6].height = Inches(2.5)  # 检查情况行高（减小）
        main_table.rows[7].height = Inches(1.5)  # 检查结果行高（减小）
        main_table.rows[8].height = Inches(0.8)  # 签名区域行高（减小）
        
        # 添加分页符，确保下一个附表另起一页
        doc.add_page_break()
        doc.add_heading('附表2: 航前质量监督检查记录', level=1)
        # 2. 航次航前质量监督检查记录表（附表2）
        # 添加附表2标题（左上角）
        appendix2_para = doc.add_paragraph()
        appendix2_run = appendix2_para.add_run('附表 2')
        appendix2_run.font.size = 12
        appendix2_run.font.bold = True
        
        # 添加主标题（居中）
        main_title_para = doc.add_paragraph()
        main_title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        main_title_run = main_title_para.add_run('航次航前质量监督检查记录表')
        main_title_run.font.size = 16
        main_title_run.font.bold = True
        
        # 添加页码（右上角）
        page_para = doc.add_paragraph()
        page_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        page_run = page_para.add_run('第1页 共2页')
        page_run.font.size = 10
        
        
        # 获取航前质量监督检查数据
        pre_voyage_inspection_data = PreVoyageInspection.query.filter_by(
            task_name=task.task_name,
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if pre_voyage_inspection_data:
            for i, inspection in enumerate(pre_voyage_inspection_data):
                if i > 0:
                    doc.add_page_break()
                
                # 创建信息表格（4列以支持复杂布局）
                info_table = doc.add_table(rows=5, cols=4)
                info_table.style = 'Table Grid'
                
                # 设置表格样式
                for row in info_table.rows:
                    for cell in row.cells:
                        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
                        for paragraph in cell.paragraphs:
                            paragraph.paragraph_format.space_before = 0
                            paragraph.paragraph_format.space_after = 0
                            paragraph.paragraph_format.line_spacing = 1.0
                
                # 第一行：被检查单位(部门)（合并后三列）
                info_table.cell(0, 0).text = '被检查单位(部门)'
                info_table.cell(0, 1).text = getattr(inspection, 'superintended', '') or ''
                info_table.cell(0, 1).merge(info_table.cell(0, 3))
                
                # 第二行：航次任务名称 | 航次任务编号
                info_table.cell(1, 0).text = '航次任务名称'
                info_table.cell(1, 1).text = getattr(inspection, 'task_name', '') or ''
                info_table.cell(1, 2).text = '航次任务编号'
                info_table.cell(1, 3).text = task.task_code or ''
                
                # 第三行：航次首席科学家 | 检查日期
                info_table.cell(2, 0).text = '航次首席科学家'
                info_table.cell(2, 1).text = getattr(inspection, 'superintendent', '') or ''
                info_table.cell(2, 2).text = '检查日期'
                info_table.cell(2, 3).text = getattr(inspection, 'check_date', '') or ''
                
                # 第四行：监督检查人员（合并后三列）
                info_table.cell(3, 0).text = '监督检查人员'
                info_table.cell(3, 1).text = getattr(inspection, 'superintendent', '') or ''
                info_table.cell(3, 1).merge(info_table.cell(3, 3))
                
                # 第五行：被检查单位(部门)主要参加人员（合并后三列）
                info_table.cell(4, 0).text = '被检查单位(部门)主要参加人员'
                # 从航前质量监督情况汇总表获取主要参与人员
                pre_summary_for_inspection = PreSummary.query.filter_by(
                    task_name=task.task_name, 
                    user_id=task.user_id
                ).first()
                info_table.cell(4, 1).text = pre_summary_for_inspection.main_participants if pre_summary_for_inspection else ''
                info_table.cell(4, 1).merge(info_table.cell(4, 3))
                
                # 检查项目表格
                doc.add_heading('检查项目', level=2)
                inspection_table = doc.add_table(rows=12, cols=4)
                inspection_table.style = 'Table Grid'
                
                # 表头
                inspection_table.cell(0, 0).text = '序号'
                inspection_table.cell(0, 1).text = '检查内容'
                inspection_table.cell(0, 2).text = '检查情况'
                inspection_table.cell(0, 3).text = '存在问题'
                
                # 检查项目内容
                check_items = [
                    '是否制定了航次质量保障实施方案,指定了航次任务质量保障员,明确航次质量保障责任分工。',
                    '调查人员是否持证上岗并经岗前强化培训。',
                    '航次主要仪器设备是否留有备份。',
                    '航次所用仪器是否具备相应操作规程。',
                    '航次所用仪器设备的检定/校准/检测情况。',
                    '不具备检定/校准/检测条件的仪器设备是否制定了相应的自校/比对/比测计划。',
                    '所使用的标准物质是否为有证标准物质。',
                    '船舶实验室环境设施是否满足航次任务要求。',
                    '航前内部质量检查及整改记录。',
                    '所有工作日志、班报、原始记录的格式、内容是否符合相关技术规程的要求。',
                    '是否开展航次试航,并对发现的问题提出解决措施。'
                ]
                
                for j, item in enumerate(check_items, 1):
                    inspection_table.cell(j, 0).text = str(j)
                    inspection_table.cell(j, 1).text = item
                    inspection_table.cell(j, 2).text = getattr(inspection, f'check_{j}', '') or ''
                    inspection_table.cell(j, 3).text = getattr(inspection, f'check_{j}_problem', '') or ''
                
                # 签名区域
                doc.add_paragraph('航次首席科学家: _________________ 年 月 日')
                doc.add_paragraph('检查小组组长: _________________ 年 月 日')
                
                # 添加空行增加间距
                doc.add_paragraph()
                doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            # 基本信息表格
            basic_info_table = doc.add_table(rows=4, cols=2)
            basic_info_table.style = 'Table Grid'
            
            basic_info_table.cell(0, 0).text = '被检查单位(部门)'
            basic_info_table.cell(0, 1).text = ''
            basic_info_table.cell(1, 0).text = '航次任务名称'
            basic_info_table.cell(1, 1).text = task.task_name or ''
            basic_info_table.cell(2, 0).text = '航次首席科学家'
            basic_info_table.cell(2, 1).text = ''
            basic_info_table.cell(3, 0).text = '检查日期'
            basic_info_table.cell(3, 1).text = ''
            
            # 检查项目表格
            doc.add_heading('检查项目', level=2)
            inspection_table = doc.add_table(rows=12, cols=4)
            inspection_table.style = 'Table Grid'
            
            # 表头
            inspection_table.cell(0, 0).text = '序号'
            inspection_table.cell(0, 1).text = '检查内容'
            inspection_table.cell(0, 2).text = '检查情况'
            inspection_table.cell(0, 3).text = '存在问题'
            
            # 检查项目内容
            check_items = [
                '是否制定了航次质量保障实施方案,指定了航次任务质量保障员,明确航次质量保障责任分工。',
                '调查人员是否持证上岗并经岗前强化培训。',
                '航次主要仪器设备是否留有备份。',
                '航次所用仪器是否具备相应操作规程。',
                '航次所用仪器设备的检定/校准/检测情况。',
                '不具备检定/校准/检测条件的仪器设备是否制定了相应的自校/比对/比测计划。',
                '所使用的标准物质是否为有证标准物质。',
                '船舶实验室环境设施是否满足航次任务要求。',
                '航前内部质量检查及整改记录。',
                '所有工作日志、班报、原始记录的格式、内容是否符合相关技术规程的要求。',
                '是否开展航次试航,并对发现的问题提出解决措施。'
            ]
            
            for j, item in enumerate(check_items, 1):
                inspection_table.cell(j, 0).text = str(j)
                inspection_table.cell(j, 1).text = item
                inspection_table.cell(j, 2).text = ''
                inspection_table.cell(j, 3).text = ''
            
            # 签名区域
            doc.add_paragraph('航次首席科学家: _________________ 年 月 日')
            doc.add_paragraph('检查小组组长: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 3. 专项调查航次外业调查人员资质一览表（附表3）
        doc.add_heading('附表3: 专项调查航次外业调查人员资质一览表 (含参与单位)', level=1)
        
        # 获取人员资质数据
        personnel_data = PersonnelQualification.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if personnel_data:
            personnel_table = doc.add_table(rows=len(personnel_data) + 1, cols=10)
            personnel_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '姓名', '性别', '出生年月', '职称', '工作单位', '从事专业', '本航次操作仪器', '培训情况', '备注']
            for j, header in enumerate(headers):
                personnel_table.cell(0, j).text = header
            
            # 数据行
            for i, personnel in enumerate(personnel_data, 1):
                personnel_table.cell(i, 0).text = str(i)
                personnel_table.cell(i, 1).text = personnel.name or ''
                personnel_table.cell(i, 2).text = personnel.sex or ''
                personnel_table.cell(i, 3).text = personnel.birthdate.strftime('%Y-%m') if personnel.birthdate else ''
                personnel_table.cell(i, 4).text = personnel.professional_title or ''
                personnel_table.cell(i, 5).text = personnel.employer or ''
                personnel_table.cell(i, 6).text = personnel.specialty or ''
                personnel_table.cell(i, 7).text = personnel.instruments or ''
                personnel_table.cell(i, 8).text = personnel.training or ''
                personnel_table.cell(i, 9).text = personnel.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            personnel_table = doc.add_table(rows=2, cols=10)
            personnel_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '姓名', '性别', '出生年月', '职称', '工作单位', '从事专业', '本航次操作仪器', '培训情况', '备注']
            for j, header in enumerate(headers):
                personnel_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(10):
                personnel_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 4. 专项调查航次仪器设备 (工作计量器具) 一览表（附表4）
        doc.add_heading('附表4: 专项调查航次仪器设备 (工作计量器具) 一览表', level=1)
        
        # 获取设备数据
        equipment_data = Equipment.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if equipment_data:
            equipment_table = doc.add_table(rows=len(equipment_data) + 1, cols=10)
            equipment_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '仪器(标准物质)名称', '编号', '型号', '量值溯源方式', '检定/校准日期', '证书编号', '有效期', '检定/校准机构', '备注']
            for j, header in enumerate(headers):
                equipment_table.cell(0, j).text = header
            
            # 数据行
            for i, equipment in enumerate(equipment_data, 1):
                equipment_table.cell(i, 0).text = str(i)
                equipment_table.cell(i, 1).text = equipment.name or ''
                equipment_table.cell(i, 2).text = equipment.number or ''
                equipment_table.cell(i, 3).text = equipment.model or ''
                equipment_table.cell(i, 4).text = equipment.traceability_method or ''
                equipment_table.cell(i, 5).text = equipment.calibration_date or ''
                equipment_table.cell(i, 6).text = equipment.certificate_number or ''
                equipment_table.cell(i, 7).text = equipment.validity_period or ''
                equipment_table.cell(i, 8).text = equipment.calibration_organization or ''
                equipment_table.cell(i, 9).text = equipment.remarks or ''
            
            # 添加说明
            doc.add_paragraph('注:如仪器为自校准,请在备注中说明,并提供自校准报告复印件。')
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            equipment_table = doc.add_table(rows=2, cols=10)
            equipment_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '仪器(标准物质)名称', '编号', '型号', '量值溯源方式', '检定/校准日期', '证书编号', '有效期', '检定/校准机构', '备注']
            for j, header in enumerate(headers):
                equipment_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(10):
                equipment_table.cell(1, j).text = ''
            
            # 添加说明
            doc.add_paragraph('注:如仪器为自校准,请在备注中说明,并提供自校准报告复印件。')
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 5. 专项调查航次外业调查项目/仪器比测统计表（附表5）
        doc.add_heading('附表5: 专项调查航次外业调查项目/仪器比测统计表', level=1)
        
        # 获取调查项目数据
        investigation_data = InvestigationProject.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if investigation_data:
            investigation_table = doc.add_table(rows=len(investigation_data) + 1, cols=8)
            investigation_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '调查项目/仪器', '比测单位甲及仪器', '比测单位乙及仪器', '比测时间', '比测地点', '比测结果', '备注']
            for j, header in enumerate(headers):
                investigation_table.cell(0, j).text = header
            
            # 数据行
            for i, project in enumerate(investigation_data, 1):
                investigation_table.cell(i, 0).text = str(i)
                investigation_table.cell(i, 1).text = project.investigation_item or ''
                investigation_table.cell(i, 2).text = project.unit_a_instrument or ''
                investigation_table.cell(i, 3).text = project.unit_b_instrument or ''
                investigation_table.cell(i, 4).text = project.comparison_time or ''
                investigation_table.cell(i, 5).text = project.comparison_location or ''
                investigation_table.cell(i, 6).text = project.comparison_result or ''
                investigation_table.cell(i, 7).text = project.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            investigation_table = doc.add_table(rows=2, cols=8)
            investigation_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '调查项目/仪器', '比测单位甲及仪器', '比测单位乙及仪器', '比测时间', '比测地点', '比测结果', '备注']
            for j, header in enumerate(headers):
                investigation_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(8):
                investigation_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 保存文档
        filename = f"航前质量监督检查记录表_{task.task_name}.docx"
        filepath = os.path.join(temp_dir, filename)
        doc.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航前检查Word文档失败: {e}")
        return None

def generate_during_voyage_word_document(task, temp_dir):
    """生成航中检查Word文档，包含所有航中检查表单"""
    try:
        # 创建Word文档
        doc = Document()
        
        # 设置文档标题
        title = doc.add_heading('航中质量监督检查记录表', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 添加空行增加间距
        doc.add_paragraph()
        doc.add_paragraph()
        
        # 添加任务信息
        doc.add_heading('任务信息', level=1)
        task_info_table = doc.add_table(rows=3, cols=2)
        task_info_table.style = 'Table Grid'
        
        # 设置任务信息表格内容
        task_info_table.cell(0, 0).text = '任务名称'
        task_info_table.cell(0, 1).text = task.task_name or ''
        task_info_table.cell(1, 0).text = '任务编号'
        task_info_table.cell(1, 1).text = task.task_code or ''
        task_info_table.cell(2, 0).text = '执行时间'
        task_info_table.cell(2, 1).text = task.executiontime or ''
        
        # 添加空行增加间距
        doc.add_paragraph()
        doc.add_paragraph()
        
        # 1. 外业调查人员资质一览表（航中）
        doc.add_heading('附表1: 外业调查人员资质一览表（航中）', level=1)
        
        # 获取航中人员资质数据
        voyage_personnel_data = VoyagePersonnel.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if voyage_personnel_data:
            personnel_table = doc.add_table(rows=len(voyage_personnel_data) + 1, cols=10)
            personnel_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '姓名', '性别', '出生年月', '职称', '工作单位', '从事专业', '本航次操作仪器', '培训情况', '备注']
            for j, header in enumerate(headers):
                personnel_table.cell(0, j).text = header
            
            # 数据行
            for i, personnel in enumerate(voyage_personnel_data, 1):
                personnel_table.cell(i, 0).text = str(i)
                personnel_table.cell(i, 1).text = personnel.name or ''
                personnel_table.cell(i, 2).text = personnel.sex or ''
                personnel_table.cell(i, 3).text = personnel.birthdate.strftime('%Y-%m') if personnel.birthdate else ''
                personnel_table.cell(i, 4).text = personnel.professional_title or ''
                personnel_table.cell(i, 5).text = personnel.employer or ''
                personnel_table.cell(i, 6).text = personnel.specialty or ''
                personnel_table.cell(i, 7).text = personnel.instruments or ''
                personnel_table.cell(i, 8).text = personnel.training or ''
                personnel_table.cell(i, 9).text = personnel.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            personnel_table = doc.add_table(rows=2, cols=10)
            personnel_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '姓名', '性别', '出生年月', '职称', '工作单位', '从事专业', '本航次操作仪器', '培训情况', '备注']
            for j, header in enumerate(headers):
                personnel_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(10):
                personnel_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 2. 仪器设备(工作计量器具)一览表（航中）
        doc.add_heading('附表2: 仪器设备(工作计量器具)一览表（航中）', level=1)
        
        # 获取航中设备数据
        voyage_equipment_data = VoyageEquipment.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if voyage_equipment_data:
            equipment_table = doc.add_table(rows=len(voyage_equipment_data) + 1, cols=10)
            equipment_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '仪器(标准物质)名称', '编号', '型号', '量值溯源方式', '检定/校准日期', '证书编号', '有效期', '检定/校准机构', '备注']
            for j, header in enumerate(headers):
                equipment_table.cell(0, j).text = header
            
            # 数据行
            for i, equipment in enumerate(voyage_equipment_data, 1):
                equipment_table.cell(i, 0).text = str(i)
                equipment_table.cell(i, 1).text = equipment.name or ''
                equipment_table.cell(i, 2).text = equipment.number or ''
                equipment_table.cell(i, 3).text = equipment.model or ''
                equipment_table.cell(i, 4).text = equipment.traceability_method or ''
                equipment_table.cell(i, 5).text = equipment.calibration_date or ''
                equipment_table.cell(i, 6).text = equipment.certificate_number or ''
                equipment_table.cell(i, 7).text = equipment.validity_period or ''
                equipment_table.cell(i, 8).text = equipment.calibration_organization or ''
                equipment_table.cell(i, 9).text = equipment.remarks or ''
            
            # 添加说明
            doc.add_paragraph('注:如仪器为自校准,请在备注中说明,并提供自校准报告复印件。')
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            equipment_table = doc.add_table(rows=2, cols=10)
            equipment_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '仪器(标准物质)名称', '编号', '型号', '量值溯源方式', '检定/校准日期', '证书编号', '有效期', '检定/校准机构', '备注']
            for j, header in enumerate(headers):
                equipment_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(10):
                equipment_table.cell(1, j).text = ''
            
            # 添加说明
            doc.add_paragraph('注:如仪器为自校准,请在备注中说明,并提供自校准报告复印件。')
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 3. 外业调查项目/仪器比测统计表（航中）
        doc.add_heading('附表3: 外业调查项目/仪器比测统计表（航中）', level=1)
        
        # 获取航中调查项目数据
        voyage_investigation_data = VoyageInvestigationProject.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if voyage_investigation_data:
            investigation_table = doc.add_table(rows=len(voyage_investigation_data) + 1, cols=8)
            investigation_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '调查项目/仪器', '比测单位甲及仪器', '比测单位乙及仪器', '比测时间', '比测地点', '比测结果', '备注']
            for j, header in enumerate(headers):
                investigation_table.cell(0, j).text = header
            
            # 数据行
            for i, project in enumerate(voyage_investigation_data, 1):
                investigation_table.cell(i, 0).text = str(i)
                investigation_table.cell(i, 1).text = project.investigation_item_instrument or ''
                investigation_table.cell(i, 2).text = project.comparison_unit_a_instrument or ''
                investigation_table.cell(i, 3).text = project.comparison_unit_b_instrument or ''
                investigation_table.cell(i, 4).text = project.comparison_time or ''
                investigation_table.cell(i, 5).text = project.comparison_location or ''
                investigation_table.cell(i, 6).text = project.comparison_result or ''
                investigation_table.cell(i, 7).text = project.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            investigation_table = doc.add_table(rows=2, cols=8)
            investigation_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '调查项目/仪器', '比测单位甲及仪器', '比测单位乙及仪器', '比测时间', '比测地点', '比测结果', '备注']
            for j, header in enumerate(headers):
                investigation_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(8):
                investigation_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 4. 监督员日志
        doc.add_heading('附表4: 监督员日志', level=1)
        
        # 获取监督员日志数据
        supervisor_log_data = SupervisorLog.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if supervisor_log_data:
            log_table = doc.add_table(rows=len(supervisor_log_data) + 1, cols=8)
            log_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '日期', '天气', '海况', '工作内容', '发现问题', '处理措施', '备注']
            for j, header in enumerate(headers):
                log_table.cell(0, j).text = header
            
            # 数据行
            for i, log in enumerate(supervisor_log_data, 1):
                log_table.cell(i, 0).text = str(i)
                log_table.cell(i, 1).text = log.inspection_date or ''
                log_table.cell(i, 2).text = ''  # 天气（数据库中没有此字段）
                log_table.cell(i, 3).text = ''  # 海况（数据库中没有此字段）
                log_table.cell(i, 4).text = log.inspection_content or ''
                log_table.cell(i, 5).text = log.existing_problems or ''
                log_table.cell(i, 6).text = log.rectification_status or ''
                log_table.cell(i, 7).text = ''  # 备注（数据库中没有此字段）
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            log_table = doc.add_table(rows=2, cols=8)
            log_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '日期', '天气', '海况', '工作内容', '发现问题', '处理措施', '备注']
            for j, header in enumerate(headers):
                log_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(8):
                log_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 5. 外业调查原始记录抽查表
        doc.add_heading('附表5: 外业调查原始记录抽查表', level=1)
        
        # 获取原始记录数据
        original_records_data = OriginalRecords.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if original_records_data:
            records_table = doc.add_table(rows=len(original_records_data) + 1, cols=7)
            records_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '记录类型', '抽查日期', '抽查内容', '发现问题', '处理措施', '备注']
            for j, header in enumerate(headers):
                records_table.cell(0, j).text = header
            
            # 数据行
            for i, record in enumerate(original_records_data, 1):
                records_table.cell(i, 0).text = str(i)
                records_table.cell(i, 1).text = record.survey_item or ''
                records_table.cell(i, 2).text = record.spot_check_time or ''
                records_table.cell(i, 3).text = f"站位: {record.station or ''}, 时间: {record.time or ''}, 地点: {record.location or ''}"
                records_table.cell(i, 4).text = ''  # 发现问题（数据库中没有此字段）
                records_table.cell(i, 5).text = record.qualified_or_not or ''
                records_table.cell(i, 6).text = record.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            records_table = doc.add_table(rows=2, cols=7)
            records_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '记录类型', '抽查日期', '抽查内容', '发现问题', '处理措施', '备注']
            for j, header in enumerate(headers):
                records_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(7):
                records_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 6. 外业调查操作规程执行统计表
        doc.add_heading('附表6: 外业调查操作规程执行统计表', level=1)
        
        # 获取操作规程执行数据
        procedure_execution_data = ProcedureExecution.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if procedure_execution_data:
            procedure_table = doc.add_table(rows=len(procedure_execution_data) + 1, cols=7)
            procedure_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '操作规程名称', '执行日期', '是否具有操作规程', '调查项目/仪器', '任务承担单位', '备注']
            for j, header in enumerate(headers):
                procedure_table.cell(0, j).text = header
            
            # 数据行
            for i, procedure in enumerate(procedure_execution_data, 1):
                procedure_table.cell(i, 0).text = str(i)
                procedure_table.cell(i, 1).text = procedure.operating_procedure_name or ''
                procedure_table.cell(i, 2).text = ''  # 执行日期（数据库中没有此字段）
                procedure_table.cell(i, 3).text = procedure.has_operating_procedures or ''
                procedure_table.cell(i, 4).text = procedure.investigation_item_instrument or ''
                procedure_table.cell(i, 5).text = procedure.task_undertaking_unit or ''
                procedure_table.cell(i, 6).text = procedure.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            procedure_table = doc.add_table(rows=2, cols=7)
            procedure_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '操作规程名称', '执行日期', '是否具有操作规程', '调查项目/仪器', '任务承担单位', '备注']
            for j, header in enumerate(headers):
                procedure_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(7):
                procedure_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 7. 外业调查工作日志抽查表
        doc.add_heading('附表7: 外业调查工作日志抽查表', level=1)
        
        # 获取工作日志数据
        work_log_data = WorkLog.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if work_log_data:
            work_log_table = doc.add_table(rows=len(work_log_data) + 1, cols=7)
            work_log_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '记录时间', '工作日志', '抽查时间', '调查项目', '任务承担单位', '备注']
            for j, header in enumerate(headers):
                work_log_table.cell(0, j).text = header
            
            # 数据行
            for i, log in enumerate(work_log_data, 1):
                work_log_table.cell(i, 0).text = str(i)
                work_log_table.cell(i, 1).text = log.record_time or ''
                work_log_table.cell(i, 2).text = log.work_log or ''
                work_log_table.cell(i, 3).text = log.spot_check_time or ''
                work_log_table.cell(i, 4).text = log.survey_project or ''
                work_log_table.cell(i, 5).text = log.task_undertaking_unit or ''
                work_log_table.cell(i, 6).text = log.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            work_log_table = doc.add_table(rows=2, cols=7)
            work_log_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '记录时间', '工作日志', '抽查时间', '调查项目', '任务承担单位', '备注']
            for j, header in enumerate(headers):
                work_log_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(7):
                work_log_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 8. 外业调查样品储存记录抽查表
        doc.add_heading('附表8: 外业调查样品储存记录抽查表', level=1)
        
        # 获取样品储存数据
        sample_storage_data = SampleStorage.query.filter_by(
            task_name=task.task_name, 
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if sample_storage_data:
            sample_table = doc.add_table(rows=len(sample_storage_data) + 1, cols=8)
            sample_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '储存样品', '记录时间', '调查项目', '抽查时间', '合格与否', '任务承担单位', '备注']
            for j, header in enumerate(headers):
                sample_table.cell(0, j).text = header
            
            # 数据行
            for i, sample in enumerate(sample_storage_data, 1):
                sample_table.cell(i, 0).text = str(i)
                sample_table.cell(i, 1).text = sample.stored_samples or ''
                sample_table.cell(i, 2).text = sample.record_time.strftime('%Y-%m-%d') if sample.record_time else ''
                sample_table.cell(i, 3).text = sample.survey_item or ''
                sample_table.cell(i, 4).text = sample.spot_check_time.strftime('%Y-%m-%d') if sample.spot_check_time else ''
                sample_table.cell(i, 5).text = sample.qualified_or_not or ''
                sample_table.cell(i, 6).text = sample.task_undertaking_unit or ''
                sample_table.cell(i, 7).text = sample.remarks or ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            sample_table = doc.add_table(rows=2, cols=8)
            sample_table.style = 'Table Grid'
            
            # 表头
            headers = ['序号', '储存样品', '记录时间', '调查项目', '抽查时间', '合格与否', '任务承担单位', '备注']
            for j, header in enumerate(headers):
                sample_table.cell(0, j).text = header
            
            # 空数据行
            for j in range(8):
                sample_table.cell(1, j).text = ''
            
            # 签名区域
            doc.add_paragraph('填表人: _________________ 审核: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 添加分页符
        doc.add_page_break()
        
        # 9. 随船质量监督检查表
        doc.add_heading('附表9: 随船质量监督检查表', level=1)
        
        # 获取随船质量监督检查数据
        onboard_inspection_data = OnboardInspection.query.filter_by(
            task_name=task.task_name,
            user_id=task.user_id
        ).all()
        
        # 无论是否有数据都显示表格结构
        if onboard_inspection_data:
            for i, inspection in enumerate(onboard_inspection_data):
                if i > 0:
                    doc.add_page_break()
                
                # 基本信息表格
                basic_info_table = doc.add_table(rows=4, cols=2)
                basic_info_table.style = 'Table Grid'
                
                basic_info_table.cell(0, 0).text = '航次任务名称'
                basic_info_table.cell(0, 1).text = getattr(inspection, 'task_name', '') or ''
                basic_info_table.cell(1, 0).text = '检查日期'
                basic_info_table.cell(1, 1).text = getattr(inspection, 'inspection_date', '') or ''
                basic_info_table.cell(2, 0).text = '监督检查人员'
                basic_info_table.cell(2, 1).text = getattr(inspection, 'onboard_supervisor', '') or ''
                basic_info_table.cell(3, 0).text = '被检查单位（部门）主要参与人员'
                basic_info_table.cell(3, 1).text = getattr(inspection, 'inspected_unit_personnel', '') or ''
                
                # 检查项目表格
                doc.add_heading('检查项目', level=2)
                inspection_table = doc.add_table(rows=13, cols=4)
                inspection_table.style = 'Table Grid'
                
                # 表头
                inspection_table.cell(0, 0).text = '序号'
                inspection_table.cell(0, 1).text = '检查内容'
                inspection_table.cell(0, 2).text = '检查情况'
                inspection_table.cell(0, 3).text = '存在问题'
                
                # 检查项目内容
                check_items = [
                    '是否成立了质量保障组织机构',
                    '是否依据质量保障实施方案开展外业质量保证工作',
                    '人员持证上岗及岗前培训考核相关记录',
                    '所有仪器设备的检定/校准证书',
                    '航次过程中质量监督及整改记录',
                    '样品的现场采集、处理及储存是否执行专项调查技术规程的要求',
                    '工作日志、班报及原始记录是否齐全',
                    '所有技术文件和成果资料中的单位是否使用法定计量单位',
                    '航次任务中发生的设计仪器设备故障情况及解决措施记录是否清晰、完整',
                    '原始记录是否清晰完整，是否符合技术规程规定',
                    '原始记录签字是否完整、规范',
                    '形成的原始记录是否经过了内部质量检查，是否有质量检查记录'
                ]
                
                for j, item in enumerate(check_items, 1):
                    inspection_table.cell(j, 0).text = str(j)
                    inspection_table.cell(j, 1).text = item
                    inspection_table.cell(j, 2).text = getattr(inspection, f'check_{j}', '') or ''
                    inspection_table.cell(j, 3).text = getattr(inspection, f'check_{j}_problem', '') or ''
                
                # 签名区域
                doc.add_paragraph('航次首席科学家: _________________ 年 月 日')
                doc.add_paragraph('检查小组组长: _________________ 年 月 日')
                
                # 添加空行增加间距
                doc.add_paragraph()
                doc.add_paragraph()
        else:
            # 如果没有数据，显示空的表格结构
            # 基本信息表格
            basic_info_table = doc.add_table(rows=4, cols=2)
            basic_info_table.style = 'Table Grid'
            
            basic_info_table.cell(0, 0).text = '航次任务名称'
            basic_info_table.cell(0, 1).text = task.task_name or ''
            basic_info_table.cell(1, 0).text = '检查日期'
            basic_info_table.cell(1, 1).text = ''
            basic_info_table.cell(2, 0).text = '监督检查人员'
            basic_info_table.cell(2, 1).text = ''
            basic_info_table.cell(3, 0).text = '被检查单位（部门）主要参与人员'
            basic_info_table.cell(3, 1).text = ''
            
            # 检查项目表格
            doc.add_heading('检查项目', level=2)
            inspection_table = doc.add_table(rows=13, cols=4)
            inspection_table.style = 'Table Grid'
            
            # 表头
            inspection_table.cell(0, 0).text = '序号'
            inspection_table.cell(0, 1).text = '检查内容'
            inspection_table.cell(0, 2).text = '检查情况'
            inspection_table.cell(0, 3).text = '存在问题'
            
            # 检查项目内容
            check_items = [
                '是否成立了质量保障组织机构',
                '是否依据质量保障实施方案开展外业质量保证工作',
                '人员持证上岗及岗前培训考核相关记录',
                '所有仪器设备的检定/校准证书',
                '航次过程中质量监督及整改记录',
                '样品的现场采集、处理及储存是否执行专项调查技术规程的要求',
                '工作日志、班报及原始记录是否齐全',
                '所有技术文件和成果资料中的单位是否使用法定计量单位',
                '航次任务中发生的设计仪器设备故障情况及解决措施记录是否清晰、完整',
                '原始记录是否清晰完整，是否符合技术规程规定',
                '原始记录签字是否完整、规范',
                '形成的原始记录是否经过了内部质量检查，是否有质量检查记录'
            ]
            
            for j, item in enumerate(check_items, 1):
                inspection_table.cell(j, 0).text = str(j)
                inspection_table.cell(j, 1).text = item
                inspection_table.cell(j, 2).text = ''
                inspection_table.cell(j, 3).text = ''
            
            # 签名区域
            doc.add_paragraph('航次首席科学家: _________________ 年 月 日')
            doc.add_paragraph('检查小组组长: _________________ 年 月 日')
            
            # 添加空行增加间距
            doc.add_paragraph()
            doc.add_paragraph()
        
        # 保存文档
        filename = f"航中质量监督检查记录表_{task.task_name}.docx"
        filepath = os.path.join(temp_dir, filename)
        doc.save(filepath)
        return filepath
        
    except Exception as e:
        print(f"生成航中检查Word文档失败: {e}")
        return None
