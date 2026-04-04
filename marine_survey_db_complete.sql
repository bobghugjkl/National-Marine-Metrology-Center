-- ================================================
-- 海洋调查现场质量监督管理系统 - 完整数据库
-- 包含所有表结构和测试数据
-- 数据库名: marine_survey_db
-- 字符集: utf8mb4
-- ================================================

-- 设置字符集和禁用外键检查
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库
DROP DATABASE IF EXISTS `marine_survey_db`;
CREATE DATABASE `marine_survey_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `marine_survey_db`;

-- ================================================
-- 核心表结构
-- ================================================

-- 1. 用户表（支持用户隔离）
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `login_name` varchar(45) DEFAULT NULL COMMENT '登录名',
  `password` varchar(45) DEFAULT NULL COMMENT '密码',
  `name` varchar(45) NOT NULL COMMENT '用户名',
  `sex` varchar(45) DEFAULT NULL COMMENT '性别',
  `role` varchar(45) DEFAULT NULL COMMENT '角色',
  `desc` varchar(45) DEFAULT NULL COMMENT '描述',
  `permission` varchar(45) DEFAULT NULL COMMENT '权限',
  `department` varchar(255) NOT NULL COMMENT '部门',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `login_name` (`login_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 2. 任务信息表
DROP TABLE IF EXISTS `tb_task_info`;
CREATE TABLE `tb_task_info` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `project` varchar(100) DEFAULT NULL COMMENT '项目名称',
  `task_name` varchar(100) NOT NULL COMMENT '任务名称',
  `task_code` varchar(100) DEFAULT NULL COMMENT '任务代码',
  `undertake` varchar(100) DEFAULT NULL COMMENT '承担单位',
  `participant` varchar(200) DEFAULT NULL COMMENT '参与人员',
  `ship` varchar(45) DEFAULT NULL COMMENT '船舶',
  `leader` varchar(45) DEFAULT NULL COMMENT '负责人',
  `chief_scientist` varchar(45) DEFAULT NULL COMMENT '首席科学家',
  `superintendent` varchar(100) DEFAULT NULL COMMENT '监督员',
  `superintended` varchar(45) DEFAULT NULL COMMENT '被监督单位',
  `executiontime` text COMMENT '执行时间',
  `subject` varchar(45) DEFAULT NULL COMMENT '学科',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_name` (`task_name`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务信息表';

-- 3. 基础人员主表
DROP TABLE IF EXISTS `tb_base_master`;
CREATE TABLE `tb_base_master` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `name` varchar(40) DEFAULT NULL COMMENT '姓名',
  `sex` varchar(4) DEFAULT NULL COMMENT '性别',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `title` varchar(45) DEFAULT NULL COMMENT '职称',
  `organization` varchar(45) DEFAULT NULL COMMENT '单位',
  `major` varchar(45) DEFAULT NULL COMMENT '专业',
  `phone` varchar(45) DEFAULT NULL COMMENT '电话',
  `id_card_number` varchar(45) NOT NULL COMMENT '身份证号',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_card_number` (`id_card_number`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='基础人员主表';

-- 4. 航前质量监督检查记录表
DROP TABLE IF EXISTS `tb_task_hqzljdjcjlb`;
CREATE TABLE `tb_task_hqzljdjcjlb` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `task_name` varchar(100) NOT NULL COMMENT '任务名称',
  `task_code` varchar(100) DEFAULT NULL COMMENT '任务代码',
  `ship` varchar(100) DEFAULT NULL COMMENT '船舶',
  `executiontime` text COMMENT '执行时间',
  `leader` varchar(45) DEFAULT NULL COMMENT '负责人',
  `chief_scientist` varchar(45) DEFAULT NULL COMMENT '首席科学家',
  `superintendent` varchar(100) DEFAULT NULL COMMENT '监督员',
  `superintended` varchar(45) DEFAULT NULL COMMENT '被监督单位',
  `check_date` date DEFAULT NULL COMMENT '检查日期',
  `check_location` varchar(100) DEFAULT NULL COMMENT '检查地点',
  `check_personnel` varchar(200) DEFAULT NULL COMMENT '检查人员',
  `check_content` text COMMENT '检查内容',
  `check_result` text COMMENT '检查结果',
  `problems` text COMMENT '存在问题',
  `suggestions` text COMMENT '建议措施',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_name` (`task_name`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航前质量监督检查记录表';

-- 5. 航前调查人员表
DROP TABLE IF EXISTS `tb_base_hq_investigator`;
CREATE TABLE `tb_base_hq_investigator` (
  `uniqueid` varchar(100) NOT NULL COMMENT '唯一ID',
  `task_name` varchar(100) DEFAULT NULL COMMENT '任务名称',
  `task_code` varchar(100) DEFAULT NULL COMMENT '任务代码',
  `ship` varchar(100) DEFAULT NULL COMMENT '船舶',
  `name` varchar(40) DEFAULT NULL COMMENT '姓名',
  `sex` varchar(4) DEFAULT NULL COMMENT '性别',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `title` varchar(40) DEFAULT NULL COMMENT '职称',
  `organization` varchar(45) DEFAULT NULL COMMENT '单位',
  `major` varchar(45) DEFAULT NULL COMMENT '专业',
  `instrument` varchar(45) DEFAULT NULL COMMENT '仪器',
  `trainingdate` varchar(45) DEFAULT NULL COMMENT '培训日期',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `preparer` varchar(45) DEFAULT NULL COMMENT '编制人',
  `verifier` varchar(45) DEFAULT NULL COMMENT '审核人',
  `create_date` date DEFAULT NULL COMMENT '创建日期',
  `attachment` text COMMENT '附件',
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航前调查人员表';

-- 6. 航前设备表
DROP TABLE IF EXISTS `tb_base_hq_device`;
CREATE TABLE `tb_base_hq_device` (
  `uniqueid` varchar(100) NOT NULL COMMENT '唯一ID',
  `task_name` varchar(100) NOT NULL COMMENT '任务名称',
  `type` varchar(45) DEFAULT NULL COMMENT '类型',
  `name` varchar(100) DEFAULT NULL COMMENT '设备名称',
  `id` varchar(45) DEFAULT NULL COMMENT '设备ID',
  `model` varchar(45) DEFAULT NULL COMMENT '型号',
  `traceability` varchar(45) DEFAULT NULL COMMENT '可追溯性',
  `checkdate` date DEFAULT NULL COMMENT '检查日期',
  `certificate_number` varchar(45) DEFAULT NULL COMMENT '证书编号',
  `validity` varchar(45) DEFAULT NULL COMMENT '有效期',
  `verification_institutions` varchar(45) DEFAULT NULL COMMENT '检定机构',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `attachment` text COMMENT '附件',
  `preparer` varchar(45) DEFAULT NULL COMMENT '编制人',
  `verifier` varchar(45) DEFAULT NULL COMMENT '审核人',
  `create_date` date DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航前设备表';

-- 7. 航中调查人员表
DROP TABLE IF EXISTS `tb_base_hz_investigator`;
CREATE TABLE `tb_base_hz_investigator` (
  `uniqueid` varchar(100) NOT NULL COMMENT '唯一ID',
  `task_name` varchar(100) DEFAULT NULL COMMENT '任务名称',
  `task_code` varchar(100) DEFAULT NULL COMMENT '任务代码',
  `ship` varchar(100) DEFAULT NULL COMMENT '船舶',
  `name` varchar(40) DEFAULT NULL COMMENT '姓名',
  `sex` varchar(4) DEFAULT NULL COMMENT '性别',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `title` varchar(40) DEFAULT NULL COMMENT '职称',
  `organization` varchar(45) DEFAULT NULL COMMENT '单位',
  `major` varchar(45) DEFAULT NULL COMMENT '专业',
  `instrument` varchar(45) DEFAULT NULL COMMENT '仪器',
  `trainingdate` varchar(45) DEFAULT NULL COMMENT '培训日期',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `preparer` varchar(45) DEFAULT NULL COMMENT '编制人',
  `verifier` varchar(45) DEFAULT NULL COMMENT '审核人',
  `create_date` date DEFAULT NULL COMMENT '创建日期',
  `attachment` text COMMENT '附件',
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航中调查人员表';

-- 8. 航中设备表
DROP TABLE IF EXISTS `tb_base_hz_device`;
CREATE TABLE `tb_base_hz_device` (
  `uniqueid` varchar(100) NOT NULL COMMENT '唯一ID',
  `task_name` varchar(100) NOT NULL COMMENT '任务名称',
  `type` varchar(45) DEFAULT NULL COMMENT '类型',
  `name` varchar(100) DEFAULT NULL COMMENT '设备名称',
  `id` varchar(45) DEFAULT NULL COMMENT '设备ID',
  `model` varchar(45) DEFAULT NULL COMMENT '型号',
  `traceability` varchar(45) DEFAULT NULL COMMENT '可追溯性',
  `checkdate` date DEFAULT NULL COMMENT '检查日期',
  `certificate_number` varchar(45) DEFAULT NULL COMMENT '证书编号',
  `validity` varchar(45) DEFAULT NULL COMMENT '有效期',
  `verification_institutions` varchar(45) DEFAULT NULL COMMENT '检定机构',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `attachment` text COMMENT '附件',
  `preparer` varchar(45) DEFAULT NULL COMMENT '编制人',
  `verifier` varchar(45) DEFAULT NULL COMMENT '审核人',
  `create_date` date DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航中设备表';

-- 9. 生产质量监督检查表
DROP TABLE IF EXISTS `tb_task_sczljdjcb`;
CREATE TABLE `tb_task_sczljdjcb` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `task_name` varchar(100) NOT NULL COMMENT '任务名称',
  `check_date` date DEFAULT NULL COMMENT '检查日期',
  `check_personnel` varchar(200) DEFAULT NULL COMMENT '检查人员',
  `check_content` text COMMENT '检查内容',
  `check_result` text COMMENT '检查结果',
  `problems` text COMMENT '存在问题',
  `suggestions` text COMMENT '建议措施',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_name` (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='生产质量监督检查表';

-- 10. 质量评估表
DROP TABLE IF EXISTS `tb_task_zlpgb`;
CREATE TABLE `tb_task_zlpgb` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `task_name` varchar(100) NOT NULL COMMENT '任务名称',
  `evaluation_date` date DEFAULT NULL COMMENT '评估日期',
  `evaluator` varchar(100) DEFAULT NULL COMMENT '评估人',
  `evaluation_content` text COMMENT '评估内容',
  `evaluation_result` text COMMENT '评估结果',
  `score` int DEFAULT NULL COMMENT '评分',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_name` (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='质量评估表';

-- ================================================
-- 扩展表结构
-- ================================================

-- 11. 设备管理表
DROP TABLE IF EXISTS `tb_equipment`;
CREATE TABLE `tb_equipment` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `equipment_name` varchar(100) NOT NULL COMMENT '设备名称',
  `equipment_type` varchar(50) DEFAULT NULL COMMENT '设备类型',
  `model` varchar(50) DEFAULT NULL COMMENT '型号',
  `serial_number` varchar(100) DEFAULT NULL COMMENT '序列号',
  `manufacturer` varchar(100) DEFAULT NULL COMMENT '制造商',
  `purchase_date` date DEFAULT NULL COMMENT '采购日期',
  `status` varchar(20) DEFAULT '正常' COMMENT '状态',
  `location` varchar(100) DEFAULT NULL COMMENT '位置',
  `remark` text COMMENT '备注',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='设备管理表';

-- 12. 人员资质表
DROP TABLE IF EXISTS `tb_personnel_qualifications`;
CREATE TABLE `tb_personnel_qualifications` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `person_name` varchar(50) NOT NULL COMMENT '人员姓名',
  `qualification_type` varchar(50) DEFAULT NULL COMMENT '资质类型',
  `certificate_number` varchar(100) DEFAULT NULL COMMENT '证书编号',
  `issue_date` date DEFAULT NULL COMMENT '发证日期',
  `expiry_date` date DEFAULT NULL COMMENT '到期日期',
  `issuing_authority` varchar(100) DEFAULT NULL COMMENT '发证机关',
  `status` varchar(20) DEFAULT '有效' COMMENT '状态',
  `remark` text COMMENT '备注',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人员资质表';

-- 13. 调查项目表
DROP TABLE IF EXISTS `tb_investigation_projects`;
CREATE TABLE `tb_investigation_projects` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `project_name` varchar(100) NOT NULL COMMENT '项目名称',
  `project_code` varchar(50) DEFAULT NULL COMMENT '项目代码',
  `project_type` varchar(50) DEFAULT NULL COMMENT '项目类型',
  `start_date` date DEFAULT NULL COMMENT '开始日期',
  `end_date` date DEFAULT NULL COMMENT '结束日期',
  `status` varchar(20) DEFAULT '进行中' COMMENT '状态',
  `description` text COMMENT '项目描述',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='调查项目表';

-- 14. 工作日志表
DROP TABLE IF EXISTS `tb_work_log`;
CREATE TABLE `tb_work_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `log_date` date NOT NULL COMMENT '日志日期',
  `work_content` text COMMENT '工作内容',
  `work_hours` decimal(4,2) DEFAULT NULL COMMENT '工作时长',
  `weather` varchar(50) DEFAULT NULL COMMENT '天气',
  `location` varchar(100) DEFAULT NULL COMMENT '工作地点',
  `participants` varchar(200) DEFAULT NULL COMMENT '参与人员',
  `remark` text COMMENT '备注',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作日志表';

-- 15. 监督日志表
DROP TABLE IF EXISTS `tb_supervisor_log`;
CREATE TABLE `tb_supervisor_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int DEFAULT NULL COMMENT '用户ID（用户隔离）',
  `log_date` date NOT NULL COMMENT '日志日期',
  `supervisor_name` varchar(50) DEFAULT NULL COMMENT '监督员姓名',
  `supervised_unit` varchar(100) DEFAULT NULL COMMENT '被监督单位',
  `supervision_content` text COMMENT '监督内容',
  `supervision_result` text COMMENT '监督结果',
  `problems_found` text COMMENT '发现的问题',
  `suggestions` text COMMENT '建议',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='监督日志表';

-- ================================================
-- 测试数据
-- ================================================

-- 插入测试用户数据
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES
(1, 'test', '123456', '111', '男', '测试用户', '测试用户账号', 'user', '测试部门'),
(2, '12', '12', '12', '男', '普通用户', '普通用户账号', 'user', '普通部门'),
(3, '123', '123456', '123', '男', '普通用户', '普通用户账号', 'user', '普通部门'),
(4, 'admin', '123456', 'admin', '男', '超级管理员', '系统管理员', 'admin', '管理部门');

-- 插入测试任务数据
INSERT INTO `tb_task_info` (`id`, `user_id`, `project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`) VALUES
(1, 3, '海洋环境调查项目', '2024年春季海洋调查任务', 'HY2024-001', '国家海洋局', '张三,李四,王五', '海洋一号', '张三', '李四', '王五', '海洋研究所', '2024年3月-5月', '海洋科学'),
(2, 3, '深海资源勘探项目', '2024年深海勘探任务', 'SD2024-001', '中科院海洋所', '赵六,钱七,孙八', '深海一号', '赵六', '钱七', '孙八', '深海研究所', '2024年4月-6月', '海洋地质'),
(3, 3, '海洋生态监测项目', '2024年生态监测任务', 'ST2024-001', '环保部', '周九,吴十,郑十一', '生态监测船', '周九', '吴十', '郑十一', '生态研究所', '2024年5月-7月', '海洋生态'),
(4, 1, '测试项目', '测试任务', 'TEST-001', '测试单位', '测试人员', '测试船舶', '测试负责人', '测试科学家', '测试监督员', '测试被监督单位', '2024年1月-2月', '测试学科'),
(5, 2, '用户2项目', '用户2任务', 'USER2-001', '用户2单位', '用户2人员', '用户2船舶', '用户2负责人', '用户2科学家', '用户2监督员', '用户2被监督单位', '2024年2月-3月', '用户2学科');

-- 插入测试人员数据
INSERT INTO `tb_base_master` (`id`, `user_id`, `name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`) VALUES
(1, 3, '张三', '男', '1980-01-01', '高级工程师', '国家海洋局', '海洋科学', '13800138001', '110101198001011234'),
(2, 3, '李四', '女', '1985-05-15', '研究员', '中科院海洋所', '海洋生物', '13800138002', '110101198505151234'),
(3, 3, '王五', '男', '1990-10-20', '工程师', '海洋研究所', '海洋化学', '13800138003', '110101199010201234'),
(4, 1, '测试人员1', '男', '1990-01-01', '工程师', '测试单位', '测试专业', '13800000001', '110101199001011111'),
(5, 2, '用户2人员1', '女', '1985-01-01', '高级工程师', '用户2单位', '用户2专业', '13800000002', '110101198501011111');

-- 插入测试检查记录数据
INSERT INTO `tb_task_hqzljdjcjlb` (`id`, `user_id`, `task_name`, `task_code`, `ship`, `executiontime`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `check_date`, `check_location`, `check_personnel`, `check_content`, `check_result`, `problems`, `suggestions`) VALUES
(1, 3, '2024年春季海洋调查任务', 'HY2024-001', '海洋一号', '2024年3月-5月', '张三', '李四', '王五', '海洋研究所', '2024-03-01', '青岛港', '张三,李四,王五', '航前质量检查', '检查合格', '无', '继续保持'),
(2, 3, '2024年深海勘探任务', 'SD2024-001', '深海一号', '2024年4月-6月', '赵六', '钱七', '孙八', '深海研究所', '2024-04-01', '上海港', '赵六,钱七,孙八', '航前质量检查', '检查合格', '无', '继续保持'),
(3, 3, '2024年生态监测任务', 'ST2024-001', '生态监测船', '2024年5月-7月', '周九', '吴十', '郑十一', '生态研究所', '2024-05-01', '大连港', '周九,吴十,郑十一', '航前质量检查', '检查合格', '无', '继续保持'),
(4, 1, '测试任务', 'TEST-001', '测试船舶', '2024年1月-2月', '测试负责人', '测试科学家', '测试监督员', '测试被监督单位', '2024-01-01', '测试地点', '测试人员', '测试检查内容', '测试结果', '无', '测试建议'),
(5, 2, '用户2任务', 'USER2-001', '用户2船舶', '2024年2月-3月', '用户2负责人', '用户2科学家', '用户2监督员', '用户2被监督单位', '2024-02-01', '用户2地点', '用户2人员', '用户2检查内容', '用户2结果', '无', '用户2建议');

-- 插入测试设备数据
INSERT INTO `tb_equipment` (`id`, `user_id`, `equipment_name`, `equipment_type`, `model`, `serial_number`, `manufacturer`, `purchase_date`, `status`, `location`, `remark`) VALUES
(1, 3, 'CTD温盐深仪', '海洋仪器', 'SBE911Plus', 'SBE911-001', 'Sea-Bird', '2023-01-01', '正常', '实验室A', '高精度温盐深测量设备'),
(2, 3, '多波束测深仪', '海洋仪器', 'EM2040', 'EM2040-001', 'Kongsberg', '2023-02-01', '正常', '实验室B', '高分辨率海底地形测量设备'),
(3, 3, 'ADCP流速仪', '海洋仪器', 'Workhorse', 'ADCP-001', 'Teledyne', '2023-03-01', '正常', '实验室C', '声学多普勒流速剖面仪'),
(4, 1, '测试设备1', '测试类型', 'TEST-MODEL', 'TEST-001', '测试制造商', '2023-01-01', '正常', '测试位置', '测试设备'),
(5, 2, '用户2设备1', '用户2类型', 'USER2-MODEL', 'USER2-001', '用户2制造商', '2023-01-01', '正常', '用户2位置', '用户2设备');

-- 插入测试人员资质数据
INSERT INTO `tb_personnel_qualifications` (`id`, `user_id`, `person_name`, `qualification_type`, `certificate_number`, `issue_date`, `expiry_date`, `issuing_authority`, `status`, `remark`) VALUES
(1, 3, '张三', '海洋调查员证书', 'HY2023001', '2023-01-01', '2025-01-01', '国家海洋局', '有效', '海洋调查专业资质'),
(2, 3, '李四', '海洋生物研究员证书', 'HY2023002', '2023-02-01', '2025-02-01', '中科院', '有效', '海洋生物研究资质'),
(3, 3, '王五', '海洋化学工程师证书', 'HY2023003', '2023-03-01', '2025-03-01', '海洋研究所', '有效', '海洋化学工程资质'),
(4, 1, '测试人员1', '测试资质', 'TEST-001', '2023-01-01', '2025-01-01', '测试机构', '有效', '测试资质'),
(5, 2, '用户2人员1', '用户2资质', 'USER2-001', '2023-01-01', '2025-01-01', '用户2机构', '有效', '用户2资质');

-- 插入测试调查项目数据
INSERT INTO `tb_investigation_projects` (`id`, `user_id`, `project_name`, `project_code`, `project_type`, `start_date`, `end_date`, `status`, `description`) VALUES
(1, 3, '2024年春季海洋环境调查', 'HY2024-ENV', '环境调查', '2024-03-01', '2024-05-31', '进行中', '春季海洋环境综合调查项目'),
(2, 3, '2024年深海资源勘探', 'SD2024-RES', '资源勘探', '2024-04-01', '2024-06-30', '进行中', '深海矿产资源勘探项目'),
(3, 3, '2024年海洋生态监测', 'ST2024-ECO', '生态监测', '2024-05-01', '2024-07-31', '进行中', '海洋生态系统监测项目'),
(4, 1, '测试项目', 'TEST-PROJ', '测试类型', '2024-01-01', '2024-02-28', '已完成', '测试项目描述'),
(5, 2, '用户2项目', 'USER2-PROJ', '用户2类型', '2024-02-01', '2024-03-31', '进行中', '用户2项目描述');

-- 插入测试工作日志数据
INSERT INTO `tb_work_log` (`id`, `user_id`, `log_date`, `work_content`, `work_hours`, `weather`, `location`, `participants`, `remark`) VALUES
(1, 3, '2024-03-01', '进行航前设备检查', 8.0, '晴', '青岛港', '张三,李四,王五', '设备检查完成'),
(2, 3, '2024-03-02', '进行人员培训', 6.0, '晴', '实验室', '张三,李四,王五', '培训效果良好'),
(3, 3, '2024-03-03', '进行安全检查', 4.0, '多云', '船舶', '张三,李四,王五', '安全检查通过'),
(4, 1, '2024-01-01', '测试工作内容', 8.0, '晴', '测试地点', '测试人员', '测试工作日志'),
(5, 2, '2024-02-01', '用户2工作内容', 8.0, '晴', '用户2地点', '用户2人员', '用户2工作日志');

-- 插入测试监督日志数据
INSERT INTO `tb_supervisor_log` (`id`, `user_id`, `log_date`, `supervisor_name`, `supervised_unit`, `supervision_content`, `supervision_result`, `problems_found`, `suggestions`) VALUES
(1, 3, '2024-03-01', '王五', '海洋研究所', '航前质量监督检查', '检查合格', '无', '继续保持'),
(2, 3, '2024-04-01', '孙八', '深海研究所', '深海勘探质量监督', '检查合格', '无', '继续保持'),
(3, 3, '2024-05-01', '郑十一', '生态研究所', '生态监测质量监督', '检查合格', '无', '继续保持'),
(4, 1, '2024-01-01', '测试监督员', '测试被监督单位', '测试监督内容', '测试结果', '无', '测试建议'),
(5, 2, '2024-02-01', '用户2监督员', '用户2被监督单位', '用户2监督内容', '用户2结果', '无', '用户2建议');

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- ================================================
-- 数据库创建完成
-- ================================================

-- 显示创建结果
SELECT '数据库 marine_survey_db 创建完成！' AS message;
SELECT '包含以下核心表：' AS message;
SELECT '1. tb_user - 用户表（支持用户隔离）' AS message;
SELECT '2. tb_task_info - 任务信息表' AS message;
SELECT '3. tb_base_master - 基础人员主表' AS message;
SELECT '4. tb_task_hqzljdjcjlb - 航前质量监督检查记录表' AS message;
SELECT '5. tb_equipment - 设备管理表' AS message;
SELECT '6. tb_personnel_qualifications - 人员资质表' AS message;
SELECT '7. tb_investigation_projects - 调查项目表' AS message;
SELECT '8. tb_work_log - 工作日志表' AS message;
SELECT '9. tb_supervisor_log - 监督日志表' AS message;
SELECT '以及其他扩展表...' AS message;

-- 显示测试数据统计
SELECT CONCAT('用户表记录数: ', COUNT(*)) AS user_count FROM tb_user;
SELECT CONCAT('任务表记录数: ', COUNT(*)) AS task_count FROM tb_task_info;
SELECT CONCAT('人员表记录数: ', COUNT(*)) AS personnel_count FROM tb_base_master;
SELECT CONCAT('设备表记录数: ', COUNT(*)) AS equipment_count FROM tb_equipment;
