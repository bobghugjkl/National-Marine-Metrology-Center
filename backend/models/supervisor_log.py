"""
监督员日志模型
"""
from datetime import datetime
import json
from config.database import db

class SupervisorLog(db.Model):
    """监督员日志模型"""
    __tablename__ = 'tb_supervisor_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    supervisor = db.Column(db.String(100), nullable=False, comment='监督员')
    inspection_date = db.Column(db.String(45), comment='检查日期')
    inspection_content = db.Column(db.Text, comment='检查内容')
    existing_problems = db.Column(db.Text, comment='存在问题')
    rectification_status = db.Column(db.Text, comment='整改情况')
    form_filling_time = db.Column(db.String(45), comment='填表时间')
    attachments = db.Column(db.Text, comment='附件列表，存储JSON字符串') # 存储附件的JSON字符串

    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False, comment='创建用户ID')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    user = db.relationship('User', backref=db.backref('supervisor_logs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'supervisor': self.supervisor,
            'inspection_date': self.inspection_date,
            'inspection_content': self.inspection_content,
            'existing_problems': self.existing_problems,
            'rectification_status': self.rectification_status,
            'form_filling_time': self.form_filling_time,
            'attachments': json.loads(self.attachments) if self.attachments else [],
            'user_id': self.user_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

    def __repr__(self):
        return f"<SupervisorLog {self.task_name} - {self.supervisor}>"
