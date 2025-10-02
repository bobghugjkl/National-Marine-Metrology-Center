#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app
from backend.models.voyage_personnel import VoyagePersonnel
from backend.config.database import db
import json

def test_attachment_save():
    """测试附件保存功能"""
    with app.app_context():
        # 查找一条记录
        record = VoyagePersonnel.query.first()
        if not record:
            print("没有找到记录，请先创建一条记录")
            return
        
        print(f"找到记录: {record.name}")
        print(f"当前附件信息: {record.attachments}")
        
        # 模拟附件数据
        test_attachments = [
            {
                "filename": "test_file.pdf",
                "url": "http://localhost:5000/static/uploads/test_file.pdf",
                "size": 1024
            }
        ]
        
        # 更新附件信息
        record.attachments = json.dumps(test_attachments)
        db.session.commit()
        
        print(f"更新后附件信息: {record.attachments}")
        
        # 验证更新
        updated_record = VoyagePersonnel.query.get(record.id)
        attachments = json.loads(updated_record.attachments) if updated_record.attachments else []
        print(f"验证附件信息: {attachments}")
        
        if attachments:
            print("✅ 附件保存成功！")
        else:
            print("❌ 附件保存失败！")

if __name__ == "__main__":
    test_attachment_save()
