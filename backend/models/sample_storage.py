"""
外业调查样品储存记录抽查表模型
"""
from config.database import db
import json

class SampleStorage(db.Model):
    """外业调查样品储存记录抽查表"""
    __tablename__ = 'tb_sample_storage'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(100), nullable=False, comment='航次任务名称')
    survey_item = db.Column(db.String(200), nullable=False, comment='调查项目')
    task_undertaking_unit = db.Column(db.String(200), nullable=False, comment='任务承担单位')
    stored_samples = db.Column(db.Text, comment='储存样品')
    record_time = db.Column(db.Date, comment='记录时间')
    spot_check_time = db.Column(db.Date, comment='抽查时间')
    qualified_or_not = db.Column(db.String(50), comment='合格与否')
    remarks = db.Column(db.Text, comment='备注')
    attachments = db.Column(db.Text, comment='附件JSON字符串')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户ID')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        attachments = []
        if self.attachments:
            try:
                attachments = json.loads(self.attachments)
            except (json.JSONDecodeError, TypeError):
                attachments = []
        
        return {
            'id': self.id,
            'task_name': self.task_name,
            'survey_item': self.survey_item,
            'task_undertaking_unit': self.task_undertaking_unit,
            'stored_samples': self.stored_samples,
            'record_time': self.record_time.strftime('%Y-%m-%d') if self.record_time else None,
            'spot_check_time': self.spot_check_time.strftime('%Y-%m-%d') if self.spot_check_time else None,
            'qualified_or_not': self.qualified_or_not,
            'remarks': self.remarks,
            'attachments': attachments,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
