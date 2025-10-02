# 🌊 外业调查人员资质管理前端页面使用说明

## 📋 功能概述

本页面实现了外业调查人员资质一览表的前端展示和管理功能，包括：

- 📊 人员资质列表展示（带分页）
- ➕ 新增人员资质记录
- ✏️ 编辑已有资质记录
- 🔍 按条件搜索人员资质
- 🗑️ 删除和批量删除功能
- 📥 Excel模板下载和文件导入
- 📎 附件上传和管理
- 👁️ 人员资质详情查看

## 🖥️ 界面预览

页面布局包含：
- **顶部标题栏**：显示"外业调查人员资质一览表"，右侧放置操作按钮
- **搜索区域**：支持按航次任务名称、姓名、工作单位筛选
- **数据表格**：展示人员资质信息，支持排序、分页等操作
- **弹窗表单**：新增/编辑人员资质信息的表单

## 🔌 后端API接口要求

为了让前端页面正常工作，后端需要实现以下RESTful API接口：

### 基础CRUD接口

```javascript
// 1. 获取人员资质列表（支持分页和搜索）
GET /api/personnel-qualifications
Query参数：
- page: 页码 (默认1)
- pageSize: 每页数量 (默认10)
- task_name: 航次任务名称（可选）
- name: 姓名（可选）
- employer: 工作单位（可选）

响应格式：
{
  "code": 200,
  "data": {
    "list": [
      {
        "id": 1,
        "task_name": "2024年春季海洋调查",
        "name": "张三",
        "sex": "男",
        "birthdate": "1985-06-15",
        "professional_title": "高级工程师",
        "employer": "海洋研究所",
        "specialty": "海洋地质",
        "instruments": "CTD、多参数水质仪",
        "training": "海洋调查技术培训",
        "remarks": "有丰富的外业调查经验",
        "attachments": [
          {
            "id": 1,
            "name": "证书.pdf",
            "url": "/uploads/certificates/证书.pdf"
          }
        ],
        "create_time": "2024-01-15T10:30:00Z",
        "update_time": "2024-01-15T10:30:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "pageSize": 10
  }
}

// 2. 创建人员资质
POST /api/personnel-qualifications
请求体：
{
  "task_name": "2024年春季海洋调查",
  "name": "张三",
  "sex": "男",
  "birthdate": "1985-06-15",
  "professional_title": "高级工程师",
  "employer": "海洋研究所",
  "specialty": "海洋地质",
  "instruments": "CTD、多参数水质仪",
  "training": "海洋调查技术培训",
  "remarks": "有丰富的外业调查经验",
  "attachments": [
    {
      "id": 1,
      "name": "证书.pdf",
      "url": "/uploads/certificates/证书.pdf"
    }
  ]
}

// 3. 更新人员资质
PUT /api/personnel-qualifications/{id}
Path参数：id（人员资质记录ID）
请求体：同创建接口

// 4. 删除人员资质
DELETE /api/personnel-qualifications/{id}
Path参数：id（人员资质记录ID）

// 5. 批量删除人员资质
POST /api/personnel-qualifications/batch-delete
请求体：
{
  "ids": [1, 2, 3, 4, 5]  // 要删除的人员资质ID数组
}

// 6. 获取单个人员资质详情
GET /api/personnel-qualifications/{id}
Path参数：id（人员资质记录ID）
```

### 文件操作接口

```javascript
// 7. 下载Excel模板
GET /api/personnel-qualifications/template
响应：Excel文件流

// 8. 导入Excel文件
POST /api/personnel-qualifications/import
Content-Type: multipart/form-data
请求体：FormData，包含file字段（Excel文件）

响应格式：
{
  "code": 200,
  "data": {
    "imported_count": 15,  // 成功导入的记录数
    "failed_count": 2,    // 导入失败的记录数
    "errors": []          // 错误详情（如果有的话）
  }
}

// 9. 导出人员资质数据
GET /api/personnel-qualifications/export
Query参数：（可选，支持筛选条件）
响应：Excel文件流

// 10. 上传附件文件
POST /api/personnel-qualifications/upload
Content-Type: multipart/form-data
请求体：FormData，包含file字段（附件文件）

响应格式：
{
  "code": 200,
  "data": {
    "id": 1,
    "name": "证书.pdf",
    "url": "/uploads/certificates/证书.pdf"
  }
}
```

## 📊 数据表结构建议

后端数据库中建议创建如下表结构：

```sql
CREATE TABLE personnel_qualifications (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    task_name VARCHAR(255) NOT NULL COMMENT '航次任务名称',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    sex VARCHAR(10) NOT NULL COMMENT '性别',
    birthdate DATE NOT NULL COMMENT '出生年月',
    professional_title VARCHAR(100) NOT NULL COMMENT '职称',
    employer VARCHAR(255) NOT NULL COMMENT '工作单位',
    specialty VARCHAR(255) NOT NULL COMMENT '从事专业',
    instruments TEXT COMMENT '本航次操作仪器',
    training TEXT COMMENT '培训情况',
    remarks TEXT COMMENT '备注',
    attachments JSON COMMENT '附件信息（JSON数组）',
    user_id INT COMMENT '创建用户ID（用户隔离）',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT '外业调查人员资质表';
```

## 🔐 权限控制

建议在后端实现用户隔离机制：
- 每个用户只能查看/编辑自己创建的人员资质记录
- 在查询接口中自动过滤 `user_id` 字段
- 支持管理员查看所有记录

## ⚠️ 注意事项

1. **用户隔离**：前端会自动携带 `user_id` 参数，后端需要根据此参数过滤数据
2. **文件上传**：附件上传需要实现文件存储和访问控制
3. **数据验证**：后端需要对所有必填字段进行验证
4. **错误处理**：建议实现统一的错误处理和日志记录
5. **性能优化**：大量数据时需要考虑分页和索引优化

## 🚀 部署说明

1. 确保后端API接口按上述规范实现
2. 配置正确的API基础地址（目前默认为 `http://localhost:5000/api`）
3. 实现文件上传和存储功能
4. 设置适当的CORS策略允许前端访问

按照以上规范实现后端接口，前端页面就可以正常工作了！
