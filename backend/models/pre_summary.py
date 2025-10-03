"""
航前质量监督情况汇总表模型
"""
from config.database import db
import json

class PreSummary(db.Model):
    """航前质量监督情况汇总表"""
    __tablename__ = 'tb_pre_summary'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(100), nullable=False, comment='航次任务名称')
    undertaking_unit = db.Column(db.String(200), comment='航次承担单位')
    participating_unit = db.Column(db.String(200), comment='航次参与单位')
    task_code = db.Column(db.String(100), comment='航次任务编号')
    survey_vessel = db.Column(db.String(100), comment='调查船')
    task_leader = db.Column(db.String(100), comment='任务负责人')
    supervision_personnel = db.Column(db.String(200), comment='监督检查人员')
    main_participants = db.Column(db.String(200), comment='受检查单位主要参与人员')
    inspection_date = db.Column(db.Date, comment='检查日期')
    inspection_details = db.Column(db.Text, comment='检查情况')
    inspection_results = db.Column(db.Text, comment='检查结果')
    related_materials = db.Column(db.Text, comment='相关资料JSON字符串')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户ID')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        related_materials = []
        if self.related_materials:
            try:
                related_materials = json.loads(self.related_materials)
            except (json.JSONDecodeError, TypeError):
                related_materials = []
        
        return {
            'id': self.id,
            'task_name': self.task_name,
            'undertaking_unit': self.undertaking_unit,
            'participating_unit': self.participating_unit,
            'task_code': self.task_code,
            'survey_vessel': self.survey_vessel,
            'task_leader': self.task_leader,
            'supervision_personnel': self.supervision_personnel,
            'main_participants': self.main_participants,
            'inspection_date': self.inspection_date.strftime('%Y-%m-%d') if self.inspection_date else None,
            'inspection_details': self.inspection_details,
            'inspection_results': self.inspection_results,
            'related_materials': related_materials,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
