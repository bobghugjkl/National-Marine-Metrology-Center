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
INSERT INTO `tb_task_hqzljdjcjlb` (`task_name`, `check_date`, `superintendent`, `superintended`, `check_1`, `check_1_problem`, `check_2`, `check_2_problem`, `check_3`, `check_3_problem`, `check_4`, `check_4_problem`, `check_5`, `check_5_problem`, `check_6`, `check_6_problem`, `check_7`, `check_7_problem`, `check_8`, `check_8_problem`, `check_9`, `check_9_problem`, `check_10`, `check_10_problem`, `check_11`, `check_11_problem`, `check_detail`, `check_result`, `chief_scientist_sign`, `check_leader_sign`, `chief_scientist_signdate`, `check_leader_signdate`, `create_date`, `user_id`) VALUES ('东海海洋调查', '111', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '111', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3);
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
INSERT INTO `tb_task_info` (`project`, `task_name`, `task_code`, `undertake`, `participant`, `ship`, `leader`, `chief_scientist`, `superintendent`, `superintended`, `executiontime`, `subject`, `user_id`) VALUES ('海洋资源调查专项', '东海海洋调查', 'HY20250011', '国家海洋标准计量中心', '', '向阳红01', '张主任', '', '', '', '2025-01-15 至 2025-02-20', '海洋地质', 3);
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of tb_user
-- ----------------------------
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (1, 'test', '123456', '111', NULL, '111', NULL, NULL, '111');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (2, '12', '12', '12', '12', '12', NULL, NULL, '12');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (3, '123', '123456', '123', NULL, '普通用户', NULL, NULL, '未分配');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (4, 'admin', '123456', 'admin', NULL, 'super_admin', NULL, NULL, 'IT_Department');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (5, 'newuser', '123456', 'newuser', NULL, '普通用户', NULL, NULL, '未分配');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (6, 'testlogin', '123', 'TestUser', NULL, 'user', NULL, NULL, 'IT');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (7, '娴嬭瘯鐢ㄦ埛', '123456', '娴嬭瘯鐢ㄦ埛', NULL, '普通用户', NULL, NULL, '未分配');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (8, 'zhangsan', '123456', '张三', NULL, '普通用户', NULL, NULL, '业务部门');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (9, 'lisi', '123456', '李四', NULL, '普通用户', NULL, NULL, '业务部门');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (10, 'wangwu', '123456', '王五', NULL, '部门经理', NULL, NULL, '管理部门');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (11, '鐜嬩簲', '123456', '鐜嬩簲', NULL, '普通用户', NULL, NULL, '未分配');
INSERT INTO `tb_user` (`id`, `login_name`, `password`, `name`, `sex`, `role`, `desc`, `permission`, `department`) VALUES (12, '1234', '123456', '1234', '未知', '普通用户', '', '基础权限', '未分配');


SET FOREIGN_KEY_CHECKS = 1;