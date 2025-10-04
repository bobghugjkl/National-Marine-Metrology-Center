-- 修正后的 MySQL SQL 文件
-- 从 SQLite 数据库转换而来，手动修正了数据类型问题
-- 生成时间: 2025-09-30

-- 删除已存在的数据库（可选）
DROP DATABASE IF EXISTS marine_survey_db;
CREATE DATABASE marine_survey_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE marine_survey_db;

-- 用户表
CREATE TABLE `tb_user` (
    `login_name` VARCHAR(45) DEFAULT NULL,
    `password` VARCHAR(45) DEFAULT NULL,
    `name` VARCHAR(45) NOT NULL,
    `sex` VARCHAR(45) DEFAULT NULL,
    `role` VARCHAR(45) DEFAULT NULL,
    `desc` VARCHAR(45) DEFAULT NULL,
    `permission` VARCHAR(45) DEFAULT NULL,
    `department` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 任务信息表
CREATE TABLE `tb_task_info` (
    `project` VARCHAR(100) DEFAULT NULL,
    `task_name` VARCHAR(100) NOT NULL,
    `task_code` VARCHAR(100) DEFAULT NULL,
    `undertake` VARCHAR(100) DEFAULT NULL,
    `participant` VARCHAR(200) DEFAULT NULL,
    `ship` VARCHAR(45) DEFAULT NULL,
    `leader` VARCHAR(45) DEFAULT NULL,
    `chief_scientist` VARCHAR(45) DEFAULT NULL,
    `superintendent` VARCHAR(100) DEFAULT NULL,
    `superintended` VARCHAR(45) DEFAULT NULL,
    `executiontime` TEXT DEFAULT NULL,
    `subject` VARCHAR(45) DEFAULT NULL,
    PRIMARY KEY (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 基础主表（修正版）
CREATE TABLE `tb_base_master` (
    `name` VARCHAR(40) DEFAULT NULL,
    `sex` VARCHAR(4) DEFAULT NULL,
    `birthday` DATE DEFAULT NULL,
    `title` VARCHAR(45) DEFAULT NULL,
    `organization` VARCHAR(45) DEFAULT NULL,
    `major` VARCHAR(45) DEFAULT NULL,
    `phone` VARCHAR(45) DEFAULT NULL,
    `id_card_number` VARCHAR(45) NOT NULL,
    `band_card_number` VARCHAR(45) DEFAULT NULL,
    `opening_band` VARCHAR(45) DEFAULT NULL,
    `remark` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`id_card_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 航前调查人员表
CREATE TABLE `tb_base_hq_investigator` (
    `uniqueid` VARCHAR(100) NOT NULL,
    `task_name` VARCHAR(100) DEFAULT NULL,
    `task_code` VARCHAR(100) DEFAULT NULL,
    `ship` VARCHAR(100) DEFAULT NULL,
    `name` VARCHAR(40) DEFAULT NULL,
    `sex` VARCHAR(4) DEFAULT NULL,
    `birthday` DATE DEFAULT NULL,
    `title` VARCHAR(40) DEFAULT NULL,
    `organization` VARCHAR(45) DEFAULT NULL,
    `major` VARCHAR(45) DEFAULT NULL,
    `instrument` VARCHAR(45) DEFAULT NULL,
    `trainingdate` VARCHAR(45) DEFAULT NULL,
    `remark` VARCHAR(100) DEFAULT NULL,
    `preparer` VARCHAR(45) DEFAULT NULL,
    `verifier` VARCHAR(45) DEFAULT NULL,
    `create_date` DATE DEFAULT NULL,
    `attachment` TEXT DEFAULT NULL,
    PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 航前设备表
CREATE TABLE `tb_base_hq_device` (
    `uniqueid` VARCHAR(100) NOT NULL,
    `task_name` VARCHAR(100) NOT NULL,
    `type` VARCHAR(45) DEFAULT NULL,
    `name` VARCHAR(100) DEFAULT NULL,
    `id` VARCHAR(45) DEFAULT NULL,
    `model` VARCHAR(45) DEFAULT NULL,
    `traceability` VARCHAR(45) DEFAULT NULL,
    `checkdate` DATE DEFAULT NULL,
    `certificate_number` VARCHAR(45) DEFAULT NULL,
    `validity` VARCHAR(45) DEFAULT NULL,
    `verification_institutions` VARCHAR(45) DEFAULT NULL,
    `remark` VARCHAR(100) DEFAULT NULL,
    `attachment` TEXT DEFAULT NULL,
    `preparer` VARCHAR(45) DEFAULT NULL,
    `verifier` VARCHAR(45) DEFAULT NULL,
    `create_date` DATE DEFAULT NULL,
    PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 航后调查人员表
CREATE TABLE `tb_base_hz_investigator` (
    `uniqueid` VARCHAR(100) NOT NULL,
    `task_name` VARCHAR(100) DEFAULT NULL,
    `task_code` VARCHAR(100) DEFAULT NULL,
    `ship` VARCHAR(100) DEFAULT NULL,
    `name` VARCHAR(40) DEFAULT NULL,
    `sex` VARCHAR(4) DEFAULT NULL,
    `birthday` DATE DEFAULT NULL,
    `title` VARCHAR(40) DEFAULT NULL,
    `organization` VARCHAR(45) DEFAULT NULL,
    `major` VARCHAR(45) DEFAULT NULL,
    `instrument` VARCHAR(45) DEFAULT NULL,
    `trainingdate` VARCHAR(45) DEFAULT NULL,
    `remark` VARCHAR(100) DEFAULT NULL,
    `preparer` VARCHAR(45) DEFAULT NULL,
    `verifier` VARCHAR(45) DEFAULT NULL,
    `create_date` DATE DEFAULT NULL,
    `attachment` TEXT DEFAULT NULL,
    PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 航后设备表
CREATE TABLE `tb_base_hz_device` (
    `uniqueid` VARCHAR(100) NOT NULL,
    `task_name` VARCHAR(100) NOT NULL,
    `type` VARCHAR(45) DEFAULT NULL,
    `name` VARCHAR(100) DEFAULT NULL,
    `id` VARCHAR(45) DEFAULT NULL,
    `model` VARCHAR(45) DEFAULT NULL,
    `traceability` VARCHAR(45) DEFAULT NULL,
    `checkdate` DATE DEFAULT NULL,
    `certificate_number` VARCHAR(45) DEFAULT NULL,
    `validity` VARCHAR(45) DEFAULT NULL,
    `verification_institutions` VARCHAR(45) DEFAULT NULL,
    `remark` VARCHAR(100) DEFAULT NULL,
    `attachment` TEXT DEFAULT NULL,
    `preparer` VARCHAR(45) DEFAULT NULL,
    `verifier` VARCHAR(45) DEFAULT NULL,
    `create_date` DATE DEFAULT NULL,
    PRIMARY KEY (`uniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入测试数据
INSERT INTO `tb_user` (`name`, `login_name`, `password`, `role`, `department`) VALUES
('admin', 'admin', '123456', '管理员', '系统管理部'),
('user1', 'user1', '123456', '普通用户', '业务部门');

INSERT INTO `tb_base_master` (`name`, `sex`, `birthday`, `title`, `organization`, `id_card_number`) VALUES
('张三', '男', '1990-01-01', '工程师', '海洋研究所', '110101199001011234'),
('李四', '女', '1985-05-15', '研究员', '海洋中心', '110101198505151234');
