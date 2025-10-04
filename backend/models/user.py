"""
用户模型
"""
from config.database import db

class User(db.Model):
    """用户表模型"""
    __tablename__ = 'tb_user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    login_name = db.Column(db.String(45))
    password = db.Column(db.String(45))
    sex = db.Column(db.String(45))
    role = db.Column(db.String(45))
    desc = db.Column('desc', db.String(45))
    permission = db.Column(db.String(45))
    department = db.Column(db.String(255))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    signature = db.Column(db.Text)  # 手写签名数据（base64格式）

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'login_name': self.login_name,
            'password': self.password,
            'sex': self.sex,
            'role': self.role,
            'desc': self.desc,
            'permission': self.permission,
            'department': self.department,
            'email': self.email,
            'phone': self.phone,
            'signature': self.signature
        }
