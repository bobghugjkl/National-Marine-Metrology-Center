"""
CORS 跨域配置
"""
from flask_cors import CORS

CORS_CONFIG = {
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5000", "*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept", "X-Requested-With"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"]
    }
}

def init_cors(app):
    """初始化 CORS（支持JWT认证）"""
    CORS(app, resources=CORS_CONFIG)
    return app
