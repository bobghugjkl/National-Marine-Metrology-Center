"""
CORS 跨域配置
"""
from flask_cors import CORS

CORS_CONFIG = {
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
}

def init_cors(app):
    """初始化 CORS"""
    CORS(app, resources=CORS_CONFIG)
    return app
