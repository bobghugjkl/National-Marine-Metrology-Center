"""
外业调查原始记录抽查表模型
"""
from datetime import datetime
import json
from config.database import db

class OriginalRecords(db.Model):
    """外业调查原始记录抽查表模型"""
    __tablename__ = 'tb_original_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    survey_item = db.Column(db.String(255), comment='调查项目')
    task_undertaking_unit = db.Column(db.String(255), comment='任务承担单位')
    station = db.Column(db.String(255), comment='站位')
    time = db.Column(db.String(45), comment='时间')
    location = db.Column(db.String(255), comment='地点')
    spot_check_time = db.Column(db.String(45), comment='抽查时间')
    qualified_or_not = db.Column(db.String(45), comment='合格与否')
    remarks = db.Column(db.Text, comment='备注')
    attachments = db.Column(db.Text, comment='附件列表，存储JSON字符串') # 存储附件的JSON字符串

    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False, comment='创建用户ID')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    user = db.relationship('User', backref=db.backref('original_records', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'survey_item': self.survey_item,
            'task_undertaking_unit': self.task_undertaking_unit,
            'station': self.station,
            'time': self.time,
            'location': self.location,
            'spot_check_time': self.spot_check_time,
            'qualified_or_not': self.qualified_or_not,
            'remarks': self.remarks,
            'attachments': json.loads(self.attachments) if self.attachments else [],
            'user_id': self.user_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

    def __repr__(self):
        return f"<OriginalRecords {self.task_name} - {self.survey_item}>"
