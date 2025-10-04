"""
外业调查项目/仪器比测统计表模型
"""
from datetime import datetime
import json
from config.database import db

class InvestigationProject(db.Model):
    """外业调查项目/仪器比测统计表模型"""
    __tablename__ = 'tb_investigation_projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    investigation_item = db.Column(db.String(255), nullable=False, comment='调查项目/仪器')
    unit_a_instrument = db.Column(db.String(255), nullable=False, comment='比测单位甲仪器')
    unit_b_instrument = db.Column(db.String(255), nullable=False, comment='比测单位乙仪器')
    comparison_time = db.Column(db.String(45), comment='比测时间')
    comparison_location = db.Column(db.String(255), comment='比测地点')
    comparison_result = db.Column(db.Text, comment='比测结果')
    remarks = db.Column(db.Text, comment='备注')
    attachments = db.Column(db.Text, comment='附件信息（JSON字符串）')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户ID（用户隔离）')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        """转换为字典"""
        attachment_list = []
        if self.attachments:
            try:
                attachment_list = json.loads(self.attachments)
            except:
                attachment_list = []

        return {
            'id': self.id,
            'task_name': self.task_name,
            'investigation_item': self.investigation_item,
            'unit_a_instrument': self.unit_a_instrument,
            'unit_b_instrument': self.unit_b_instrument,
            'comparison_time': self.comparison_time,
            'comparison_location': self.comparison_location,
            'comparison_result': self.comparison_result,
            'remarks': self.remarks,
            'attachmentList': attachment_list,
            'user_id': self.user_id,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None,
        }
