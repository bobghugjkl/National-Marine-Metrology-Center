#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务数据模型
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TaskInfo(db.Model):
    __tablename__ = 'tb_task_info'
    
    task_name = db.Column(db.String(100), primary_key=True)  # 任务名称（主键）
    project = db.Column(db.String(100))  # 专项名称
    task_code = db.Column(db.String(100))  # 航次任务编号
    undertake = db.Column(db.String(100))  # 航次承担单位
    participant = db.Column(db.String(200))  # 航次参与单位
    ship = db.Column(db.String(45))  # 调查船
    leader = db.Column(db.String(45))  # 任务负责人
    chief_scientist = db.Column(db.String(45))  # 首席科学家
    superintendent = db.Column(db.String(100))  # 随船监督员
    superintended = db.Column(db.String(45))  # 随船监督
    executiontime = db.Column(db.Text)  # 执行时间
    subject = db.Column(db.String(45))  # 任务学科
    
    def to_dict(self):
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
            'subject': self.subject
        }
