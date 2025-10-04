"""
数据库配置文件
"""
from flask_sqlalchemy import SQLAlchemy
import pymysql

# 安装 PyMySQL 作为 MySQLdb
pymysql.install_as_MySQLdb()

# 创建数据库实例
db = SQLAlchemy()

# 数据库配置
DATABASE_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:WASDijkl15963@localhost:3306/marine_survey_db?charset=utf8mb4',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'JSON_AS_ASCII': False
}

def init_db(app):
    """初始化数据库"""
    app.config.update(DATABASE_CONFIG)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return db
