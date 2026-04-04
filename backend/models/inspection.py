"""
航前质量监督检查记录模型
"""
from config.database import db

class PreVoyageInspection(db.Model):
    """航前质量监督检查记录表模型"""
    __tablename__ = 'tb_task_hqzljdjcjlb'
    
    task_name = db.Column(db.String(45), primary_key=True)
    check_date = db.Column(db.String(45))
    superintendent = db.Column(db.String(100))
    superintended = db.Column(db.String(100))
    check_1 = db.Column(db.Text)
    check_1_problem = db.Column(db.Text)
    check_2 = db.Column(db.Text)
    check_2_problem = db.Column(db.Text)
    check_3 = db.Column(db.Text)
    check_3_problem = db.Column(db.Text)
    check_4 = db.Column(db.Text)
    check_4_problem = db.Column(db.Text)
    check_5 = db.Column(db.Text)
    check_5_problem = db.Column(db.Text)
    check_6 = db.Column(db.Text)
    check_6_problem = db.Column(db.Text)
    check_7 = db.Column(db.Text)
    check_7_problem = db.Column(db.Text)
    check_8 = db.Column(db.Text)
    check_8_problem = db.Column(db.Text)
    check_9 = db.Column(db.Text)
    check_9_problem = db.Column(db.Text)
    check_10 = db.Column(db.Text)
    check_10_problem = db.Column(db.Text)
    check_11 = db.Column(db.Text)
    check_11_problem = db.Column(db.Text)
    check_detail = db.Column(db.Text)
    check_result = db.Column(db.Text)
    chief_scientist_sign = db.Column(db.String(100))
    chief_scientist_signdate = db.Column(db.String(45))
    check_leader_sign = db.Column(db.String(100))
    check_leader_signdate = db.Column(db.String(45))
    user_id = db.Column(db.Integer, nullable=False, comment='创建检查记录的用户ID')

    def to_dict(self):
        """转换为字典"""
        return {
            'task_name': self.task_name,
            'check_date': self.check_date,
            'superintendent': self.superintendent,
            'superintended': self.superintended,
            'check_1': self.check_1,
            'check_1_problem': self.check_1_problem,
            'check_2': self.check_2,
            'check_2_problem': self.check_2_problem,
            'check_3': self.check_3,
            'check_3_problem': self.check_3_problem,
            'check_4': self.check_4,
            'check_4_problem': self.check_4_problem,
            'check_5': self.check_5,
            'check_5_problem': self.check_5_problem,
            'check_6': self.check_6,
            'check_6_problem': self.check_6_problem,
            'check_7': self.check_7,
            'check_7_problem': self.check_7_problem,
            'check_8': self.check_8,
            'check_8_problem': self.check_8_problem,
            'check_9': self.check_9,
            'check_9_problem': self.check_9_problem,
            'check_10': self.check_10,
            'check_10_problem': self.check_10_problem,
            'check_11': self.check_11,
            'check_11_problem': self.check_11_problem,
            'check_detail': self.check_detail,
            'check_result': self.check_result,
            'chief_scientist_sign': self.chief_scientist_sign,
            'chief_scientist_signdate': self.chief_scientist_signdate,
            'check_leader_sign': self.check_leader_sign,
            'check_leader_signdate': self.check_leader_signdate,
            'user_id': self.user_id
        }
