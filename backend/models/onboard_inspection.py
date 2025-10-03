"""
随船质量监督检查表模型
"""
from config.database import db

class OnboardInspection(db.Model):
    """随船质量监督检查表模型"""
    __tablename__ = 'tb_onboard_inspection'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(100), nullable=False, comment='航次任务名称')
    inspected_unit = db.Column(db.String(200), comment='被检查承担单位')
    participating_unit = db.Column(db.String(200), comment='被检查参加单位')
    task_code = db.Column(db.String(100), comment='航次任务编号')
    chief_scientist = db.Column(db.String(100), comment='航次首席科学家')
    inspection_date = db.Column(db.String(50), comment='检查日期')
    onboard_supervisor = db.Column(db.String(100), comment='随船质量监督员')
    inspected_unit_personnel = db.Column(db.String(200), comment='被检查单位(部门)主要参与人员')
    
    # 检查内容（12项）
    check_1 = db.Column(db.Text, comment='检查内容1')
    check_1_problem = db.Column(db.Text, comment='存在问题1')
    check_2 = db.Column(db.Text, comment='检查内容2')
    check_2_problem = db.Column(db.Text, comment='存在问题2')
    check_3 = db.Column(db.Text, comment='检查内容3')
    check_3_problem = db.Column(db.Text, comment='存在问题3')
    check_4 = db.Column(db.Text, comment='检查内容4')
    check_4_problem = db.Column(db.Text, comment='存在问题4')
    check_5 = db.Column(db.Text, comment='检查内容5')
    check_5_problem = db.Column(db.Text, comment='存在问题5')
    check_6 = db.Column(db.Text, comment='检查内容6')
    check_6_problem = db.Column(db.Text, comment='存在问题6')
    check_7 = db.Column(db.Text, comment='检查内容7')
    check_7_problem = db.Column(db.Text, comment='存在问题7')
    check_8 = db.Column(db.Text, comment='检查内容8')
    check_8_problem = db.Column(db.Text, comment='存在问题8')
    check_9 = db.Column(db.Text, comment='检查内容9')
    check_9_problem = db.Column(db.Text, comment='存在问题9')
    check_10 = db.Column(db.Text, comment='检查内容10')
    check_10_problem = db.Column(db.Text, comment='存在问题10')
    check_11 = db.Column(db.Text, comment='检查内容11')
    check_11_problem = db.Column(db.Text, comment='存在问题11')
    check_12 = db.Column(db.Text, comment='检查内容12')
    check_12_problem = db.Column(db.Text, comment='存在问题12')
    
    # 签名信息
    team_leader_sign = db.Column(db.String(100), comment='组长签字')
    task_leader_sign = db.Column(db.String(100), comment='任务负责人签字')
    
    # 附件
    attachments = db.Column(db.Text, comment='附件信息(JSON格式)')
    
    # 用户ID
    user_id = db.Column(db.Integer, nullable=False, comment='创建用户ID')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'inspected_unit': self.inspected_unit,
            'participating_unit': self.participating_unit,
            'task_code': self.task_code,
            'chief_scientist': self.chief_scientist,
            'inspection_date': self.inspection_date,
            'onboard_supervisor': self.onboard_supervisor,
            'inspected_unit_personnel': self.inspected_unit_personnel,
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
            'check_12': self.check_12,
            'check_12_problem': self.check_12_problem,
            'team_leader_sign': self.team_leader_sign,
            'task_leader_sign': self.task_leader_sign,
            'attachments': self.attachments,
            'user_id': self.user_id
        }
