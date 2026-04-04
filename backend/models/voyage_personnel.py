"""
航中外业调查人员表模型
"""
from datetime import datetime
import json
from config.database import db

class VoyagePersonnel(db.Model):
    """航中外业调查人员表模型"""
    __tablename__ = 'tb_voyage_personnel'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    name = db.Column(db.String(100), nullable=False, comment='姓名')
    sex = db.Column(db.String(10), nullable=False, comment='性别')
    birthdate = db.Column(db.Date, nullable=False, comment='出生年月')
    professional_title = db.Column(db.String(100), nullable=False, comment='职称')
    employer = db.Column(db.String(255), nullable=False, comment='工作单位')
    specialty = db.Column(db.String(255), nullable=False, comment='从事专业')
    instruments = db.Column(db.Text, comment='本航次操作仪器')
    training = db.Column(db.Text, comment='培训情况')
    remarks = db.Column(db.Text, comment='备注')
    attachments = db.Column(db.Text, comment='附件信息（JSON字符串）')
    user_id = db.Column(db.Integer, comment='创建用户ID（用户隔离）')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'name': self.name,
            'sex': self.sex,
            'birthdate': self.birthdate.strftime('%Y-%m-%d') if self.birthdate else None,
            'professional_title': self.professional_title,
            'employer': self.employer,
            'specialty': self.specialty,
            'instruments': self.instruments,
            'training': self.training,
            'remarks': self.remarks,
            'attachments': json.loads(self.attachments) if self.attachments else [],
            'user_id': self.user_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }
