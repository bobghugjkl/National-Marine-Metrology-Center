"""
外业调查操作规程执行统计表模型
"""
from datetime import datetime
import json
from config.database import db

class ProcedureExecution(db.Model):
    """外业调查操作规程执行统计表模型"""
    __tablename__ = 'tb_procedure_execution'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    investigation_item_instrument = db.Column(db.String(255), comment='调查项目/仪器')
    task_undertaking_unit = db.Column(db.String(255), comment='任务承担单位')
    has_operating_procedures = db.Column(db.String(45), comment='是否具有操作规程')
    operating_procedure_name = db.Column(db.String(255), comment='操作规程名称')
    remarks = db.Column(db.Text, comment='备注')
    attachments = db.Column(db.Text, comment='附件列表，存储JSON字符串') # 存储附件的JSON字符串

    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False, comment='创建用户ID')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    user = db.relationship('User', backref=db.backref('procedure_execution', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'investigation_item_instrument': self.investigation_item_instrument,
            'task_undertaking_unit': self.task_undertaking_unit,
            'has_operating_procedures': self.has_operating_procedures,
            'operating_procedure_name': self.operating_procedure_name,
            'remarks': self.remarks,
            'attachments': json.loads(self.attachments) if self.attachments else [],
            'user_id': self.user_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

    def __repr__(self):
        return f"<ProcedureExecution {self.task_name} - {self.investigation_item_instrument}>"
