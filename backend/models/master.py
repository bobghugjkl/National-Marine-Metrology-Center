"""
基本人员信息模型
"""
from config.database import db

class BaseMaster(db.Model):
    """基本人员信息表模型"""
    __tablename__ = 'tb_base_master'
    
    id_card_number = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    phone = db.Column(db.String(45))
    department = db.Column(db.String(100))
    post = db.Column(db.String(100))
    user_id = db.Column(db.Integer, nullable=False, comment='创建人员信息的用户ID')

    def to_dict(self):
        """转换为字典"""
        return {
            'id_card_number': self.id_card_number,
            'name': self.name,
            'sex': self.sex,
            'phone': self.phone,
            'department': self.department,
            'post': self.post,
            'user_id': self.user_id
        }
