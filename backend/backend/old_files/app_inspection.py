"""
航前质量监督检查记录管理后端
端口: 5002
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models_inspection import db
from routes_inspection import inspection_bp
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:WASDijkl15963@localhost:3306/marine_survey_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# 初始化数据库
db.init_app(app)

# CORS配置
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 注册蓝图
app.register_blueprint(inspection_bp)

# 健康检查
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'success', 'message': '航前检查记录后端运行正常'})

if __name__ == '__main__':
    print('航前检查记录后端已启动: http://localhost:5002')
    app.run(debug=True, port=5002, host='0.0.0.0')
