"""
航后检查表模型
"""
from config.database import db
import json

class PostInspection(db.Model):
    """航后检查表"""
    __tablename__ = 'tb_post_inspection'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(100), nullable=False, comment='航次任务名称')
    inspection_date = db.Column(db.Date, comment='检查日期')
    inspection_content = db.Column(db.Text, comment='检查内容')
    existing_problems = db.Column(db.Text, comment='存在问题')
    rectification_status = db.Column(db.Text, comment='整改情况')
    form_filling_time = db.Column(db.Date, comment='填表时间')
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
            'inspection_date': self.inspection_date.strftime('%Y-%m-%d') if self.inspection_date else None,
            'inspection_content': self.inspection_content,
            'existing_problems': self.existing_problems,
            'rectification_status': self.rectification_status,
            'form_filling_time': self.form_filling_time.strftime('%Y-%m-%d') if self.form_filling_time else None,
            'attachments': attachments,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
