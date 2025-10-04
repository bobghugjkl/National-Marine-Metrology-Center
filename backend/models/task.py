"""
任务模型
"""
from config.database import db

class TaskInfo(db.Model):
    """任务信息表模型"""
    __tablename__ = 'tb_task_info'

    task_name = db.Column(db.String(100), primary_key=True)
    project = db.Column(db.String(100))
    task_code = db.Column(db.String(100))
    undertake = db.Column(db.String(100))
    participant = db.Column(db.String(200))
    ship = db.Column(db.String(45))
    leader = db.Column(db.String(45))
    chief_scientist = db.Column(db.String(45))
    superintendent = db.Column(db.String(100))
    superintended = db.Column(db.String(45))
    executiontime = db.Column(db.Text)
    subject = db.Column(db.String(45))
    user_id = db.Column(db.Integer, nullable=False, comment='创建任务的用户ID')

    def to_dict(self):
        """转换为字典"""
        return {
            'task_name': self.task_name,
            'project': self.project,
            'task_code': self.task_code,
            'undertake': self.undertake,
            'participant': self.participant,
            'ship': self.ship,
            'leader': self.leader,
            'chief_scientist': self.chief_scientist,
            'superintendent': self.superintendent,
            'superintended': self.superintended,
            'executiontime': self.executiontime,
            'subject': self.subject,
            'user_id': self.user_id
        }
