"""
任务模型
"""
from config.database import db

class TaskInfo(db.Model):
    """任务信息表模型"""
    __tablename__ = 'tb_task_info'
    
    task_name = db.Column(db.String(45), primary_key=True)
    project = db.Column(db.String(100))
    participant = db.Column(db.Text)
    chief_scientist = db.Column(db.String(100))
    superintendent = db.Column(db.String(100))
    superintended = db.Column(db.String(100))
    executiontime = db.Column(db.String(100))
    subject = db.Column(db.Text)
    user_id = db.Column(db.Integer, nullable=False, comment='创建任务的用户ID')

    def to_dict(self):
        """转换为字典"""
        return {
            'task_name': self.task_name,
            'project': self.project,
            'participant': self.participant,
            'chief_scientist': self.chief_scientist,
            'superintendent': self.superintendent,
            'superintended': self.superintended,
            'executiontime': self.executiontime,
            'subject': self.subject,
            'user_id': self.user_id
        }
