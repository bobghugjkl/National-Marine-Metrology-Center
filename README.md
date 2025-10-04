# 🌊 海洋调查现场质量监督管理系统

> 基于 Vue 3 + Flask + MySQL 的全栈海洋调查质量监督管理平台

[![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen.svg)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-blue.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## 📚 快速导航

| 🚀 快速开始 | 📖 文档中心 | 🗄️ 数据库 | 📝 更新日志 |
|:---:|:---:|:---:|:---:|
| [启动指南](#-快速开始) | [📚 文档索引](./docs/README.md) | [数据库说明](./docs/数据库说明.md) | [CHANGELOG](./CHANGELOG.md) |

---

## 📋 项目简介

海洋调查现场质量监督管理系统是一个专为海洋调查任务设计的全栈管理平台，支持任务管理、人员管理、设备管理、航前/航中质量检查等核心功能。系统采用前后端分离架构，具备用户隔离、权限管理、实时数据同步等特性。

### ✨ 核心特性

- 🔐 **用户隔离机制** - 每个用户只能查看和管理自己创建的数据
- 📊 **任务全生命周期管理** - 从任务创建到质量检查的完整流程
- 🔍 **智能搜索与过滤** - 支持多条件搜索和数据筛选
- 🎨 **现代化 UI** - 基于 Element Plus 的美观界面
- 🏗️ **MVC 架构** - 后端采用标准 MVC 模式，代码清晰易维护
- 🔄 **实时数据同步** - 前后端数据自动同步，无需刷新

---

## 🚀 快速开始

### 环境要求

| 工具 | 版本要求 |
|------|---------|
| Node.js | >= 16.x |
| Python | >= 3.11 |
| MySQL | >= 8.0 |

### 1️⃣ 数据库准备

#### 方式一：使用完整备份（推荐）

```bash
# 导入最新数据库备份（包含用户隔离功能）
mysql -u root -p < marine_survey_db_latest.sql
```

#### 方式二：使用旧版 SQL

```bash
# 如果使用旧版 SQL，需要手动执行结构更新
mysql -u root -p < mysql_final.sql
cd backend
python update_database_structure.py
```

**数据库配置信息：**
- 📌 数据库名：`marine_survey_db`
- 👤 用户名：`root`
- 🔑 密码：`WASDijkl15963`（根据实际情况修改）

### 2️⃣ 后端启动

```bash
# 进入后端目录
cd backend

# 安装 Python 依赖
pip install -r requirements.txt

# 启动 Flask 服务（统一入口）
python app.py
```

✅ 后端运行地址：`http://localhost:5000`

**提供的服务：**
- 用户管理 (`/api/users`)
- 登录注册 (`/api/login`, `/api/register`)
- 任务管理 (`/api/tasks`)
- 检查记录管理 (`/api/inspections`)

### 3️⃣ 前端启动

```bash
# 回到项目根目录
cd ..

# 安装依赖（首次运行）
npm install
# 或
yarn install

# 启动开发服务器
npm run dev
# 或
yarn dev
```

✅ 前端访问地址：`http://localhost:5173`

---

## 📂 项目结构

```
vue-manage-system/
├── backend/                    # 后端服务
│   ├── app.py                 # Flask 应用入口（MVC 架构）
│   ├── config/                # 配置文件
│   │   ├── database.py       # 数据库配置
│   │   └── cors.py           # CORS 配置
│   ├── models/                # 数据模型
│   │   ├── user.py           # 用户模型
│   │   ├── task.py           # 任务模型
│   │   ├── inspection.py     # 检查记录模型
│   │   └── master.py         # 人员模型
│   ├── controllers/           # 控制器（路由）
│   │   ├── user_controller.py
│   │   ├── auth_controller.py
│   │   ├── task_controller.py
│   │   └── inspection_controller.py
│   └── requirements.txt       # Python 依赖
├── src/                       # 前端源码
│   ├── api/                  # API 接口
│   │   ├── index.ts          # 用户/人员 API
│   │   ├── task.ts           # 任务 API
│   │   └── inspection.ts     # 检查记录 API
│   ├── views/                # 页面视图
│   │   ├── VoyageInfo/       # 任务管理
│   │   ├── preVoyageInspection/  # 航前检查
│   │   ├── pages/            # 登录注册等
│   │   └── system/           # 系统管理
│   ├── components/           # 通用组件
│   ├── router/               # 路由配置
│   └── utils/                # 工具函数
├── docs/                      # 📚 项目文档
│   ├── 数据库说明.md
│   ├── 用户隔离功能说明.md
│   ├── 后端MVC重构说明.md
│   ├── 增删改查实现原理详解.md
│   └── ... （更多文档）
├── marine_survey_db_latest.sql  # 最新数据库备份
└── README.md                  # 本文件
```

---

## 🗄️ 数据库说明

### 核心表结构（10张表）

| 表名 | 说明 | 用户隔离 |
|------|------|---------|
| `tb_user` | 用户表（含自增 ID） | ✅ 主表 |
| `tb_task_info` | 任务信息表 | ✅ |
| `tb_task_hqzljdjcjlb` | 航前质量监督检查记录表 | ✅ |
| `tb_base_master` | 基础人员信息表 | ✅ |
| `tb_base_hq_investigator` | 航前调查人员表 | - |
| `tb_base_hq_device` | 航前设备表 | - |
| `tb_base_hz_investigator` | 航中调查人员表 | - |
| `tb_base_hz_device` | 航中设备表 | - |
| `tb_task_sczljdjcb` | 生产质量监督检查表 | - |
| `tb_task_zlpgb` | 质量评估表 | - |

### 用户隔离机制

- ✅ `tb_user` 表新增自增主键 `id`
- ✅ 关键表新增 `user_id` 字段
- ✅ 每个用户只能看到自己创建的数据
- ✅ 登录时自动保存 `userId` 到 localStorage
- ✅ 所有请求自动携带 `user_id` 参数

**详细说明**：请查看 [`docs/数据库说明.md`](./docs/数据库说明.md)

---

## 🔑 测试账号

| ID | 用户名 | 登录名 | 密码 | 角色 | 说明 |
|----|--------|--------|------|------|------|
| 1 | 111 | test | 123456 | 测试用户 | - |
| 2 | 12 | 12 | 12 | - | - |
| 3 | 123 | 123 | 123456 | 普通用户 | **所有现有任务的所有者** |
| 4 | admin | admin | 123456 | 超级管理员 | - |

> **注意**：所有预置任务数据的 `user_id=3`，登录用户 `123` 可查看全部任务

---

## ⚙️ 功能清单

### 用户功能
- ✅ 用户注册/登录
- ✅ 用户信息管理（增删改查）
- ✅ 基于用户的数据隔离
- ✅ 密码验证与错误提示

### 任务管理
- ✅ 任务创建/编辑/删除
- ✅ 任务搜索与重置
- ✅ 任务列表分页展示
- ✅ 任务与检查记录自动关联

### 航前质量检查
- ✅ 11项质量检查内容
- ✅ 检查记录编辑与保存
- ✅ 任务与检查记录一对一关联
- ✅ 自动创建/删除检查记录

### 界面优化
- ✅ 现代化 UI 设计
- ✅ 响应式布局
- ✅ 友好的错误提示
- ✅ 流畅的页面跳转

---

## 🛠️ 技术栈

### 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.x | 前端框架 |
| Vite | 最新 | 构建工具 |
| TypeScript | 最新 | 类型支持 |
| Element Plus | 最新 | UI 组件库 |
| Axios | 最新 | HTTP 请求 |
| Vue Router | 4.x | 路由管理 |
| Pinia | 最新 | 状态管理 |

### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Flask | 3.0 | Web 框架 |
| Flask-SQLAlchemy | 3.1.1 | ORM |
| Flask-CORS | 4.0.0 | 跨域支持 |
| PyMySQL | 1.1.0 | MySQL 驱动 |
| SQLAlchemy | 2.0.23 | 数据库工具 |

### 数据库

- **MySQL** 8.0
- 字符集：`utf8mb4`
- 引擎：`InnoDB`

---

## 📡 API 接口

### 用户认证
```bash
POST /api/login       # 用户登录
POST /api/register    # 用户注册
```

### 用户管理
```bash
GET    /api/users           # 获取用户列表
POST   /api/users           # 创建用户
PUT    /api/users/:name     # 更新用户
DELETE /api/users/:name     # 删除用户
```

### 任务管理
```bash
GET    /api/tasks                # 获取任务列表（支持 user_id 过滤）
POST   /api/tasks                # 创建任务
PUT    /api/tasks/:task_name     # 更新任务
DELETE /api/tasks/:task_name     # 删除任务
```

### 检查记录
```bash
GET    /api/inspections/:task_name    # 获取检查记录（支持 user_id 过滤）
PUT    /api/inspections/:task_name    # 更新检查记录
```

### 健康检查
```bash
GET /api/health    # 服务健康检查
```

**详细 API 文档**：请查看 [`docs/增删改查实现原理详解.md`](./docs/增删改查实现原理详解.md)

---

## 📚 文档中心

项目文档已整理到 [`docs/`](./docs/) 目录，包含：

### 核心功能文档
- 📘 [数据库说明](./docs/数据库说明.md) - 完整的数据库结构说明
- 📗 [用户隔离功能说明](./docs/用户隔离功能说明.md) - 用户数据隔离实现
- 📕 [后端MVC重构说明](./docs/后端MVC重构说明.md) - 后端架构说明
- 📙 [增删改查实现原理详解](./docs/增删改查实现原理详解.md) - CRUD 教程

### 功能实现文档
- [任务管理功能说明](./docs/任务管理功能说明.md)
- [航前检查功能说明](./docs/航前检查功能说明.md)
- [登录注册功能说明](./docs/登录注册功能说明.md)
- [搜索功能说明](./docs/搜索功能说明.md)

### 修复与优化
- [问题修复说明](./docs/问题修复说明.md)
- [检查记录页面跳转修复说明](./docs/检查记录页面跳转修复说明.md)
- [菜单整合说明](./docs/菜单整合说明.md)

### 快速开始
- [重构完成-快速开始](./docs/重构完成-快速开始.md)
- [启动说明](./docs/启动说明.md)

---

## 🔧 开发配置

### 后端配置

修改 `backend/app.py`：

```python
# 数据库连接配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/marine_survey_db'
)
```

### 前端配置

修改 `src/utils/request.ts`：

```typescript
const service: AxiosInstance = axios.create({
    baseURL: 'http://localhost:5000/api',  // 后端地址
    timeout: 5000
});
```

---

## 🐛 常见问题

### 1. 数据库连接失败
**问题**：`Can't connect to MySQL server`

**解决**：
- 检查 MySQL 服务是否启动
- 确认数据库密码是否正确
- 检查防火墙设置

### 2. 用户隔离不生效
**问题**：用户可以看到其他用户的数据

**解决**：
- 确保已重新登录（localStorage 中有 `userId`）
- 检查浏览器控制台的网络请求是否携带 `user_id`
- 查看后端日志，确认接收到 `user_id` 参数

### 3. 后端跨域错误
**问题**：`CORS policy: No 'Access-Control-Allow-Origin' header`

**解决**：
- 确保后端已启动
- 检查 `backend/config/cors.py` 配置
- 清除浏览器缓存后重试

### 4. 前端构建失败
**问题**：`npm install` 或 `npm run dev` 报错

**解决**：
```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm cache clean --force

# 重新安装
npm install

# 使用 yarn（推荐）
yarn install
```

### 5. Python 依赖安装失败
**问题**：`pip install` 超时或报错

**解决**：
```bash
# 使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 🎯 开发路线图

### ✅ 已完成功能（2025年9月）
- [x] 用户隔离机制
- [x] 后端 MVC 架构重构
- [x] 任务管理完整 CRUD
- [x] 航前检查记录管理
- [x] 登录注册功能
- [x] 搜索与过滤功能
- [x] UI 美化与优化

### 🚧 开发中
- [ ] 航中质量检查功能
- [ ] 质量评估功能
- [ ] 数据报表与导出
- [ ] 文件上传与附件管理

### 📅 未来计划
- [ ] 权限管理系统
- [ ] 消息通知功能
- [ ] 数据备份与恢复
- [ ] 移动端适配
- [ ] 国际化支持

---

## 👥 团队协作

### Git 工作流程

```bash
# 1. 克隆项目
git clone <repository-url>

# 2. 创建功能分支
git checkout -b feature/your-feature-name

# 3. 提交更改
git add .
git commit -m "feat: 添加某某功能"

# 4. 推送到远程
git push origin feature/your-feature-name

# 5. 创建 Pull Request
```

### 提交规范

| 类型 | 说明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修复 |
| `docs:` | 文档更新 |
| `style:` | 代码格式调整 |
| `refactor:` | 代码重构 |
| `test:` | 测试相关 |
| `chore:` | 构建/工具链更新 |

---

## 📄 开源协议

本项目基于 [MIT License](./LICENSE) 开源。

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 提交 [Issue](../../issues)
- 💬 发起 [Discussion](../../discussions)
- 📝 查看 [Wiki](../../wiki)

---

## 🙏 致谢

感谢以下开源项目：

- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - Vue 3 组件库
- [Flask](https://flask.palletsprojects.com/) - Python Web 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM

---

