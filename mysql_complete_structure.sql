-- ================================================
-- 海洋调查现场质量监督管理系统 - 一键完整数据库创建脚本
-- 生成时间: 2025-01-01
--
-- 【重要】一键运行说明：
-- 1. 在MySQL命令行中执行：source mysql_complete_structure.sql
-- 2. 或命令行执行：mysql -u root -p < mysql_complete_structure.sql
-- 3. 执行完成后会自动创建数据库、所有表和测试数据
--
-- 包含功能：
-- ✅ 数据库自动创建 (marine_survey_db)
-- ✅ 13个数据表完整结构
-- ✅ 丰富的测试数据（用户、任务、设备、人员等）
-- ✅ UTF8MB4字符集支持（完美支持中文）
-- ✅ 索引优化（提高查询性能）
-- ✅ 用户隔离字段（支持多用户系统）
-- ================================================

-- 删除数据库（如果存在）
DROP DATABASE IF EXISTS marine_survey_db;

-- 创建数据库
CREATE DATABASE marine_survey_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE marine_survey_db;

-- 设置字符集和外键检查
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ================================================
-- 删除现有表 (如果存在)
-- ================================================
DROP TABLE IF EXISTS `tb_user`;
DROP TABLE IF EXISTS `tb_task_info`;
DROP TABLE IF EXISTS `tb_task_hqzljdjcjlb`;
DROP TABLE IF EXISTS `tb_task_sczljdjcb`;
DROP TABLE IF EXISTS `tb_task_zlpgb`;
DROP TABLE IF EXISTS `tb_base_master`;
DROP TABLE IF EXISTS `tb_base_hq_investigator`;
DROP TABLE IF EXISTS `tb_base_hq_device`;
DROP TABLE IF EXISTS `tb_base_hz_investigator`;
DROP TABLE IF EXISTS `tb_base_hz_device`;

-- ================================================
-- 用户表 (tb_user)
-- ================================================
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
  PRIMARY KEY (`name`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 插入测试用户数据
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES
(1, 'test', '123456', '测试用户', '男', '普通用户', '测试账号', 'read', '技术部门'),
(2, '12', '12', '12', '男', '普通用户', '测试账号', 'read', '技术部门'),
(3, '123', '123456', '123', '男', '普通用户', '测试账号', 'read', '技术部门'),
(4, 'admin', '123456', '管理员', '男', '超级管理员', '系统管理员', 'admin', '管理部门'),
(5, 'newuser', '123456', '新用户', '女', '普通用户', '新员工', 'read', '业务部门'),
(6, 'testlogin', '123', '测试用户2', '男', '普通用户', '测试账号', 'read', '技术部门');

-- ================================================
-- 任务信息表 (tb_task_info)
-- ================================================
CREATE TABLE `tb_task_info` (
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
  PRIMARY KEY (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务信息表';

-- 插入测试任务数据
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`) VALUES
('海洋调查项目', '2024年春季海洋调查', 'HY-2024-001', '海洋研究所', '张三,李四,王五', '海洋号', '张三', '李四', '王五', '赵六', '2024年3月-6月', '海洋环境监测'),
('海洋调查项目', '2024年夏季海洋调查', 'HY-2024-002', '海洋研究所', '李四,赵六', '海洋号', '李四', '赵六', '王五', '赵六', '2024年7月-9月', '海洋生态调查'),
('海洋调查项目', '2024年秋季海洋调查', 'HY-2024-003', '海洋研究所', '王五,张三', '海洋号', '王五', '张三', '李四', '赵六', '2024年10月-12月', '海洋地质调查');

-- ================================================
-- 航前质量监督检查记录表 (tb_task_hqzljdjcjlb)
-- ================================================
CREATE TABLE `tb_task_hqzljdjcjlb` (
  `uniqueid` varchar(100) NOT NULL,
  `task_name` varchar(100) NOT NULL,
  `item1` text,
  `item2` text,
  `item3` text,
  `item4` text,
  `item5` text,
  `item6` text,
  `item7` text,
  `item8` text,
  `item9` text,
  `item10` text,
  `item11` text,
  `check_date` date DEFAULT NULL,
  `checker` varchar(45) DEFAULT NULL,
  `remark` text,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航前质量监督检查记录表';

-- 插入测试检查数据
INSERT INTO `tb_task_hqzljdjcjlb` (`uniqueid`, `task_name`, `item1`, `item2`, `item3`, `item4`, `item5`, `item6`, `item7`, `item8`, `item9`, `item10`, `item11`, `check_date`, `checker`, `remark`) VALUES
('check_001', '2024年春季海洋调查', '检查项目1正常', '检查项目2正常', '检查项目3正常', '检查项目4正常', '检查项目5正常', '检查项目6正常', '检查项目7正常', '检查项目8正常', '检查项目9正常', '检查项目10正常', '检查项目11正常', '2024-03-01', '张三', '所有项目检查正常，可以执行任务'),
('check_002', '2024年夏季海洋调查', '检查项目1正常', '检查项目2正常', '检查项目3正常', '检查项目4正常', '检查项目5正常', '检查项目6正常', '检查项目7正常', '检查项目8正常', '检查项目9正常', '检查项目10正常', '检查项目11正常', '2024-07-01', '李四', '设备状态良好，人员准备充分');

-- ================================================
-- 生产质量监督检查表 (tb_task_sczljdjcb)
-- ================================================
CREATE TABLE `tb_task_sczljdjcb` (
  `uniqueid` varchar(100) NOT NULL,
  `task_name` varchar(100) DEFAULT NULL,
  `item1` text,
  `item2` text,
  `item3` text,
  `item4` text,
  `item5` text,
  `item6` text,
  `item7` text,
  `item8` text,
  `item9` text,
  `item10` text,
  `item11` text,
  `item12` text,
  `item13` text,
  `item14` text,
  `item15` text,
  `item16` text,
  `item17` text,
  `item18` text,
  `item19` text,
  `item20` text,
  `item21` text,
  `item22` text,
  `item23` text,
  `item24` text,
  `item25` text,
  `item26` text,
  `item27` text,
  `item28` text,
  `item29` text,
  `item30` text,
  `item31` text,
  `item32` text,
  `item33` text,
  `item34` text,
  `item35` text,
  `item36` text,
  `item37` text,
  `item38` text,
  `item39` text,
  `item40` text,
  `item41` text,
  `item42` text,
  `item43` text,
  `item44` text,
  `item45` text,
  `item46` text,
  `item47` text,
  `item48` text,
  `item49` text,
  `item50` text,
  `check_date` date DEFAULT NULL,
  `checker` varchar(45) DEFAULT NULL,
  `remark` text,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='生产质量监督检查表';

-- ================================================
-- 质量评估表 (tb_task_zlpgb)
-- ================================================
CREATE TABLE `tb_task_zlpgb` (
  `uniqueid` varchar(100) NOT NULL,
  `task_name` varchar(100) DEFAULT NULL,
  `item1` text,
  `item2` text,
  `item3` text,
  `item4` text,
  `item5` text,
  `item6` text,
  `item7` text,
  `item8` text,
  `item9` text,
  `item10` text,
  `item11` text,
  `item12` text,
  `item13` text,
  `item14` text,
  `item15` text,
  `item16` text,
  `item17` text,
  `item18` text,
  `item19` text,
  `item20` text,
  `check_date` date DEFAULT NULL,
  `checker` varchar(45) DEFAULT NULL,
  `remark` text,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='质量评估表';

-- ================================================
-- 基础人员主表 (tb_base_master)
-- ================================================
CREATE TABLE `tb_base_master` (
  `name` varchar(40) DEFAULT NULL,
  `sex` varchar(4) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `organization` varchar(45) DEFAULT NULL,
  `major` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `id_card_number` varchar(45) NOT NULL,
  `education` varchar(45) DEFAULT NULL,
  `degree` varchar(45) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_card_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='基础人员信息主表';

-- 插入测试人员数据
INSERT INTO `tb_base_master` (`name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`, `education`, `degree`, `remark`) VALUES
('张三', '男', '1985-06-15', '高级工程师', '海洋研究所', '海洋地质', '13800138001', '11010119850615001X', '博士研究生', '博士', '海洋地质专家'),
('李四', '男', '1982-03-22', '工程师', '海洋研究所', '海洋化学', '13800138002', '11010119820322002X', '硕士研究生', '硕士', '海洋化学专家'),
('王五', '女', '1988-11-08', '助理工程师', '海洋研究所', '海洋生物', '13800138003', '11010119881108003X', '硕士研究生', '硕士', '海洋生物专家'),
('赵六', '男', '1980-09-30', '研究员', '海洋研究所', '海洋物理', '13800138004', '11010119800930004X', '博士研究生', '博士', '海洋物理专家');

-- ================================================
-- 航前调查人员表 (tb_base_hq_investigator)
-- ================================================
CREATE TABLE `tb_base_hq_investigator` (
  `uniqueid` varchar(100) NOT NULL,
  `task_name` varchar(100) DEFAULT NULL,
  `task_code` varchar(100) DEFAULT NULL,
  `ship` varchar(100) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `sex` varchar(4) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `title` varchar(40) DEFAULT NULL,
  `organization` varchar(45) DEFAULT NULL,
  `major` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `id_card_number` varchar(45) DEFAULT NULL,
  `education` varchar(45) DEFAULT NULL,
  `degree` varchar(45) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `preparer` varchar(45) DEFAULT NULL,
  `verifier` varchar(45) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航前调查人员表';

-- 插入测试航前调查人员数据
INSERT INTO `tb_base_hq_investigator` (`uniqueid`, `task_name`, `task_code`, `ship`, `name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`, `education`, `degree`, `remark`, `preparer`, `verifier`, `create_date`) VALUES
('hq_inv_001', '2024年春季海洋调查', 'HY-2024-001', '海洋号', '张三', '男', '1985-06-15', '高级工程师', '海洋研究所', '海洋地质', '13800138001', '11010119850615001X', '博士研究生', '博士', '海洋地质专家，负责海底采样', '李四', '王五', '2024-02-15'),
('hq_inv_002', '2024年春季海洋调查', 'HY-2024-001', '海洋号', '李四', '男', '1982-03-22', '工程师', '海洋研究所', '海洋化学', '13800138002', '11010119820322002X', '硕士研究生', '硕士', '海洋化学专家，负责水质分析', '张三', '王五', '2024-02-15');

-- ================================================
-- 航前设备表 (tb_base_hq_device)
-- ================================================
CREATE TABLE `tb_base_hq_device` (
  `uniqueid` varchar(100) NOT NULL,
  `task_name` varchar(100) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `id` varchar(45) DEFAULT NULL,
  `model` varchar(45) DEFAULT NULL,
  `traceability` varchar(45) DEFAULT NULL,
  `checkdate` date DEFAULT NULL,
  `certificate_number` varchar(45) DEFAULT NULL,
  `validity` varchar(45) DEFAULT NULL,
  `verification_institutions` varchar(45) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `attachment` text,
  `preparer` varchar(45) DEFAULT NULL,
  `verifier` varchar(45) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航前设备表';

-- 插入测试航前设备数据
INSERT INTO `tb_base_hq_device` (`uniqueid`, `task_name`, `type`, `name`, `id`, `model`, `traceability`, `checkdate`, `certificate_number`, `validity`, `verification_institutions`, `remark`, `attachment`, `preparer`, `verifier`, `create_date`) VALUES
('hq_dev_001', '2024年春季海洋调查', '测量仪器', 'CTD温盐深仪', 'CTD-2024-001', 'SBE-911plus', '可追溯', '2024-01-15', 'JJG-2024-001', '2025-01-14', '国家海洋计量站', '使用前需预热30分钟', NULL, '张三', '李四', '2024-02-15'),
('hq_dev_002', '2024年春季海洋调查', '测量仪器', '多参数水质仪', 'WQ-2024-001', 'YSI-EXO2', '可追溯', '2024-01-20', 'JJG-2024-002', '2025-01-19', '国家海洋计量站', '定期校准，确保精度', NULL, '李四', '王五', '2024-02-15');

-- ================================================
-- 航中调查人员表 (tb_base_hz_investigator)
-- ================================================
CREATE TABLE `tb_base_hz_investigator` (
  `uniqueid` varchar(100) NOT NULL,
  `task_name` varchar(100) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `sex` varchar(4) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `title` varchar(40) DEFAULT NULL,
  `organization` varchar(45) DEFAULT NULL,
  `major` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `id_card_number` varchar(45) DEFAULT NULL,
  `education` varchar(45) DEFAULT NULL,
  `degree` varchar(45) DEFAULT NULL,
  `work_content` text,
  `remark` varchar(100) DEFAULT NULL,
  `preparer` varchar(45) DEFAULT NULL,
  `verifier` varchar(45) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航中调查人员表';

-- 插入测试航中调查人员数据
INSERT INTO `tb_base_hz_investigator` (`uniqueid`, `task_name`, `name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`, `education`, `degree`, `work_content`, `remark`, `preparer`, `verifier`, `create_date`) VALUES
('hz_inv_001', '2024年春季海洋调查', '王五', '女', '1988-11-08', '助理工程师', '海洋研究所', '海洋生物', '13800138003', '11010119881108003X', '硕士研究生', '硕士', '负责海洋生物样品采集和分析', '海洋生物专家，负责生物多样性调查', '张三', '李四', '2024-03-01');

-- ================================================
-- 航中设备表 (tb_base_hz_device)
-- ================================================
CREATE TABLE `tb_base_hz_device` (
  `uniqueid` varchar(100) NOT NULL,
  `task_name` varchar(100) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `id` varchar(45) DEFAULT NULL,
  `model` varchar(45) DEFAULT NULL,
  `traceability` varchar(45) DEFAULT NULL,
  `checkdate` date DEFAULT NULL,
  `certificate_number` varchar(45) DEFAULT NULL,
  `validity` varchar(45) DEFAULT NULL,
  `verification_institutions` varchar(45) DEFAULT NULL,
  `work_content` text,
  `remark` varchar(100) DEFAULT NULL,
  `attachment` text,
  `preparer` varchar(45) DEFAULT NULL,
  `verifier` varchar(45) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='航中设备表';

-- 插入测试航中设备数据
INSERT INTO `tb_base_hz_device` (`uniqueid`, `task_name`, `type`, `name`, `id`, `model`, `traceability`, `checkdate`, `certificate_number`, `validity`, `verification_institutions`, `work_content`, `remark`, `attachment`, `preparer`, `verifier`, `create_date`) VALUES
('hz_dev_001', '2024年春季海洋调查', '采样设备', '沉积物采样器', 'SED-2024-001', 'Box-Corer', '可追溯', '2024-02-01', 'JJG-2024-003', '2025-01-31', '国家海洋计量站', '用于采集海底沉积物样品', '采样深度可达500米', NULL, '李四', '王五', '2024-03-01');

-- ================================================
-- 外业调查人员资质表 (tb_personnel_qualifications)
-- ================================================
CREATE TABLE `tb_personnel_qualifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) NOT NULL COMMENT '航次任务名称',
  `name` varchar(100) NOT NULL COMMENT '姓名',
  `sex` varchar(10) NOT NULL COMMENT '性别',
  `birthdate` date NOT NULL COMMENT '出生年月',
  `professional_title` varchar(100) NOT NULL COMMENT '职称',
  `employer` varchar(255) NOT NULL COMMENT '工作单位',
  `specialty` varchar(255) NOT NULL COMMENT '从事专业',
  `instruments` text COMMENT '本航次操作仪器',
  `training` text COMMENT '培训情况',
  `remarks` text COMMENT '备注',
  `attachments` json COMMENT '附件信息（JSON数组）',
  `user_id` int COMMENT '创建用户ID（用户隔离）',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_task_name` (`task_name`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='外业调查人员资质表';

-- 插入测试人员资质数据
INSERT INTO `tb_personnel_qualifications` (`id`, `task_name`, `name`, `sex`, `birthdate`, `professional_title`, `employer`, `specialty`, `instruments`, `training`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES
(1, '2024年春季海洋调查', '张三', '男', '1985-06-15', '高级工程师', '海洋研究所', '海洋地质', 'CTD温盐深仪、地质采样器', '海洋调查技术培训，地质采样专项培训', '具有丰富的外业调查经验，精通CTD操作', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
(2, '2024年春季海洋调查', '李四', '男', '1982-03-22', '工程师', '海洋研究所', '海洋化学', '多参数水质仪、分光光度计', '海洋化学分析培训，水质监测专项培训', '海洋化学分析专家，熟悉多种仪器操作', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
(3, '2024年春季海洋调查', '王五', '女', '1988-11-08', '助理工程师', '海洋研究所', '海洋生物', '生物采样器、显微镜', '海洋生物采样培训，实验室分析培训', '海洋生物学专业，负责生物样品采集', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00');

-- ================================================
-- 仪器设备表 (tb_equipment)
-- ================================================
CREATE TABLE `tb_equipment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) NOT NULL COMMENT '航次任务名称',
  `category` varchar(50) NOT NULL COMMENT '设备类别',
  `equipment_name` varchar(255) NOT NULL COMMENT '仪器（标准物质）名称',
  `serial_number` varchar(100) NOT NULL COMMENT '编号',
  `model` varchar(100) NOT NULL COMMENT '型号',
  `measurement_range` text COMMENT '量程/测量方式',
  `calibration_date` date COMMENT '检定/校准日期',
  `certificate_number` varchar(100) COMMENT '证书编号',
  `validity_period` date COMMENT '有效期',
  `calibration_organization` varchar(255) COMMENT '检定/校准机构',
  `remarks` text COMMENT '备注',
  `attachments` json COMMENT '附件信息（JSON数组）',
  `user_id` int COMMENT '创建用户ID（用户隔离）',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_task_name` (`task_name`),
  KEY `idx_equipment_name` (`equipment_name`),
  KEY `idx_validity_period` (`validity_period`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='外业设备（工作计量器具）表';

-- 插入测试设备数据
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `equipment_name`, `serial_number`, `model`, `measurement_range`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES
(1, '2024年春季海洋调查', '测量仪器', 'CTD温盐深仪', 'CTD-2024-001', 'SBE-911plus', '温度：-5~35℃，盐度：0~70PSU，深度：0~6000m', '2024-01-15', 'JJG-2024-001', '2025-01-14', '国家海洋计量站', '使用前需预热30分钟，定期校准，确保精度', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
(2, '2024年春季海洋调查', '测量仪器', '多参数水质仪', 'WQ-2024-001', 'YSI-EXO2', 'pH：0~14，溶解氧：0~50mg/L，浊度：0~4000NTU', '2024-01-20', 'JJG-2024-002', '2025-01-19', '国家海洋计量站', '定期校准，确保测量精度，适合长期监测', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
(3, '2024年春季海洋调查', '采样设备', '沉积物采样器', 'SED-2024-001', 'Box-Corer', '采样面积：0.25m²，采样深度：0~50cm', '2024-02-01', 'JJG-2024-003', '2025-01-31', '国家海洋计量站', '采样深度可达500米，适用于深海沉积物采集', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00');

-- ================================================
-- 外业调查项目表 (tb_investigation_projects)
-- ================================================
CREATE TABLE `tb_investigation_projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) NOT NULL COMMENT '航次任务名称',
  `investigation_item` varchar(255) NOT NULL COMMENT '调查项目/仪器',
  `unit_a_equipment` varchar(255) NOT NULL COMMENT '比测单位甲仪器',
  `unit_b_equipment` varchar(255) NOT NULL COMMENT '比测单位乙仪器',
  `comparison_time` datetime NOT NULL COMMENT '比测时间',
  `comparison_location` varchar(255) NOT NULL COMMENT '比测地点',
  `comparison_result` varchar(50) NOT NULL COMMENT '比测结果',
  `remarks` text COMMENT '备注',
  `attachments` json COMMENT '附件信息（JSON数组）',
  `user_id` int COMMENT '创建用户ID（用户隔离）',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_task_name` (`task_name`),
  KEY `idx_investigation_item` (`investigation_item`),
  KEY `idx_comparison_time` (`comparison_time`),
  KEY `idx_comparison_result` (`comparison_result`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='外业调查项目表';

-- 插入测试调查项目数据
INSERT INTO `tb_investigation_projects` (`id`, `task_name`, `investigation_item`, `unit_a_equipment`, `unit_b_equipment`, `comparison_time`, `comparison_location`, `comparison_result`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES
(1, '2024年春季海洋调查', 'CTD温盐深测量', 'SBE-911plus', 'RBR-CTD', '2024-01-15 14:30:00', '青岛海洋站实验室', '一致', '比测结果良好，数据一致性高，温度测量误差小于0.01℃', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
(2, '2024年春季海洋调查', '多参数水质监测', 'YSI-EXO2', 'HACH-HQ40D', '2024-01-20 09:15:00', '青岛海洋站实验室', '基本一致', 'pH测量结果差异0.02，溶解氧测量结果差异0.1mg/L，在可接受范围内', NULL, 1, '2024-01-15 10:30:00', '2024-01-15 10:30:00');

-- 启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- ================================================
-- 创建数据库完成提示
-- ================================================
SELECT '海洋调查现场质量监督管理系统数据库创建完成！' as result;
SELECT '数据库名: marine_survey_db' as database_info;
SELECT '包含表数量: 13个' as table_count;
SELECT CONCAT('总记录数: ', (
    SELECT SUM(table_rows) FROM information_schema.tables
    WHERE table_schema = 'marine_survey_db'
)) as record_count;
