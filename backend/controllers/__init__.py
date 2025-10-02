"""
控制器模块 - 导出所有路由蓝图
"""
from .user_controller import user_bp
from .task_controller import task_bp
from .inspection_controller import inspection_bp
from .auth_controller import auth_bp
from .personnel_controller import personnel_bp
from .equipment_controller import equipment_bp
from .investigation_controller import investigation_bp
from .voyage_personnel_controller import voyage_personnel_bp
from .voyage_equipment_controller import voyage_equipment_bp
from .voyage_investigation_controller import voyage_investigation_bp
from .supervisor_log_controller import supervisor_log_bp
from .original_records_controller import original_records_bp
from .procedure_execution_controller import procedure_execution_bp

__all__ = ['user_bp', 'task_bp', 'inspection_bp', 'auth_bp', 'personnel_bp', 'equipment_bp', 'investigation_bp', 'voyage_personnel_bp', 'voyage_equipment_bp', 'voyage_investigation_bp', 'supervisor_log_bp', 'original_records_bp', 'procedure_execution_bp']
