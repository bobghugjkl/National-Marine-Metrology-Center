"""
外业调查工作日志抽查表模型
"""
from datetime import datetime
import json
from config.database import db

class WorkLog(db.Model):
    """外业调查工作日志抽查表模型"""
    __tablename__ = 'tb_work_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    survey_project = db.Column(db.String(255), comment='调查项目')
    task_undertaking_unit = db.Column(db.String(255), comment='任务承担单位')
    work_log = db.Column(db.Text, comment='工作日志')
    record_time = db.Column(db.String(45), comment='记录时间')
    spot_check_time = db.Column(db.String(45), comment='抽查时间')
    remarks = db.Column(db.Text, comment='备注')
    attachments = db.Column(db.Text, comment='附件列表，存储JSON字符串') # 存储附件的JSON字符串

    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False, comment='创建用户ID')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    user = db.relationship('User', backref=db.backref('work_log', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'survey_project': self.survey_project,
            'task_undertaking_unit': self.task_undertaking_unit,
            'work_log': self.work_log,
            'record_time': self.record_time,
            'spot_check_time': self.spot_check_time,
            'remarks': self.remarks,
            'attachments': json.loads(self.attachments) if self.attachments else [],
            'user_id': self.user_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

    def __repr__(self):
        return f"<WorkLog {self.task_name} - {self.survey_project}>"
