"""
任务单位模型
"""
from config.database import db

class TaskUnit(db.Model):
    """任务单位模型"""
    __tablename__ = 'tb_task_unit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_name = db.Column(db.String(100), nullable=False, comment='单位名称')
    specialized_person = db.Column(db.String(50), comment='专项负责人')
    quality_manager = db.Column(db.String(50), comment='质量管理负责人')
    contact_person = db.Column(db.String(50), comment='联系人')
    contact_info = db.Column(db.String(50), comment='联系方式')
    remarks = db.Column(db.Text, comment='备注')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户ID')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'unit_name': self.unit_name,
            'specialized_person': self.specialized_person,
            'quality_manager': self.quality_manager,
            'contact_person': self.contact_person,
            'contact_info': self.contact_info,
            'remarks': self.remarks,
            'user_id': self.user_id
        }
