-- ================================================
-- 海洋调查现场质量监督管理系统 - 数据库完整备份
-- 生成时间: 2025-09-30
-- 数据库名: marine_survey_db
-- ================================================

-- 设置字符集
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


-- ----------------------------
-- Table structure for tb_base_hq_device
-- ----------------------------
DROP TABLE IF EXISTS `tb_base_hq_device`;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for tb_base_hq_investigator
-- ----------------------------
DROP TABLE IF EXISTS `tb_base_hq_investigator`;
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
  `instrument` varchar(45) DEFAULT NULL,
  `trainingdate` varchar(45) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `preparer` varchar(45) DEFAULT NULL,
  `verifier` varchar(45) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  `attachment` text,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for tb_base_hz_device
-- ----------------------------
DROP TABLE IF EXISTS `tb_base_hz_device`;
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
  `remark` varchar(100) DEFAULT NULL,
  `attachment` text,
  `preparer` varchar(45) DEFAULT NULL,
  `verifier` varchar(45) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for tb_base_hz_investigator
-- ----------------------------
DROP TABLE IF EXISTS `tb_base_hz_investigator`;
CREATE TABLE `tb_base_hz_investigator` (
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
  `instrument` varchar(45) DEFAULT NULL,
  `trainingdate` varchar(45) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `preparer` varchar(45) DEFAULT NULL,
  `verifier` varchar(45) DEFAULT NULL,
  `create_date` date DEFAULT NULL,
  `attachment` text,
  PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for tb_base_master
-- ----------------------------
DROP TABLE IF EXISTS `tb_base_master`;
CREATE TABLE `tb_base_master` (
  `name` varchar(40) DEFAULT NULL,
  `sex` varchar(4) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `organization` varchar(45) DEFAULT NULL,
  `major` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `id_card_number` varchar(45) NOT NULL,
  `band_card_number` varchar(45) DEFAULT NULL,
  `opening_band` varchar(45) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT '3' COMMENT '创建人员信息的用户ID',
  PRIMARY KEY (`id_card_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of tb_base_master
-- ----------------------------
INSERT INTO `tb_base_master` (`name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`, `band_card_number`, `opening_band`, `remark`, `user_id`) VALUES ('李四', '女', '1985-05-15', '研究员', '海洋中心', NULL, '13800138002', '110101198505151234', NULL, NULL, NULL, 3);
INSERT INTO `tb_base_master` (`name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`, `band_card_number`, `opening_band`, `remark`, `user_id`) VALUES ('王五', '男', '1988-08-20', '助理研究员', '海洋实验室', NULL, '13800138003', '110101198808201234', NULL, NULL, NULL, 3);
INSERT INTO `tb_base_master` (`name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`, `band_card_number`, `opening_band`, `remark`, `user_id`) VALUES ('张三', '男', '1990-01-01', '工程师', '海洋研究所', NULL, '13800138001', '110101199001011234', NULL, NULL, NULL, 3);
INSERT INTO `tb_base_master` (`name`, `sex`, `birthday`, `title`, `organization`, `major`, `phone`, `id_card_number`, `band_card_number`, `opening_band`, `remark`, `user_id`) VALUES ('赵六', '女', '1992-03-10', '技术员', '海洋监测站', NULL, '13800138004', '110101199203101234', NULL, NULL, NULL, 3);


-- ----------------------------
-- Table structure for tb_equipment
-- ----------------------------
DROP TABLE IF EXISTS `tb_equipment`;
CREATE TABLE `tb_equipment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '类别',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '仪器（标准物质）名称',
  `number` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '编号',
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '型号',
  `traceability_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '量值溯源方式',
  `calibration_date` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '检定/校准日期',
  `certificate_number` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '证书编号',
  `validity_period` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '有效期',
  `calibration_organization` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '检定/校准机构',
  `remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '附件信息（JSON字符串）',
  `user_id` int NOT NULL COMMENT '创建用户ID（用户隔离）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_equipment
-- ----------------------------
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '南海海洋调查任务', '仪器', 'CTD温盐深仪', 'CTD-001', 'SBE-911', '国家海洋计量站校准', '2024-03-15', 'OM-2024-001', '2025-03-15', '国家海洋计量站', '用于海洋温盐深剖面测量', '[]', 1, '2025-10-02 16:48:55', '2025-10-02 16:48:55');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (2, '南海海洋调查任务', '标准物质', '海水盐度标准物质', 'SS-002', 'IAPSO标准海水', '国际原子能机构溯源', '2024-01-10', 'IAEA-2024-002', '2026-01-10', '国际原子能机构', '用于盐度测量校准', '[]', 1, '2025-10-02 16:48:55', '2025-10-02 16:48:55');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (3, '东海海洋调查任务', '计量器具', '数字温度计', 'DT-003', 'Fluke-51II', '国家计量院校准', '2024-02-20', 'NIM-2024-003', '2025-02-20', '国家计量院', '用于水温测量', '[]', 1, '2025-10-02 16:48:55', '2025-10-02 16:48:55');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (4, '东海海洋调查', '仪器', 'weqwe', 'awddaw', 'awdaw', 'awdaw', '2025-10-01', 'awdwa', 'wadaw', 'dwad', 'awdaw', '[{"name": "2024-08-14_105917.png", "url": "http://localhost:5000/static/uploads/equipment_attachments/20251003055928_3_2024-08-14_105917.png", "uid": "20251003055928"}]', 3, '2025-10-02 16:52:30', '2025-10-03 05:59:44');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (5, '东海海洋调查', '仪器', 'wdwa', 'wdad', 'awda', '伟大阿瓦', '', '挖的', '', '', '', '[{"name": "2024-08-14_105917.png", "url": "http://localhost:5000/static/uploads/equipment_attachments/20251003064132_3_2024-08-14_105917.png", "uid": "20251003064132"}]', 3, '2025-10-02 20:05:05', '2025-10-03 06:41:35');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (6, '东海海洋调查', '仪器', '达瓦', '伟大阿瓦', '啊伟大伟大', '啊伟大伟大', '2025-10-02', '啊伟大伟大', '哇啊挖的', '娃娃大', '伟大阿瓦达', '[{"name": "2024-08-14_105917.png", "url": "http://localhost:5000/static/uploads/equipment_attachments/20251003064112_3_2024-08-14_105917.png", "uid": "20251003064112"}]', 3, '2025-10-03 06:41:28', '2025-10-03 06:41:28');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (7, '南海深海探测', '仪器', '哇大王', '伟大挖的', '伟大阿瓦达', '哇哇', '', '', '', '', '', '[{"name": "2024-08-14_105917.png", "url": "http://localhost:5000/static/uploads/equipment_attachments/20251003070938_3_2024-08-14_105917.png", "uid": "20251003070938"}]', 3, '2025-10-03 07:09:39', '2025-10-03 07:09:39');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (8, '南海深海探测', '仪器', '达瓦', '伟大', '伟大挖的', '', '', '', '', '', '', '[]', 3, '2025-10-03 11:02:54', '2025-10-03 11:02:54');
INSERT INTO `tb_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (9, '东海海洋调查', '仪器', '大王的', '啊吴大维', '啊我的娃', '娃娃大', '', '', '', '', '', '[]', 3, '2025-10-03 20:24:13', '2025-10-03 20:24:13');


-- ----------------------------
-- Table structure for tb_expert_talent
-- ----------------------------
DROP TABLE IF EXISTS `tb_expert_talent`;
CREATE TABLE `tb_expert_talent` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `gender` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '性别',
  `birth_date` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '出生年月',
  `job_title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '职称',
  `work_unit` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '工作单位',
  `specialty` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '从事专业',
  `contact_info` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系方式',
  `id_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号',
  `bank_card_number` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '银行卡号',
  `opening_bank` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '开户行',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------
-- Table structure for tb_investigation_projects
-- ----------------------------
DROP TABLE IF EXISTS `tb_investigation_projects`;
CREATE TABLE `tb_investigation_projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `investigation_item` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '调查项目/仪器',
  `unit_a_instrument` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '比测单位甲仪器',
  `unit_b_instrument` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '比测单位乙仪器',
  `comparison_time` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '比测时间',
  `comparison_location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '比测地点',
  `comparison_result` text COLLATE utf8mb4_unicode_ci COMMENT '比测结果',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件信息（JSON字符串）',
  `user_id` int NOT NULL COMMENT '创建用户ID（用户隔离）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_investigation_projects
-- ----------------------------
INSERT INTO `tb_investigation_projects` (`id`, `task_name`, `investigation_item`, `unit_a_instrument`, `unit_b_instrument`, `comparison_time`, `comparison_location`, `comparison_result`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '哇大啊', '阿斯旺挖的', '吴大维', '', '', '', '', '[]', 3, '2025-10-09 18:47:47', '2025-10-09 18:47:52');


-- ----------------------------
-- Table structure for tb_onboard_inspection
-- ----------------------------
DROP TABLE IF EXISTS `tb_onboard_inspection`;
CREATE TABLE `tb_onboard_inspection` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `inspected_unit` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '被检查承担单位',
  `participating_unit` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '被检查参加单位',
  `task_code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '航次任务编号',
  `chief_scientist` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '航次首席科学家',
  `inspection_date` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '检查日期',
  `onboard_supervisor` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '随船质量监督员',
  `inspected_unit_personnel` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '被检查单位(部门)主要参与人员',
  `check_1` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容1',
  `check_1_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题1',
  `check_2` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容2',
  `check_2_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题2',
  `check_3` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容3',
  `check_3_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题3',
  `check_4` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容4',
  `check_4_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题4',
  `check_5` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容5',
  `check_5_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题5',
  `check_6` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容6',
  `check_6_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题6',
  `check_7` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容7',
  `check_7_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题7',
  `check_8` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容8',
  `check_8_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题8',
  `check_9` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容9',
  `check_9_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题9',
  `check_10` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容10',
  `check_10_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题10',
  `check_11` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容11',
  `check_11_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题11',
  `check_12` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容12',
  `check_12_problem` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题12',
  `team_leader_sign` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组长签字',
  `task_leader_sign` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务负责人签字',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件信息(JSON格式)',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_onboard_inspection
-- ----------------------------
INSERT INTO `tb_onboard_inspection` (`id`, `task_name`, `inspected_unit`, `participating_unit`, `task_code`, `chief_scientist`, `inspection_date`, `onboard_supervisor`, `inspected_unit_personnel`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_12`, `check_12_problem`, `team_leader_sign`, `task_leader_sign`, `attachments`, `user_id`) VALUES (1, '东海海洋调查', '阿瓦达达娃', '低洼阿迪王', '', '', '', '', '', '', '', '哇达瓦低洼地', '', '哇低洼低洼的', '', '达瓦达瓦达瓦', '', '', '', '啊伟大伟大', '', '娃娃吊带袜', '', '', '', '', '', '', '', '', '', '', '', '', '', '[]', 3);


-- ----------------------------
-- Table structure for tb_original_records
-- ----------------------------
DROP TABLE IF EXISTS `tb_original_records`;
CREATE TABLE `tb_original_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `survey_item` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '调查项目',
  `task_undertaking_unit` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务承担单位',
  `station` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '站位',
  `time` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '时间',
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '地点',
  `spot_check_time` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '抽查时间',
  `qualified_or_not` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '合格与否',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件列表，存储JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tb_original_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_original_records
-- ----------------------------
INSERT INTO `tb_original_records` (`id`, `task_name`, `survey_item`, `task_undertaking_unit`, `station`, `time`, `location`, `spot_check_time`, `qualified_or_not`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '挖的低洼', '伟大阿瓦达', '伟大的哇', '', '挖的低洼', '', '', '', '[]', 3, '2025-10-10 11:08:51', '2025-10-10 11:08:51');


-- ----------------------------
-- Table structure for tb_personnel_qualifications
-- ----------------------------
DROP TABLE IF EXISTS `tb_personnel_qualifications`;
CREATE TABLE `tb_personnel_qualifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `sex` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '性别',
  `birthdate` date NOT NULL COMMENT '出生年月',
  `professional_title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '职称',
  `employer` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '工作单位',
  `specialty` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '从事专业',
  `instruments` text COLLATE utf8mb4_unicode_ci COMMENT '本航次操作仪器',
  `training` text COLLATE utf8mb4_unicode_ci COMMENT '培训情况',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件信息（JSON字符串）',
  `user_id` int DEFAULT NULL COMMENT '创建用户ID（用户隔离）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_personnel_qualifications
-- ----------------------------
INSERT INTO `tb_personnel_qualifications` (`id`, `task_name`, `name`, `sex`, `birthdate`, `professional_title`, `employer`, `specialty`, `instruments`, `training`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '达瓦', '男', '2025-01-01', '哇大王', '伟大哇', '挖的', '哇大王', '哇大王', '', NULL, 3, '2025-10-10 10:59:23', '2025-10-10 10:59:23');
INSERT INTO `tb_personnel_qualifications` (`id`, `task_name`, `name`, `sex`, `birthdate`, `professional_title`, `employer`, `specialty`, `instruments`, `training`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (2, '东海海洋调查', '阿瓦达', '女', '2025-01-01', '阿瓦达达娃', '阿达伟大', '哇大王', '啊微微的', '我打阿迪王', '', NULL, 3, '2025-10-10 10:59:40', '2025-10-10 10:59:40');


-- ----------------------------
-- Table structure for tb_post_inspection
-- ----------------------------
DROP TABLE IF EXISTS `tb_post_inspection`;
CREATE TABLE `tb_post_inspection` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `inspection_date` date DEFAULT NULL COMMENT '检查日期',
  `inspection_content` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容',
  `existing_problems` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题',
  `rectification_status` text COLLATE utf8mb4_unicode_ci COMMENT '整改情况',
  `form_filling_time` date DEFAULT NULL COMMENT '填表时间',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------
-- Table structure for tb_pre_summary
-- ----------------------------
DROP TABLE IF EXISTS `tb_pre_summary`;
CREATE TABLE `tb_pre_summary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `undertaking_unit` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '航次承担单位',
  `participating_unit` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '航次参与单位',
  `task_code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '航次任务编号',
  `survey_vessel` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '调查船',
  `task_leader` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务负责人',
  `supervision_personnel` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '监督检查人员',
  `main_participants` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '受检查单位主要参与人员',
  `inspection_date` date DEFAULT NULL COMMENT '检查日期',
  `inspection_details` text COLLATE utf8mb4_unicode_ci COMMENT '检查情况',
  `inspection_results` text COLLATE utf8mb4_unicode_ci COMMENT '检查结果',
  `related_materials` text COLLATE utf8mb4_unicode_ci COMMENT '相关资料JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_pre_summary
-- ----------------------------
INSERT INTO `tb_pre_summary` (`id`, `task_name`, `undertaking_unit`, `participating_unit`, `task_code`, `survey_vessel`, `task_leader`, `supervision_personnel`, `main_participants`, `inspection_date`, `inspection_details`, `inspection_results`, `related_materials`, `user_id`, `created_at`, `updated_at`) VALUES (1, '东海海洋调查', '啊哇哇', '挖的哇', '的娃娃', '多少多少钱', '阿达瓦', '阿达瓦', '大啊吊带袜', '2025-10-21', '达瓦伟大', '阿瓦达达娃', NULL, 3, '2025-10-10 11:03:32', '2025-10-12 19:51:12');


-- ----------------------------
-- Table structure for tb_procedure_execution
-- ----------------------------
DROP TABLE IF EXISTS `tb_procedure_execution`;
CREATE TABLE `tb_procedure_execution` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `investigation_item_instrument` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '调查项目/仪器',
  `task_undertaking_unit` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务承担单位',
  `has_operating_procedures` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '是否具有操作规程',
  `operating_procedure_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作规程名称',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件列表，存储JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tb_procedure_execution_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_procedure_execution
-- ----------------------------
INSERT INTO `tb_procedure_execution` (`id`, `task_name`, `investigation_item_instrument`, `task_undertaking_unit`, `has_operating_procedures`, `operating_procedure_name`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '啊伟大伟大', '阿瓦达达娃', '是', '伟大达娃', '', '[]', 3, '2025-10-10 11:08:59', '2025-10-10 11:08:59');


-- ----------------------------
-- Table structure for tb_sample_storage
-- ----------------------------
DROP TABLE IF EXISTS `tb_sample_storage`;
CREATE TABLE `tb_sample_storage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `survey_item` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '调查项目',
  `task_undertaking_unit` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务承担单位',
  `stored_samples` text COLLATE utf8mb4_unicode_ci COMMENT '储存样品',
  `record_time` date DEFAULT NULL COMMENT '记录时间',
  `spot_check_time` date DEFAULT NULL COMMENT '抽查时间',
  `qualified_or_not` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '合格与否',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_sample_storage
-- ----------------------------
INSERT INTO `tb_sample_storage` (`id`, `task_name`, `survey_item`, `task_undertaking_unit`, `stored_samples`, `record_time`, `spot_check_time`, `qualified_or_not`, `remarks`, `attachments`, `user_id`, `created_at`, `updated_at`) VALUES (1, '东海海洋调查', '阿瓦伟大的哇', '伟大伟大', '', NULL, '2025-10-09', '不合格', '', NULL, 3, '2025-10-10 11:09:15', '2025-10-10 11:09:15');


-- ----------------------------
-- Table structure for tb_supervisor_log
-- ----------------------------
DROP TABLE IF EXISTS `tb_supervisor_log`;
CREATE TABLE `tb_supervisor_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `supervisor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '监督员',
  `inspection_date` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '检查日期',
  `inspection_content` text COLLATE utf8mb4_unicode_ci COMMENT '检查内容',
  `existing_problems` text COLLATE utf8mb4_unicode_ci COMMENT '存在问题',
  `rectification_status` text COLLATE utf8mb4_unicode_ci COMMENT '整改情况',
  `form_filling_time` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '填表时间',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件列表，存储JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tb_supervisor_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_supervisor_log
-- ----------------------------
INSERT INTO `tb_supervisor_log` (`id`, `task_name`, `supervisor`, `inspection_date`, `inspection_content`, `existing_problems`, `rectification_status`, `form_filling_time`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '哇大王', '2025-10-02', '啊我的娃', '啊我的娃', '阿瓦达', '2025-10-09 00:00:00', '[]', 3, '2025-10-10 11:08:43', '2025-10-10 11:08:43');


-- ----------------------------
-- Table structure for tb_task_hqzljdjcjlb
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_hqzljdjcjlb`;
CREATE TABLE `tb_task_hqzljdjcjlb` (
  `task_name` varchar(100) NOT NULL,
  `check_date` text,
  `superintendent` varchar(100) DEFAULT NULL,
  `superintended` varchar(45) DEFAULT NULL,
  `check_1` varchar(200) DEFAULT NULL,
  `check_1_problem` varchar(200) DEFAULT NULL,
  `check_2` varchar(200) DEFAULT NULL,
  `check_2_problem` varchar(200) DEFAULT NULL,
  `check_3` varchar(200) DEFAULT NULL,
  `check_3_problem` varchar(200) DEFAULT NULL,
  `check_4` varchar(200) DEFAULT NULL,
  `check_4_problem` varchar(200) DEFAULT NULL,
  `check_5` varchar(200) DEFAULT NULL,
  `check_5_problem` varchar(200) DEFAULT NULL,
  `check_6` varchar(200) DEFAULT NULL,
  `check_6_problem` varchar(200) DEFAULT NULL,
  `check_7` varchar(200) DEFAULT NULL,
  `check_7_problem` varchar(200) DEFAULT NULL,
  `check_8` varchar(200) DEFAULT NULL,
  `check_8_problem` varchar(200) DEFAULT NULL,
  `check_9` varchar(200) DEFAULT NULL,
  `check_9_problem` varchar(200) DEFAULT NULL,
  `check_10` varchar(200) DEFAULT NULL,
  `check_10_problem` varchar(200) DEFAULT NULL,
  `check_11` varchar(200) DEFAULT NULL,
  `check_11_problem` varchar(200) DEFAULT NULL,
  `check_detail` text,
  `check_result` text,
  `chief_scientist_sign` varchar(45) DEFAULT NULL,
  `check_leader_sign` varchar(45) DEFAULT NULL,
  `chief_scientist_signdate` date DEFAULT NULL,
  `check_leader_signdate` date DEFAULT NULL,
  `create_date` text,
  `user_id` int DEFAULT '3' COMMENT '创建检查记录的用户ID',
  PRIMARY KEY (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of tb_task_hqzljdjcjlb
-- ----------------------------
INSERT INTO `tb_task_hqzljdjcjlb` (`task_name`, `check_date`, `superintendent`, `superintended`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_detail`, `check_result`, `chief_scientist_sign`, `check_leader_sign`, `chief_scientist_signdate`, `check_leader_signdate`, `create_date`, `user_id`) VALUES ('111', '', '111', '111', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 12);
INSERT INTO `tb_task_hqzljdjcjlb` (`task_name`, `check_date`, `superintendent`, `superintended`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_detail`, `check_result`, `chief_scientist_sign`, `check_leader_sign`, `chief_scientist_signdate`, `check_leader_signdate`, `create_date`, `user_id`) VALUES ('东海海洋调查', '111', '阿迪王低洼的', '的娃娃', NULL, NULL, NULL, NULL, '达瓦伟大', NULL, '伟大达娃', NULL, '达瓦达瓦', NULL, '我的娃达娃', NULL, '111', NULL, NULL, NULL, '啊我的娃', NULL, '阿迪王伟大伟大', NULL, '达瓦阿瓦达', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3);
INSERT INTO `tb_task_hqzljdjcjlb` (`task_name`, `check_date`, `superintendent`, `superintended`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_detail`, `check_result`, `chief_scientist_sign`, `check_leader_sign`, `chief_scientist_signdate`, `check_leader_signdate`, `create_date`, `user_id`) VALUES ('南海深海探测', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3);
INSERT INTO `tb_task_hqzljdjcjlb` (`task_name`, `check_date`, `superintendent`, `superintended`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_detail`, `check_result`, `chief_scientist_sign`, `check_leader_sign`, `chief_scientist_signdate`, `check_leader_signdate`, `create_date`, `user_id`) VALUES ('海洋生物任务002', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3);
INSERT INTO `tb_task_hqzljdjcjlb` (`task_name`, `check_date`, `superintendent`, `superintended`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_detail`, `check_result`, `chief_scientist_sign`, `check_leader_sign`, `chief_scientist_signdate`, `check_leader_signdate`, `create_date`, `user_id`) VALUES ('海洋调查任务001', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3);
INSERT INTO `tb_task_hqzljdjcjlb` (`task_name`, `check_date`, `superintendent`, `superintended`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_detail`, `check_result`, `chief_scientist_sign`, `check_leader_sign`, `chief_scientist_signdate`, `check_leader_signdate`, `create_date`, `user_id`) VALUES ('渤海环境监测', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3);


-- ----------------------------
-- Table structure for tb_task_info
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_info`;
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
  `user_id` int DEFAULT '3' COMMENT '创建任务的用户ID',
  PRIMARY KEY (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of tb_task_info
-- ----------------------------
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`, `user_id`) VALUES ('111', '111', NULL, NULL, '111', NULL, NULL, '111', '111', '111', '111', '11', 12);
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`, `user_id`) VALUES ('海洋资源调查专项', '东海海洋调查', 'HY20250011', '国家海洋标准计量中心', '达瓦伟大', '向阳红01', '张主任', '的娃娃伟大', '达瓦达瓦', '啊大无畏的', '2025-01-15 至 2025-02-20', '海洋地质', 3);
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`, `user_id`) VALUES ('深海科考专项', '南海深海探测', 'HY2025002', '中国海洋大学', '', '科学号', '李教授', '', '', '', '2025-03-01 至 2025-04-15', '海洋生物', 3);
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`, `user_id`) VALUES ('海洋生物调查', '海洋生物任务002', 'TASK002', '海洋中心', '王五', '生物号', '李主任', '陈教授', '孙监督', NULL, '2024年3月至8月', '海洋生物多样性', 3);
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`, `user_id`) VALUES ('海洋调查项目', '海洋调查任务001', 'TASK001', '海洋研究所', '张三,李四', '海洋号', '张主任', '李教授', '王监督', NULL, '2024年1月至6月', '海洋环境监测', 3);
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`, `user_id`) VALUES ('海洋环境保护专项', '渤海环境监测', 'HY2025003', '海洋环境监测中心', '', '海巡01', '王工程师', '', '', '', '2025-05-10 至 2025-06-20', '海洋化学', 3);


-- ----------------------------
-- Table structure for tb_task_sczljdjcb
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_sczljdjcb`;
CREATE TABLE `tb_task_sczljdjcb` (
  `task_name` varchar(100) NOT NULL,
  `check_date` text,
  `superintendent` varchar(100) DEFAULT NULL,
  `superintended` varchar(100) DEFAULT NULL,
  `check_1` varchar(200) DEFAULT NULL,
  `check_1_problem` varchar(200) DEFAULT NULL,
  `check_2` varchar(200) DEFAULT NULL,
  `check_2_problem` varchar(200) DEFAULT NULL,
  `check_3` varchar(200) DEFAULT NULL,
  `check_3_problem` varchar(200) DEFAULT NULL,
  `check_4` varchar(200) DEFAULT NULL,
  `check_4_problem` varchar(200) DEFAULT NULL,
  `check_5` varchar(200) DEFAULT NULL,
  `check_5_problem` varchar(200) DEFAULT NULL,
  `check_6` varchar(200) DEFAULT NULL,
  `check_6_problem` varchar(200) DEFAULT NULL,
  `check_7` varchar(200) DEFAULT NULL,
  `check_7_problem` varchar(200) DEFAULT NULL,
  `check_8` varchar(200) DEFAULT NULL,
  `check_8_problem` varchar(200) DEFAULT NULL,
  `check_9` varchar(200) DEFAULT NULL,
  `check_9_problem` varchar(200) DEFAULT NULL,
  `check_10` varchar(200) DEFAULT NULL,
  `check_10_problem` varchar(200) DEFAULT NULL,
  `check_11` varchar(200) DEFAULT NULL,
  `check_11_problem` varchar(200) DEFAULT NULL,
  `check_12` varchar(200) DEFAULT NULL,
  `check_12_problem` varchar(200) DEFAULT NULL,
  `chief_scientist_sign` varchar(45) DEFAULT NULL,
  `check_leader_sign` varchar(45) DEFAULT NULL,
  `chief_scientist_signdate` date DEFAULT NULL,
  `check_leader_signdate` date DEFAULT NULL,
  `create_date` text,
  PRIMARY KEY (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for tb_task_unit
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_unit`;
CREATE TABLE `tb_task_unit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '单位名称',
  `specialized_person` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '专项负责人',
  `quality_manager` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '质量管理负责人',
  `contact_person` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系人',
  `contact_info` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系方式',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_task_unit
-- ----------------------------
INSERT INTO `tb_task_unit` (`id`, `unit_name`, `specialized_person`, `quality_manager`, `contact_person`, `contact_info`, `remarks`, `user_id`) VALUES (1, '大啊伟大', '达瓦', '伟大哇', '阿达瓦', '我的娃', '吴大维', 3);
INSERT INTO `tb_task_unit` (`id`, `unit_name`, `specialized_person`, `quality_manager`, `contact_person`, `contact_info`, `remarks`, `user_id`) VALUES (2, '伟大伟大', '达瓦达瓦', '的娃娃', '挖挖达瓦', '我的娃', '哇大王', 3);


-- ----------------------------
-- Table structure for tb_task_zlpgb
-- ----------------------------
DROP TABLE IF EXISTS `tb_task_zlpgb`;
CREATE TABLE `tb_task_zlpgb` (
  `task_name` varchar(100) NOT NULL,
  `evaluated_unit` varchar(200) DEFAULT NULL,
  `check_1_grade` int DEFAULT NULL,
  `check_1_problem` varchar(200) DEFAULT NULL,
  `check_2_grade` int DEFAULT NULL,
  `check_2_problem` varchar(200) DEFAULT NULL,
  `check_3_grade` int DEFAULT NULL,
  `check_3_problem` varchar(200) DEFAULT NULL,
  `check_4_grade` int DEFAULT NULL,
  `check_4_problem` varchar(200) DEFAULT NULL,
  `check_5_grade` int DEFAULT NULL,
  `check_5_problem` varchar(200) DEFAULT NULL,
  `check_6_grade` int DEFAULT NULL,
  `check_6_problem` varchar(200) DEFAULT NULL,
  `check_7_grade` int DEFAULT NULL,
  `check_7_problem` varchar(200) DEFAULT NULL,
  `check_8_grade` int DEFAULT NULL,
  `check_8_problem` varchar(200) DEFAULT NULL,
  `check_9_grade` int DEFAULT NULL,
  `check_9_problem` varchar(200) DEFAULT NULL,
  `check_10_grade` int DEFAULT NULL,
  `check_10_problem` varchar(200) DEFAULT NULL,
  `check_11_grade` int DEFAULT NULL,
  `check_11_problem` varchar(200) DEFAULT NULL,
  `check_12_grade` int DEFAULT NULL,
  `check_12_problem` varchar(200) DEFAULT NULL,
  `check_13_grade` int DEFAULT NULL,
  `check_13_problem` varchar(200) DEFAULT NULL,
  `evaluated_sign` varchar(45) DEFAULT NULL,
  `evaluator_sign` varchar(45) DEFAULT NULL,
  `evaluated_signdate` date DEFAULT NULL,
  `evaluator_signdate` date DEFAULT NULL,
  `create_date` text,
  PRIMARY KEY (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for tb_user
-- ----------------------------
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of tb_user
-- ----------------------------
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (1, 'test', '123456', '111', NULL, '111', NULL, NULL, '111', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (2, '12', '12', '12', '12', '12', NULL, NULL, '12', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (3, '123', '123456', '123', '男', '普通用户', NULL, NULL, '未分配', 'RunshiLi2004Stone@outlook.com', '15963300728', 'data:image/png;base64,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');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (4, 'admin', '123456', 'admin', NULL, 'super_admin', NULL, NULL, 'IT_Department', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (5, 'newuser', '123456', 'newuser', NULL, '普通用户', NULL, NULL, '未分配', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (6, 'testlogin', '123', 'TestUser', NULL, 'user', NULL, NULL, 'IT', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (7, '娴嬭瘯鐢ㄦ埛', '123456', '娴嬭瘯鐢ㄦ埛', NULL, '普通用户', NULL, NULL, '未分配', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (8, 'zhangsan', '123456', '张三', NULL, '普通用户', NULL, NULL, '业务部门', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (9, 'lisi', '123456', '李四', NULL, '普通用户', NULL, NULL, '业务部门', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (10, 'wangwu', '123456', '王五', NULL, '部门经理', NULL, NULL, '管理部门', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (11, '鐜嬩簲', '123456', '鐜嬩簲', NULL, '普通用户', NULL, NULL, '未分配', NULL, NULL, NULL);
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`, `email`, `phone`, `signature`) VALUES (12, '1234', '123456', '1234', '未知', '普通用户', '', '基础权限', '未分配', NULL, NULL, NULL);


-- ----------------------------
-- Table structure for tb_voyage_equipment
-- ----------------------------
DROP TABLE IF EXISTS `tb_voyage_equipment`;
CREATE TABLE `tb_voyage_equipment` (
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_voyage_equipment
-- ----------------------------
INSERT INTO `tb_voyage_equipment` (`id`, `task_name`, `category`, `name`, `number`, `model`, `traceability_method`, `calibration_date`, `certificate_number`, `validity_period`, `calibration_organization`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '仪器', '达瓦大屋顶', '挖的伟大', '阿瓦达达娃', '挖挖达瓦', '2025-10-02', '', '', '', '', '[]', 3, '2025-10-10 11:08:23', '2025-10-10 11:08:23');


-- ----------------------------
-- Table structure for tb_voyage_investigation_project
-- ----------------------------
DROP TABLE IF EXISTS `tb_voyage_investigation_project`;
CREATE TABLE `tb_voyage_investigation_project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `investigation_item_instrument` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '调查项目/仪器',
  `comparison_unit_a_instrument` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '比测单位甲及仪器',
  `comparison_unit_b_instrument` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '比测单位乙及仪器',
  `comparison_time` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '比测时间',
  `comparison_location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '比测地点',
  `comparison_result` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '比测结果',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件列表，存储JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tb_voyage_investigation_project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_voyage_investigation_project
-- ----------------------------
INSERT INTO `tb_voyage_investigation_project` (`id`, `task_name`, `investigation_item_instrument`, `comparison_unit_a_instrument`, `comparison_unit_b_instrument`, `comparison_time`, `comparison_location`, `comparison_result`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '阿瓦达达娃', '达瓦达瓦', '达瓦伟大的哇', '', '', '', '', '[]', 3, '2025-10-10 11:08:31', '2025-10-10 11:08:31');


-- ----------------------------
-- Table structure for tb_voyage_personnel
-- ----------------------------
DROP TABLE IF EXISTS `tb_voyage_personnel`;
CREATE TABLE `tb_voyage_personnel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `sex` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '性别',
  `birthdate` date NOT NULL COMMENT '出生年月',
  `professional_title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '职称',
  `employer` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '工作单位',
  `specialty` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '从事专业',
  `instruments` text COLLATE utf8mb4_unicode_ci COMMENT '本航次操作仪器',
  `training` text COLLATE utf8mb4_unicode_ci COMMENT '培训情况',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件信息（JSON字符串）',
  `user_id` int DEFAULT NULL COMMENT '创建用户ID（用户隔离）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_voyage_personnel
-- ----------------------------
INSERT INTO `tb_voyage_personnel` (`id`, `task_name`, `name`, `sex`, `birthdate`, `professional_title`, `employer`, `specialty`, `instruments`, `training`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '大无畏', '男', '2025-10-21', '达瓦伟大', '阿瓦达达娃', '啊我的娃', '挖的低洼', '大娃娃', '阿达瓦', '[]', 3, '2025-10-10 11:08:13', '2025-10-10 11:08:13');


-- ----------------------------
-- Table structure for tb_work_log
-- ----------------------------
DROP TABLE IF EXISTS `tb_work_log`;
CREATE TABLE `tb_work_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '航次任务名称',
  `survey_project` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '调查项目',
  `task_undertaking_unit` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务承担单位',
  `work_log` text COLLATE utf8mb4_unicode_ci COMMENT '工作日志',
  `record_time` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '记录时间',
  `spot_check_time` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '抽查时间',
  `remarks` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `attachments` text COLLATE utf8mb4_unicode_ci COMMENT '附件列表，存储JSON字符串',
  `user_id` int NOT NULL COMMENT '创建用户ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `tb_work_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of tb_work_log
-- ----------------------------
INSERT INTO `tb_work_log` (`id`, `task_name`, `survey_project`, `task_undertaking_unit`, `work_log`, `record_time`, `spot_check_time`, `remarks`, `attachments`, `user_id`, `create_time`, `update_time`) VALUES (1, '东海海洋调查', '挖地道', '哇哇的', '', '', '', '', '[]', 3, '2025-10-10 11:09:06', '2025-10-10 11:09:06');


SET FOREIGN_KEY_CHECKS = 1;