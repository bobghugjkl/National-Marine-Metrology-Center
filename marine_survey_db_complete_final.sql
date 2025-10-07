-- ================================================
-- 海洋调查现场质量监督管理系统 - 完整数据库备份
-- 包含所有表结构和真实数据
-- 数据库名: marine_survey_db
-- 字符集: utf8mb4
-- 生成时间: 2025-10-06
-- ================================================

-- 设置字符集和禁用外键检查
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库
DROP DATABASE IF EXISTS `marine_survey_db`;
CREATE DATABASE `marine_survey_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `marine_survey_db`;

-- ================================================
-- 用户表（完整结构）
-- ================================================
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login_name` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `name` varchar(45) NOT NULL,
  `sex` varchar(45) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  `desc` varchar(45) DEFAULT NULL,
  `permission` varchar(45) DEFAULT NULL,
  `department` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `signature` text,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 插入用户数据
INSERT INTO `tb_user` VALUES 
(1,'test','123456','111',NULL,'111',NULL,NULL,'111',NULL,NULL,NULL,NULL,NULL),
(2,'12','12','12','12','12',NULL,NULL,'12',NULL,NULL,NULL,NULL,NULL),
(3,'123','e10adc3949ba59abbe56e057f20f883e','123','男','普通用户',NULL,NULL,'未分配','2553348955@qq.com','15963300728','data:image/png;base64,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',NULL,NULL),
(4,'admin','123456','admin',NULL,'super_admin',NULL,NULL,'IT_Department',NULL,NULL,NULL,NULL,NULL),
(5,'newuser','123456','newuser',NULL,'普通用户',NULL,NULL,'未分配',NULL,NULL,NULL,NULL,NULL),
(6,'testlogin','123','TestUser',NULL,'user',NULL,NULL,'IT',NULL,NULL,NULL,NULL,NULL),
(7,'娴嬭瘯鐢ㄦ埛','123456','娴嬭瘯鐢ㄦ埛',NULL,'普通用户',NULL,NULL,'未分配',NULL,NULL,NULL,NULL,NULL),
(8,'zhangsan','123456','张三',NULL,'普通用户',NULL,NULL,'业务部门',NULL,NULL,NULL,NULL,NULL),
(9,'lisi','123456','李四',NULL,'普通用户',NULL,NULL,'业务部门',NULL,NULL,NULL,NULL,NULL),
(10,'wangwu','123456','王五',NULL,'部门经理',NULL,NULL,'管理部门',NULL,NULL,NULL,NULL,NULL),
(11,'鐜嬩簲','123456','鐜嬩簲',NULL,'普通用户',NULL,NULL,'未分配',NULL,NULL,NULL,NULL,NULL),
(12,'1234','123456','1234','未知','普通用户','','基础权限','未分配',NULL,NULL,NULL,NULL,NULL),
(13,'12345','123456','12345','未知','普通用户','','基础权限','未分配',NULL,NULL,NULL,NULL,NULL),
(14,'123456','123456','123456','未知','普通用户','','基础权限','未分配',NULL,NULL,NULL,NULL,NULL),
(15,'123556','123456','123556','未知','普通用户','','基础权限','未分配',NULL,NULL,NULL,NULL,NULL),
(16,'1235564533','123456','1235564533','未知','普通用户','','基础权限','未分配',NULL,NULL,NULL,NULL,NULL),
(17,'123666','123456','123666','未知','普通用户','','基础权限','未分配',NULL,NULL,NULL,NULL,NULL);

-- ================================================
-- 其他表结构（从原始备份中提取）
-- ================================================

-- 任务信息表
DROP TABLE IF EXISTS `tb_task_info`;
CREATE TABLE `tb_task_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `project` varchar(100) DEFAULT NULL,
  `task_name` varchar(100) NOT NULL,
  `task_code` varchar(100) DEFAULT NULL,
  `undertake` varchar(100) DEFAULT NULL,
  `participant` varchar(200) DEFAULT NULL,
  `ship` varchar(45) DEFAULT NULL,
  `leader` varchar(45) DEFAULT NULL,
  `chief_scientist` varchar(45) DEFAULT NULL,
  `superintendent` varchar(100) DEFAULT NULL,
  `superintended` varchar(45) DEFAULT NULL,
  `executiontime` text,
  `subject` varchar(45) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_name` (`task_name`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入任务数据
INSERT INTO `tb_task_info` VALUES 
(1,3,'南海海洋调查项目','南海海洋调查任务','HY2024-001','国家海洋局第一海洋研究所','张三,李四,王五','向阳红01号','张三','李四','王五','海洋研究所','2024年3月-5月','海洋科学','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(2,3,'东海海洋调查项目','东海海洋调查','HY2024-002','国家海洋局第二海洋研究所','赵六,钱七,孙八','向阳红02号','赵六','钱七','孙八','东海研究所','2024年4月-6月','海洋地质','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(3,3,'南海深海探测项目','南海深海探测','SD2024-001','中科院深海科学与工程研究所','周九,吴十,郑十一','深海勇士号','周九','吴十','郑十一','深海研究所','2024年5月-7月','深海科学','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(4,1,'测试项目','测试任务','TEST-001','测试单位','测试人员','测试船舶','测试负责人','测试科学家','测试监督员','测试被监督单位','2024年1月-2月','测试学科','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(5,2,'用户2项目','用户2任务','USER2-001','用户2单位','用户2人员','用户2船舶','用户2负责人','用户2科学家','用户2监督员','用户2被监督单位','2024年2月-3月','用户2学科','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(6,3,'2024年夏季海洋环境监测','2024年夏季海洋环境监测','HY2024-002','国家海洋环境监测中心','监测人员A,监测人员B','向阳红02号','监测负责人','环境科学家','环境监督员','环境监测所','2024年6月-8月','环境科学','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(7,3,'2024年秋季深海探测任务','2024年秋季深海探测任务','HY2024-003','国家深海基地管理中心','探测人员A,探测人员B','深海勇士号','探测负责人','深海科学家','深海监督员','深海研究所','2024年9月-11月','深海科学','2025-10-02 16:48:55','2025-10-02 16:48:55');

-- 基础人员主表
DROP TABLE IF EXISTS `tb_base_master`;
CREATE TABLE `tb_base_master` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `sex` varchar(4) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `organization` varchar(45) DEFAULT NULL,
  `major` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `id_card_number` varchar(45) NOT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_card_number` (`id_card_number`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入人员数据
INSERT INTO `tb_base_master` VALUES 
(1,3,'张三','男','1985-03-15','高级工程师','国家海洋局第一海洋研究所','海洋地质','13800138001','110101198503151234','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(2,3,'李四','女','1990-07-22','研究员','中国科学院海洋研究所','海洋生物','13800138002','110101199007221234','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(3,3,'王五','男','1988-11-08','副研究员','国家海洋局第二海洋研究所','海洋化学','13800138003','110101198811081234','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(4,3,'赵六','女','1992-05-12','教授','中国海洋大学','物理海洋','13800138004','110101199205121234','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(5,3,'孙七','男','1987-09-30','工程师','国家深海基地管理中心','深海探测','13800138005','110101198709301234','2025-10-02 16:48:55','2025-10-02 16:48:55'),
(6,1,'测试人员1','男','1990-01-01','工程师','测试单位','测试专业','13800000001','110101199001011111','2025-10-02 16:48:55','2025-10-02 16:48:55');

-- 设备管理表
DROP TABLE IF EXISTS `tb_equipment`;
CREATE TABLE `tb_equipment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '类别',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '仪器（标准物质）名称',
  `number` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '编号',
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '型号',
  `traceability_method` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '量值溯源方式',
  `calibration_date` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '检定/校准日期',
  `certificate_number` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '证书编号',
  `validity_period` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '有效期',
  `calibration_organization` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '检定/校准机构',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件信息（JSON字符串）',
  `user_id` int NOT NULL COMMENT '创建用户ID（用户隔离）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入设备数据
INSERT INTO `tb_equipment` VALUES 
(1,'南海海洋调查任务','仪器','CTD温盐深仪','CTD-001','SBE-911','国家海洋计量站校准','2024-03-15','OM-2024-001','2025-03-15','国家海洋计量站','用于海洋温盐深剖面测量','[]',1,'2025-10-02 16:48:55','2025-10-02 16:48:55'),
(2,'南海海洋调查任务','标准物质','海水盐度标准物质','SS-002','IAPSO标准海水','国际原子能机构溯源','2024-01-10','IAEA-2024-002','2026-01-10','国际原子能机构','用于盐度测量校准','[]',1,'2025-10-02 16:48:55','2025-10-02 16:48:55'),
(3,'东海海洋调查任务','计量器具','数字温度计','DT-003','Fluke-51II','国家计量院校准','2024-02-20','NIM-2024-003','2025-02-20','国家计量院','用于水温测量','[]',1,'2025-10-02 16:48:55','2025-10-02 16:48:55'),
(4,'东海海洋调查','仪器','weqwe','awddaw','awdaw','awdaw','2025-10-01','awdwa','wadaw','dwad','awdaw','[{\"name\": \"2024-08-14_105917.png\", \"url\": \"http://localhost:5000/static/uploads/equipment_attachments/20251003055928_3_2024-08-14_105917.png\", \"uid\": \"20251003055928\"}]',3,'2025-10-02 16:52:30','2025-10-03 05:59:44'),
(5,'东海海洋调查','仪器','wdwa','wdad','awda','伟大阿瓦','','挖的','','','','[{\"name\": \"2024-08-14_105917.png\", \"url\": \"http://localhost:5000/static/uploads/equipment_attachments/20251003064132_3_2024-08-14_105917.png\", \"uid\": \"20251003064132\"}]',3,'2025-10-02 20:05:05','2025-10-03 06:41:35'),
(6,'东海海洋调查','仪器','达瓦','伟大阿瓦','啊伟大伟大','啊伟大伟大','2025-10-02','啊伟大伟大','哇啊挖的','娃娃大','伟大阿瓦达','[{\"name\": \"2024-08-14_105917.png\", \"url\": \"http://localhost:5000/static/uploads/equipment_attachments/20251003064112_3_2024-08-14_105917.png\", \"uid\": \"20251003064112\"}]',3,'2025-10-03 06:41:28','2025-10-03 06:41:28'),
(7,'南海深海探测','仪器','哇大王','伟大挖的','伟大阿瓦达','哇哇','','','','','','[{\"name\": \"2024-08-14_105917.png\", \"url\": \"http://localhost:5000/static/uploads/equipment_attachments/20251003070938_3_2024-08-14_105917.png\", \"uid\": \"20251003070938\"}]',3,'2025-10-03 07:09:39','2025-10-03 07:09:39'),
(8,'南海深海探测','仪器','达瓦','伟大','伟大挖的','','','','','','','[]',3,'2025-10-03 11:02:54','2025-10-03 11:02:54'),
(9,'东海海洋调查','仪器','大王的','啊吴大维','啊我的娃','娃娃大','','','','','','[]',3,'2025-10-03 20:24:13','2025-10-03 20:24:13');

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- ================================================
-- 数据库创建完成
-- ================================================

-- 显示创建结果
SELECT '数据库 marine_survey_db 创建完成！' AS message;
SELECT '包含完整的用户表结构和所有真实数据' AS message;
SELECT '用户表包含14个字段：id, login_name, password, name, sex, role, desc, permission, department, email, phone, signature, create_time, update_time' AS message;
SELECT '包含17个用户记录' AS message;
SELECT '包含7个任务记录' AS message;
SELECT '包含6个人员记录' AS message;
SELECT '包含9个设备记录' AS message;

-- 显示数据统计
SELECT CONCAT('用户表记录数: ', COUNT(*)) AS user_count FROM tb_user;
SELECT CONCAT('任务表记录数: ', COUNT(*)) AS task_count FROM tb_task_info;
SELECT CONCAT('人员表记录数: ', COUNT(*)) AS personnel_count FROM tb_base_master;
SELECT CONCAT('设备表记录数: ', COUNT(*)) AS equipment_count FROM tb_equipment;
