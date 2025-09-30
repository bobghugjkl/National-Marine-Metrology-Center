# Flask 后端 API 文档

## 启动方式

1. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 启动服务：
```bash
python app.py
```

服务将运行在：`http://localhost:5000`

## 数据库配置

- 数据库：MySQL
- 数据库名：`marine_survey_db`
- 用户名：`root`
- 密码：`WASDijkl15963`
- 端口：`3306`

## API 接口说明

### 健康检查
- **GET** `/api/health` - 检查服务是否正常运行

### 用户管理
- **GET** `/api/users` - 获取所有用户
- **POST** `/api/users` - 创建用户
- **PUT** `/api/users/<name>` - 更新用户（按姓名）
- **DELETE** `/api/users/<name>` - 删除用户（按姓名）

### 任务管理
- **GET** `/api/tasks` - 获取所有任务
- **POST** `/api/tasks` - 创建任务
- **PUT** `/api/tasks/<task_name>` - 更新任务（按任务名）
- **DELETE** `/api/tasks/<task_name>` - 删除任务（按任务名）

### 基础人员管理
- **GET** `/api/masters` - 获取所有基础人员
- **POST** `/api/masters` - 创建基础人员
- **PUT** `/api/masters/<id_card_number>` - 更新基础人员（按身份证号）
- **DELETE** `/api/masters/<id_card_number>` - 删除基础人员（按身份证号）

### 角色管理
- **GET** `/api/roles` - 获取角色列表（暂时返回空数组）

## 响应格式

成功响应：
```json
{
  "code": 200,
  "data": [...],
  "message": "操作成功"
}
```

错误响应：
```json
{
  "code": 500,
  "message": "错误信息"
}
```

## 数据库表结构

### tb_user（用户表）
- name (主键)
- login_name
- password
- sex
- role
- desc
- permission
- department

### tb_task_info（任务信息表）
- task_name (主键)
- project
- task_code
- undertake
- participant
- ship
- leader
- chief_scientist
- superintendent
- superintended
- executiontime
- subject

### tb_base_master（基础人员表）
- id_card_number (主键)
- name
- sex
- birthday
- title
- organization
- major
- phone
- band_card_number
- opening_band
- remark
