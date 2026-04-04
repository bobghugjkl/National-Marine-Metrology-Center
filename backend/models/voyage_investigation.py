"""
航中外业调查项目/仪器比测统计表模型
"""
from datetime import datetime
import json
from config.database import db

class VoyageInvestigationProject(db.Model):
    """航中外业调查项目/仪器比测统计表模型"""
    __tablename__ = 'tb_voyage_investigation_project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    investigation_item_instrument = db.Column(db.String(255), nullable=False, comment='调查项目/仪器')
    comparison_unit_a_instrument = db.Column(db.String(255), comment='比测单位甲及仪器')
    comparison_unit_b_instrument = db.Column(db.String(255), comment='比测单位乙及仪器')
    comparison_time = db.Column(db.String(100), comment='比测时间')
    comparison_location = db.Column(db.String(255), comment='比测地点')
    comparison_result = db.Column(db.String(255), comment='比测结果')
    remarks = db.Column(db.Text, comment='备注')
    attachments = db.Column(db.Text, comment='附件列表，存储JSON字符串') # 存储附件的JSON字符串

    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), nullable=False, comment='创建用户ID')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    user = db.relationship('User', backref=db.backref('voyage_investigation_projects', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'investigation_item_instrument': self.investigation_item_instrument,
            'comparison_unit_a_instrument': self.comparison_unit_a_instrument,
            'comparison_unit_b_instrument': self.comparison_unit_b_instrument,
            'comparison_time': self.comparison_time,
            'comparison_location': self.comparison_location,
            'comparison_result': self.comparison_result,
            'remarks': self.remarks,
            'attachments': json.loads(self.attachments) if self.attachments else [],
            'user_id': self.user_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }

    def __repr__(self):
        return f"<VoyageInvestigationProject {self.task_name} - {self.investigation_item_instrument}>"
