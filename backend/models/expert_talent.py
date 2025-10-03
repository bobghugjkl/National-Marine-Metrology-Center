"""
专家人才模型
"""
from config.database import db

class ExpertTalent(db.Model):
    """专家人才模型"""
    __tablename__ = 'tb_expert_talent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.String(10), comment='性别')
    birth_date = db.Column(db.String(20), comment='出生年月')
    job_title = db.Column(db.String(50), comment='职称')
    work_unit = db.Column(db.String(100), comment='工作单位')
    specialty = db.Column(db.String(100), comment='从事专业')
    contact_info = db.Column(db.String(50), comment='联系方式')
    id_number = db.Column(db.String(20), comment='身份证号')
    bank_card_number = db.Column(db.String(30), comment='银行卡号')
    opening_bank = db.Column(db.String(100), comment='开户行')
    remarks = db.Column(db.Text, comment='备注')
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户ID')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'job_title': self.job_title,
            'work_unit': self.work_unit,
            'specialty': self.specialty,
            'contact_info': self.contact_info,
            'id_number': self.id_number,
            'bank_card_number': self.bank_card_number,
            'opening_bank': self.opening_bank,
            'remarks': self.remarks,
            'user_id': self.user_id
        }
