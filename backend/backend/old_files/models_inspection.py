from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PreVoyageInspection(db.Model):
    """航前质量监督检查记录表模型"""
    __tablename__ = 'tb_task_hqzljdjcjlb'
    
    task_name = db.Column(db.String(100), primary_key=True, comment='航次任务名称')
    check_date = db.Column(db.Text, comment='检查日期')
    superintendent = db.Column(db.String(100), comment='监督员')
    superintended = db.Column(db.String(45), comment='被监督')
    
    # 检查项1-11（检查内容和存在问题）
    check_1 = db.Column(db.String(200), comment='检查内容1')
    check_1_problem = db.Column(db.String(200), comment='存在问题1')
    check_2 = db.Column(db.String(200), comment='检查内容2')
    check_2_problem = db.Column(db.String(200), comment='存在问题2')
    check_3 = db.Column(db.String(200), comment='检查内容3')
    check_3_problem = db.Column(db.String(200), comment='存在问题3')
    check_4 = db.Column(db.String(200), comment='检查内容4')
    check_4_problem = db.Column(db.String(200), comment='存在问题4')
    check_5 = db.Column(db.String(200), comment='检查内容5')
    check_5_problem = db.Column(db.String(200), comment='存在问题5')
    check_6 = db.Column(db.String(200), comment='检查内容6')
    check_6_problem = db.Column(db.String(200), comment='存在问题6')
    check_7 = db.Column(db.String(200), comment='检查内容7')
    check_7_problem = db.Column(db.String(200), comment='存在问题7')
    check_8 = db.Column(db.String(200), comment='检查内容8')
    check_8_problem = db.Column(db.String(200), comment='存在问题8')
    check_9 = db.Column(db.String(200), comment='检查内容9')
    check_9_problem = db.Column(db.String(200), comment='存在问题9')
    check_10 = db.Column(db.String(200), comment='检查内容10')
    check_10_problem = db.Column(db.String(200), comment='存在问题10')
    check_11 = db.Column(db.String(200), comment='检查内容11')
    check_11_problem = db.Column(db.String(200), comment='存在问题11')
    
    # 其他字段
    check_detail = db.Column(db.Text, comment='检查详情')
    check_result = db.Column(db.Text, comment='检查结果')
    chief_scientist_sign = db.Column(db.String(45), comment='首席科学家签字')
    check_leader_sign = db.Column(db.String(45), comment='检查组长签字')
    chief_scientist_signdate = db.Column(db.Date, comment='首席科学家签字日期')
    check_leader_signdate = db.Column(db.Date, comment='检查组长签字日期')
    create_date = db.Column(db.Text, comment='创建日期')
    
    def to_dict(self):
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
            'check_leader_sign': self.check_leader_sign,
            'chief_scientist_signdate': str(self.chief_scientist_signdate) if self.chief_scientist_signdate else None,
            'check_leader_signdate': str(self.check_leader_signdate) if self.check_leader_signdate else None,
            'create_date': self.create_date
        }
