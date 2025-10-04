# 🌊 海洋调查管理系统 - 后端服务

基于 Flask 的 MVC 架构后端服务

## 📂 项目结构

```
backend/
├── app.py                    # 🚀 启动入口
├── config/                   # ⚙️ 配置层
│   ├── database.py          # 数据库配置
│   └── cors.py              # CORS 配置
├── models/                   # 📊 模型层
│   ├── user.py              # 用户模型
│   ├── task.py              # 任务模型
│   ├── inspection.py        # 检查记录模型
│   └── master.py            # 基本人员模型
├── controllers/              # 🎮 控制器层
│   ├── user_controller.py   # 用户管理
│   ├── auth_controller.py   # 认证（登录/注册）
│   ├── task_controller.py   # 任务管理
│   └── inspection_controller.py  # 检查记录
└── utils/                    # 🛠️ 工具类
```

## 🚀 快速启动

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

### 3. 访问服务

- 服务地址：http://localhost:5000
- 健康检查：http://localhost:5000/api/health

## 📡 API 接口

### 用户管理
- `GET /api/users` - 获取用户列表（支持搜索）
- `POST /api/users` - 创建用户
- `PUT /api/users/<name>` - 更新用户
- `DELETE /api/users/<name>` - 删除用户

### 认证
- `POST /api/login` - 用户登录
- `POST /api/register` - 用户注册

### 任务管理
- `GET /api/tasks` - 获取任务列表
- `POST /api/tasks` - 创建任务
- `PUT /api/tasks/<task_name>` - 更新任务
- `DELETE /api/tasks/<task_name>` - 删除任务

### 检查记录
- `GET /api/inspections/task/<task_name>` - 获取检查记录
- `PUT /api/inspections/<task_name>` - 更新检查记录

## 🗄️ 数据库配置

- **类型**：MySQL
- **地址**：localhost:3306
- **数据库**：marine_survey_db
- **配置文件**：`config/database.py`

## 🏗️ MVC 架构

### Model (模型层)
- 定义数据库表结构
- 提供 `to_dict()` 方法用于序列化

### Controller (控制器层)
- 处理 HTTP 请求
- 调用 Model 进行数据操作
- 返回 JSON 响应

### Config (配置层)
- 数据库配置
- CORS 跨域配置
- 其他应用配置

## 📝 开发规范

### 添加新功能

1. **添加模型** (models/)
   ```python
   from config.database import db
   
   class NewModel(db.Model):
       __tablename__ = 'tb_new'
       # 定义字段...
   ```

2. **添加控制器** (controllers/)
   ```python
   from flask import Blueprint
   
   new_bp = Blueprint('new', __name__, url_prefix='/api')
   
   @new_bp.route('/new', methods=['GET'])
   def get_new():
       # 业务逻辑...
   ```

3. **注册蓝图** (app.py)
   ```python
   from controllers import new_bp
   app.register_blueprint(new_bp)
   ```

## 🧪 测试

### 健康检查
```bash
curl http://localhost:5000/api/health
```

### 获取用户列表
```bash
curl http://localhost:5000/api/users
```

### 登录
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}'
```

## 📦 依赖

- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-CORS==4.0.0
- PyMySQL==1.1.0
- SQLAlchemy==2.0.23

## 🔧 配置说明

### 数据库连接 (config/database.py)
```python
DATABASE_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://user:pass@localhost/db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'JSON_AS_ASCII': False
}
```

### CORS 配置 (config/cors.py)
```python
CORS_CONFIG = {
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
}
```

## ⚠️ 注意事项

1. **生产环境部署**
   - 关闭 DEBUG 模式
   - 使用生产级 WSGI 服务器（如 Gunicorn）
   - 配置环境变量管理敏感信息

2. **数据库迁移**
   - 使用 Flask-Migrate 进行数据库版本管理
   - 定期备份数据库

3. **安全性**
   - 实现 JWT 或 Session 认证
   - 添加请求速率限制
   - 对密码进行加密存储

## 📚 相关文档

- [后端 MVC 重构说明](../后端MVC重构说明.md)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy 文档](https://flask-sqlalchemy.palletsprojects.com/)

---

**版本**：2.0.0 (MVC 重构版)  
**最后更新**：2025年9月30日