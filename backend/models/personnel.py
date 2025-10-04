"""
外业调查人员资质表模型
"""
from datetime import datetime
import json
from config.database import db

class PersonnelQualification(db.Model):
    """外业调查人员资质表模型"""
    __tablename__ = 'tb_personnel_qualifications'
    
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
        attachment_list = []
        if self.attachments:
            try:
                attachment_list = json.loads(self.attachments)
            except:
                attachment_list = []
                
        return {
            'id': self.id,
            'task_name': self.task_name,
            'name': self.name,
            'gender': self.sex,  # 前端使用gender字段
            'birth_date': self.birthdate.strftime('%Y-%m') if self.birthdate else '',
            'title': self.professional_title,  # 前端使用title字段
            'work_unit': self.employer,  # 前端使用work_unit字段
            'major': self.specialty,  # 前端使用major字段
            'instruments': self.instruments,
            'training': self.training,
            'remark': self.remarks,  # 前端使用remark字段
            'attachmentList': attachment_list,
            'user_id': self.user_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else '',
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else ''
        }
    
    @staticmethod
    def from_dict(data, user_id=None):
        """从字典创建或更新实例"""
        instance = PersonnelQualification()
        
        instance.task_name = data.get('task_name')
        instance.name = data.get('name')
        instance.sex = data.get('gender')  # 前端使用gender字段
        
        # 处理日期字段
        birth_date = data.get('birth_date')
        if birth_date:
            if len(birth_date) == 7:  # 只有年月 YYYY-MM
                birth_date = f"{birth_date}-01"  # 添加日期
            instance.birthdate = datetime.strptime(birth_date, '%Y-%m-%d').date()
            
        instance.professional_title = data.get('title')  # 前端使用title字段
        instance.employer = data.get('work_unit')  # 前端使用work_unit字段
        instance.specialty = data.get('major')  # 前端使用major字段
        instance.instruments = data.get('instruments')
        instance.training = data.get('training')
        instance.remarks = data.get('remark')  # 前端使用remark字段
        
        # 处理附件列表
        attachment_list = data.get('attachmentList', [])
        if attachment_list:
            instance.attachments = json.dumps(attachment_list)
        
        # 设置用户ID（用于用户隔离）
        if user_id is not None:
            instance.user_id = user_id
            
        return instance
