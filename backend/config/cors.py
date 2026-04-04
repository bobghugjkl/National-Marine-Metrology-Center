"""
CORS 跨域配置
"""
from flask_cors import CORS

CORS_CONFIG = {
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept", "X-Requested-With"],
        "supports_credentials": False,
        "expose_headers": ["Content-Type", "Authorization"],
        "vary_header": False
    }
}

def init_cors(app):
    """初始化 CORS（支持JWT认证）"""
    CORS(app, resources=CORS_CONFIG)
    return app
