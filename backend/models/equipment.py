"""
仪器设备（工作计量器具）表模型
"""
from datetime import datetime
import json
from config.database import db

class Equipment(db.Model):
    """仪器设备（工作计量器具）表模型"""
    __tablename__ = 'tb_equipment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(255), nullable=False, comment='航次任务名称')
    category = db.Column(db.String(100), nullable=False, comment='类别')
    name = db.Column(db.String(255), nullable=False, comment='仪器（标准物质）名称')
    number = db.Column(db.String(100), nullable=False, comment='编号')
    model = db.Column(db.String(100), nullable=False, comment='型号')
    traceability_method = db.Column(db.String(255), comment='量值溯源方式')
    calibration_date = db.Column(db.String(45), comment='检定/校准日期')
    certificate_number = db.Column(db.String(100), comment='证书编号')
    validity_period = db.Column(db.String(45), comment='有效期')
    calibration_organization = db.Column(db.String(255), comment='检定/校准机构')
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
            'category': self.category,
            'name': self.name,
            'number': self.number,
            'model': self.model,
            'traceability_method': self.traceability_method,
            'calibration_date': self.calibration_date,
            'certificate_number': self.certificate_number,
            'validity_period': self.validity_period,
            'calibration_organization': self.calibration_organization,
            'remarks': self.remarks,
            'attachmentList': attachment_list,
            'user_id': self.user_id,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None,
        }
