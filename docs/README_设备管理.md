# 🛠️ 外业设备（工作计量器具）管理前端页面使用说明

## 📋 功能概述

本页面实现了外业设备（工作计量器具）一览表的前端展示和管理功能，包括：

- 📊 设备列表展示（带分页和有效期状态）
- ➕ 新增设备记录
- ✏️ 编辑已有设备信息
- 🔍 按条件搜索设备
- 🗑️ 删除和批量删除功能
- 📥 Excel模板下载和文件导入
- 📎 附件上传和管理
- 👁️ 设备详情查看

## 🖥️ 界面预览

页面布局包含：
- **顶部标题栏**：显示"仪器设备（工作计量器具）一览表"，右侧放置操作按钮
- **搜索区域**：支持按航次任务、仪器名称、类别、检定机构筛选
- **数据表格**：展示设备信息，支持排序、分页等操作，有效期状态颜色提示
- **弹窗表单**：新增/编辑设备信息的表单

## 🎨 特色功能

### 📅 有效期状态显示
- 🟢 **有效**：距离到期超过30天
- 🟡 **即将过期**：距离到期30天以内
- 🔴 **已过期**：已超过有效期

### 📋 表格列说明
| 列名 | 说明 | 特殊功能 |
|------|------|----------|
| 航次任务名称 | 所属海洋调查任务 | - |
| 类别 | 设备分类标签 | 彩色标签显示 |
| 仪器（标准物质）名称 | 设备或标准物质名称 | - |
| 编号 | 设备唯一编号 | - |
| 型号 | 设备型号规格 | - |
| 量程/测量方式 | 测量范围或方式 | - |
| 检定/校准日期 | 上次检定日期 | - |
| 证书编号 | 检定证书编号 | 等宽字体显示 |
| 有效期 | 证书有效期 | 状态颜色提示 |
| 检定/校准机构 | 检定单位名称 | - |
| 备注 | 附加说明信息 | - |
| 附件 | 相关文档 | 点击查看/下载 |

## 🔌 后端API接口要求

为了让前端页面正常工作，后端需要实现以下RESTful API接口：

### 基础CRUD接口

```javascript
// 1. 获取设备列表（支持分页和搜索）
GET /api/equipment
Query参数：
- page: 页码 (默认1)
- pageSize: 每页数量 (默认10)
- task_name: 航次任务名称（可选）
- equipment_name: 仪器名称（可选）
- category: 类别（可选）
- calibration_organization: 检定机构（可选）

响应格式：
{
  "code": 200,
  "data": {
    "list": [
      {
        "id": 1,
        "task_name": "2024年春季海洋调查",
        "category": "测量仪器",
        "equipment_name": "CTD温盐深仪",
        "serial_number": "CTD-2024-001",
        "model": "SBE-911",
        "measurement_range": "温度：-5~35℃，盐度：0~70PSU",
        "calibration_date": "2024-01-15",
        "certificate_number": "JJG-2024-001",
        "validity_period": "2025-01-14",
        "calibration_organization": "国家海洋计量站",
        "remarks": "使用前需预热30分钟",
        "attachments": [
          {
            "id": 1,
            "name": "检定证书.pdf",
            "url": "/uploads/certificates/检定证书.pdf"
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

// 2. 创建设备记录
POST /api/equipment
请求体：
{
  "task_name": "2024年春季海洋调查",
  "category": "测量仪器",
  "equipment_name": "CTD温盐深仪",
  "serial_number": "CTD-2024-001",
  "model": "SBE-911",
  "measurement_range": "温度：-5~35℃，盐度：0~70PSU",
  "calibration_date": "2024-01-15",
  "certificate_number": "JJG-2024-001",
  "validity_period": "2025-01-14",
  "calibration_organization": "国家海洋计量站",
  "remarks": "使用前需预热30分钟",
  "attachments": [
    {
      "id": 1,
      "name": "检定证书.pdf",
      "url": "/uploads/certificates/检定证书.pdf"
    }
  ]
}

// 3. 更新设备记录
PUT /api/equipment/{id}
Path参数：id（设备记录ID）
请求体：同创建接口

// 4. 删除设备记录
DELETE /api/equipment/{id}
Path参数：id（设备记录ID）

// 5. 批量删除设备记录
POST /api/equipment/batch-delete
请求体：
{
  "ids": [1, 2, 3, 4, 5]  // 要删除的设备ID数组
}

// 6. 获取单个设备详情
GET /api/equipment/{id}
Path参数：id（设备记录ID）
```

### 文件操作接口

```javascript
// 7. 下载Excel模板
GET /api/equipment/template
响应：Excel文件流

// 8. 导入Excel文件
POST /api/equipment/import
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

// 9. 导出设备数据
GET /api/equipment/export
Query参数：（可选，支持筛选条件）
响应：Excel文件流

// 10. 上传附件文件
POST /api/equipment/upload
Content-Type: multipart/form-data
请求体：FormData，包含file字段（附件文件）

响应格式：
{
  "code": 200,
  "data": {
    "id": 1,
    "name": "检定证书.pdf",
    "url": "/uploads/certificates/检定证书.pdf"
  }
}

// 11. 获取设备类别选项（可选）
GET /api/equipment/categories
响应：
{
  "code": 200,
  "data": [
    "测量仪器",
    "标准物质",
    "辅助设备",
    "其他"
  ]
}

// 12. 获取检定机构选项（可选）
GET /api/equipment/organizations
响应：
{
  "code": 200,
  "data": [
    "国家海洋计量站",
    "中国计量科学研究院",
    "地方计量检定机构"
  ]
}
```

## 📊 数据表结构建议

后端数据库中建议创建如下表结构：

```sql
CREATE TABLE equipment (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    task_name VARCHAR(255) NOT NULL COMMENT '航次任务名称',
    category VARCHAR(50) NOT NULL COMMENT '设备类别',
    equipment_name VARCHAR(255) NOT NULL COMMENT '仪器（标准物质）名称',
    serial_number VARCHAR(100) NOT NULL COMMENT '编号',
    model VARCHAR(100) NOT NULL COMMENT '型号',
    measurement_range TEXT COMMENT '量程/测量方式',
    calibration_date DATE COMMENT '检定/校准日期',
    certificate_number VARCHAR(100) COMMENT '证书编号',
    validity_period DATE COMMENT '有效期',
    calibration_organization VARCHAR(255) COMMENT '检定/校准机构',
    remarks TEXT COMMENT '备注',
    attachments JSON COMMENT '附件信息（JSON数组）',
    user_id INT COMMENT '创建用户ID（用户隔离）',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_task_name (task_name),
    INDEX idx_equipment_name (equipment_name),
    INDEX idx_validity_period (validity_period)
) COMMENT '外业设备（工作计量器具）表';
```

## 🔐 权限控制

建议在后端实现用户隔离机制：
- 每个用户只能查看/编辑自己创建的设备记录
- 在查询接口中自动过滤 `user_id` 字段
- 支持管理员查看所有记录

## ⚠️ 注意事项

1. **用户隔离**：前端会自动携带 `user_id` 参数，后端需要根据此参数过滤数据
2. **文件上传**：附件上传需要实现文件存储和访问控制
3. **数据验证**：后端需要对所有必填字段进行验证
4. **有效期监控**：可以考虑定时任务提醒即将到期的设备
5. **错误处理**：建议实现统一的错误处理和日志记录
6. **性能优化**：大量数据时需要考虑分页和索引优化

## 🚀 部署说明

1. 确保后端API接口按上述规范实现
2. 配置正确的API基础地址（目前默认为 `http://localhost:5000/api`）
3. 实现文件上传和存储功能
4. 设置适当的CORS策略允许前端访问
5. 考虑添加设备有效期提醒功能

## 📈 扩展建议

1. **设备状态管理**：增加设备状态字段（正常/维修/报废）
2. **使用记录**：记录设备的每次使用情况
3. **保养提醒**：定期保养提醒功能
4. **设备轨迹**：记录设备的位置和移动轨迹
5. **批量操作**：支持批量导入/导出/更新

按照以上规范实现后端接口，前端页面就可以正常工作了！
