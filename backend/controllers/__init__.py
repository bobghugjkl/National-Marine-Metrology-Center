"""
控制器模块 - 导出所有路由蓝图
"""
from .user_controller import user_bp
from .task_controller import task_bp
from .inspection_controller import inspection_bp
from .auth_controller import auth_bp
from .personnel_controller import personnel_bp

__all__ = ['user_bp', 'task_bp', 'inspection_bp', 'auth_bp', 'personnel_bp']
