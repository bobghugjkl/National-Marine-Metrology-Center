-- 海洋调查现场质量监督管理系统 - 完整版数据库
-- 包含所有核心表 + 测试数据
-- 密码: WASDijkl15963

DROP DATABASE IF EXISTS marine_survey_db;
CREATE DATABASE marine_survey_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE marine_survey_db;

-- ==================== 基础表 ====================

-- 1. 用户表
CREATE TABLE tb_user (
    login_name VARCHAR(45) DEFAULT NULL,
    password VARCHAR(45) DEFAULT NULL,
    name VARCHAR(45) NOT NULL,
    sex VARCHAR(45) DEFAULT NULL,
    role VARCHAR(45) DEFAULT NULL,
    `desc` VARCHAR(45) DEFAULT NULL,
    permission VARCHAR(45) DEFAULT NULL,
    department VARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 任务信息表
CREATE TABLE tb_task_info (
    project VARCHAR(100) DEFAULT NULL,
    task_name VARCHAR(100) NOT NULL,
    task_code VARCHAR(100) DEFAULT NULL,
    undertake VARCHAR(100) DEFAULT NULL,
    participant VARCHAR(200) DEFAULT NULL,
    ship VARCHAR(45) DEFAULT NULL,
    leader VARCHAR(45) DEFAULT NULL,
    chief_scientist VARCHAR(45) DEFAULT NULL,
    superintendent VARCHAR(100) DEFAULT NULL,
    superintended VARCHAR(45) DEFAULT NULL,
    executiontime TEXT DEFAULT NULL,
    subject VARCHAR(45) DEFAULT NULL,
    PRIMARY KEY (task_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 基础人员主表
CREATE TABLE tb_base_master (
    name VARCHAR(40) DEFAULT NULL,
    sex VARCHAR(4) DEFAULT NULL,
    birthday DATE DEFAULT NULL,
    title VARCHAR(45) DEFAULT NULL,
    organization VARCHAR(45) DEFAULT NULL,
    major VARCHAR(45) DEFAULT NULL,
    phone VARCHAR(45) DEFAULT NULL,
    id_card_number VARCHAR(45) NOT NULL,
    band_card_number VARCHAR(45) DEFAULT NULL,
    opening_band VARCHAR(45) DEFAULT NULL,
    remark VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (id_card_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==================== 航前相关表 ====================

-- 4. 航前调查人员表
CREATE TABLE tb_base_hq_investigator (
    uniqueid VARCHAR(100) NOT NULL,
    task_name VARCHAR(100) DEFAULT NULL,
    task_code VARCHAR(100) DEFAULT NULL,
    ship VARCHAR(100) DEFAULT NULL,
    name VARCHAR(40) DEFAULT NULL,
    sex VARCHAR(4) DEFAULT NULL,
    birthday DATE DEFAULT NULL,
    title VARCHAR(40) DEFAULT NULL,
    organization VARCHAR(45) DEFAULT NULL,
    major VARCHAR(45) DEFAULT NULL,
    instrument VARCHAR(45) DEFAULT NULL,
    trainingdate VARCHAR(45) DEFAULT NULL,
    remark VARCHAR(100) DEFAULT NULL,
    preparer VARCHAR(45) DEFAULT NULL,
    verifier VARCHAR(45) DEFAULT NULL,
    create_date DATE DEFAULT NULL,
    attachment TEXT DEFAULT NULL,
    PRIMARY KEY (uniqueid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 航前设备表
CREATE TABLE tb_base_hq_device (
    uniqueid VARCHAR(100) NOT NULL,
    task_name VARCHAR(100) NOT NULL,
    type VARCHAR(45) DEFAULT NULL,
    name VARCHAR(100) DEFAULT NULL,
    id VARCHAR(45) DEFAULT NULL,
    model VARCHAR(45) DEFAULT NULL,
    traceability VARCHAR(45) DEFAULT NULL,
    checkdate DATE DEFAULT NULL,
    certificate_number VARCHAR(45) DEFAULT NULL,
    validity VARCHAR(45) DEFAULT NULL,
    verification_institutions VARCHAR(45) DEFAULT NULL,
    remark VARCHAR(100) DEFAULT NULL,
    attachment TEXT DEFAULT NULL,
    preparer VARCHAR(45) DEFAULT NULL,
    verifier VARCHAR(45) DEFAULT NULL,
    create_date DATE DEFAULT NULL,
    PRIMARY KEY (uniqueid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 航前质量监督检查记录表
CREATE TABLE tb_task_hqzljdjcjlb (
    task_name VARCHAR(100) NOT NULL,
    check_date TEXT DEFAULT NULL,
    superintendent VARCHAR(100) DEFAULT NULL,
    superintended VARCHAR(45) DEFAULT NULL,
    check_1 VARCHAR(200) DEFAULT NULL,
    check_1_problem VARCHAR(200) DEFAULT NULL,
    check_2 VARCHAR(200) DEFAULT NULL,
    check_2_problem VARCHAR(200) DEFAULT NULL,
    check_3 VARCHAR(200) DEFAULT NULL,
    check_3_problem VARCHAR(200) DEFAULT NULL,
    check_4 VARCHAR(200) DEFAULT NULL,
    check_4_problem VARCHAR(200) DEFAULT NULL,
    check_5 VARCHAR(200) DEFAULT NULL,
    check_5_problem VARCHAR(200) DEFAULT NULL,
    check_6 VARCHAR(200) DEFAULT NULL,
    check_6_problem VARCHAR(200) DEFAULT NULL,
    check_7 VARCHAR(200) DEFAULT NULL,
    check_7_problem VARCHAR(200) DEFAULT NULL,
    check_8 VARCHAR(200) DEFAULT NULL,
    check_8_problem VARCHAR(200) DEFAULT NULL,
    check_9 VARCHAR(200) DEFAULT NULL,
    check_9_problem VARCHAR(200) DEFAULT NULL,
    check_10 VARCHAR(200) DEFAULT NULL,
    check_10_problem VARCHAR(200) DEFAULT NULL,
    check_11 VARCHAR(200) DEFAULT NULL,
    check_11_problem VARCHAR(200) DEFAULT NULL,
    check_detail TEXT DEFAULT NULL,
    check_result TEXT DEFAULT NULL,
    chief_scientist_sign VARCHAR(45) DEFAULT NULL,
    check_leader_sign VARCHAR(45) DEFAULT NULL,
    chief_scientist_signdate DATE DEFAULT NULL,
    check_leader_signdate DATE DEFAULT NULL,
    create_date TEXT DEFAULT NULL,
    PRIMARY KEY (task_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==================== 航后相关表 ====================

-- 7. 航后调查人员表
CREATE TABLE tb_base_hz_investigator (
    uniqueid VARCHAR(100) NOT NULL,
    task_name VARCHAR(100) DEFAULT NULL,
    task_code VARCHAR(100) DEFAULT NULL,
    ship VARCHAR(100) DEFAULT NULL,
    name VARCHAR(40) DEFAULT NULL,
    sex VARCHAR(4) DEFAULT NULL,
    birthday DATE DEFAULT NULL,
    title VARCHAR(40) DEFAULT NULL,
    organization VARCHAR(45) DEFAULT NULL,
    major VARCHAR(45) DEFAULT NULL,
    instrument VARCHAR(45) DEFAULT NULL,
    trainingdate VARCHAR(45) DEFAULT NULL,
    remark VARCHAR(100) DEFAULT NULL,
    preparer VARCHAR(45) DEFAULT NULL,
    verifier VARCHAR(45) DEFAULT NULL,
    create_date DATE DEFAULT NULL,
    attachment TEXT DEFAULT NULL,
    PRIMARY KEY (uniqueid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. 航后设备表
CREATE TABLE tb_base_hz_device (
    uniqueid VARCHAR(100) NOT NULL,
    task_name VARCHAR(100) NOT NULL,
    type VARCHAR(45) DEFAULT NULL,
    name VARCHAR(100) DEFAULT NULL,
    id VARCHAR(45) DEFAULT NULL,
    model VARCHAR(45) DEFAULT NULL,
    traceability VARCHAR(45) DEFAULT NULL,
    checkdate DATE DEFAULT NULL,
    certificate_number VARCHAR(45) DEFAULT NULL,
    validity VARCHAR(45) DEFAULT NULL,
    verification_institutions VARCHAR(45) DEFAULT NULL,
    remark VARCHAR(100) DEFAULT NULL,
    attachment TEXT DEFAULT NULL,
    preparer VARCHAR(45) DEFAULT NULL,
    verifier VARCHAR(45) DEFAULT NULL,
    create_date DATE DEFAULT NULL,
    PRIMARY KEY (uniqueid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==================== 质量检查表 ====================

-- 9. 现场质量监督检查表
CREATE TABLE tb_task_sczljdjcb (
    task_name VARCHAR(100) NOT NULL,
    check_date TEXT DEFAULT NULL,
    superintendent VARCHAR(100) DEFAULT NULL,
    superintended VARCHAR(100) DEFAULT NULL,
    check_1 VARCHAR(200) DEFAULT NULL,
    check_1_problem VARCHAR(200) DEFAULT NULL,
    check_2 VARCHAR(200) DEFAULT NULL,
    check_2_problem VARCHAR(200) DEFAULT NULL,
    check_3 VARCHAR(200) DEFAULT NULL,
    check_3_problem VARCHAR(200) DEFAULT NULL,
    check_4 VARCHAR(200) DEFAULT NULL,
    check_4_problem VARCHAR(200) DEFAULT NULL,
    check_5 VARCHAR(200) DEFAULT NULL,
    check_5_problem VARCHAR(200) DEFAULT NULL,
    check_6 VARCHAR(200) DEFAULT NULL,
    check_6_problem VARCHAR(200) DEFAULT NULL,
    check_7 VARCHAR(200) DEFAULT NULL,
    check_7_problem VARCHAR(200) DEFAULT NULL,
    check_8 VARCHAR(200) DEFAULT NULL,
    check_8_problem VARCHAR(200) DEFAULT NULL,
    check_9 VARCHAR(200) DEFAULT NULL,
    check_9_problem VARCHAR(200) DEFAULT NULL,
    check_10 VARCHAR(200) DEFAULT NULL,
    check_10_problem VARCHAR(200) DEFAULT NULL,
    check_11 VARCHAR(200) DEFAULT NULL,
    check_11_problem VARCHAR(200) DEFAULT NULL,
    check_12 VARCHAR(200) DEFAULT NULL,
    check_12_problem VARCHAR(200) DEFAULT NULL,
    chief_scientist_sign VARCHAR(45) DEFAULT NULL,
    check_leader_sign VARCHAR(45) DEFAULT NULL,
    chief_scientist_signdate DATE DEFAULT NULL,
    check_leader_signdate DATE DEFAULT NULL,
    create_date TEXT DEFAULT NULL,
    PRIMARY KEY (task_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. 质量评估表
CREATE TABLE tb_task_zlpgb (
    task_name VARCHAR(100) NOT NULL,
    evaluated_unit VARCHAR(200) DEFAULT NULL,
    check_1_grade INT DEFAULT NULL,
    check_1_problem VARCHAR(200) DEFAULT NULL,
    check_2_grade INT DEFAULT NULL,
    check_2_problem VARCHAR(200) DEFAULT NULL,
    check_3_grade INT DEFAULT NULL,
    check_3_problem VARCHAR(200) DEFAULT NULL,
    check_4_grade INT DEFAULT NULL,
    check_4_problem VARCHAR(200) DEFAULT NULL,
    check_5_grade INT DEFAULT NULL,
    check_5_problem VARCHAR(200) DEFAULT NULL,
    check_6_grade INT DEFAULT NULL,
    check_6_problem VARCHAR(200) DEFAULT NULL,
    check_7_grade INT DEFAULT NULL,
    check_7_problem VARCHAR(200) DEFAULT NULL,
    check_8_grade INT DEFAULT NULL,
    check_8_problem VARCHAR(200) DEFAULT NULL,
    check_9_grade INT DEFAULT NULL,
    check_9_problem VARCHAR(200) DEFAULT NULL,
    check_10_grade INT DEFAULT NULL,
    check_10_problem VARCHAR(200) DEFAULT NULL,
    check_11_grade INT DEFAULT NULL,
    check_11_problem VARCHAR(200) DEFAULT NULL,
    check_12_grade INT DEFAULT NULL,
    check_12_problem VARCHAR(200) DEFAULT NULL,
    check_13_grade INT DEFAULT NULL,
    check_13_problem VARCHAR(200) DEFAULT NULL,
    evaluated_sign VARCHAR(45) DEFAULT NULL,
    evaluator_sign VARCHAR(45) DEFAULT NULL,
    evaluated_signdate DATE DEFAULT NULL,
    evaluator_signdate DATE DEFAULT NULL,
    create_date TEXT DEFAULT NULL,
    PRIMARY KEY (task_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==================== 插入测试数据 ====================

-- 用户数据
INSERT INTO tb_user (name, login_name, password, role, department) VALUES
('admin', 'admin', '123456', '管理员', '系统管理部'),
('张三', 'zhangsan', '123456', '普通用户', '业务部门'),
('李四', 'lisi', '123456', '普通用户', '业务部门'),
('王五', 'wangwu', '123456', '部门经理', '管理部门');

-- 任务数据
INSERT INTO tb_task_info (project, task_name, task_code, undertake, participant, ship, leader, chief_scientist, superintendent, executiontime, subject) VALUES
('海洋调查项目', '海洋调查任务001', 'TASK001', '海洋研究所', '张三,李四', '海洋号', '张主任', '李教授', '王监督', '2024年1月至6月', '海洋环境监测'),
('海洋生物调查', '海洋生物任务002', 'TASK002', '海洋中心', '王五', '生物号', '李主任', '陈教授', '孙监督', '2024年3月至8月', '海洋生物多样性');

-- 基础人员数据
INSERT INTO tb_base_master (name, sex, birthday, title, organization, phone, id_card_number) VALUES
('张三', '男', '1990-01-01', '工程师', '海洋研究所', '13800138001', '110101199001011234'),
('李四', '女', '1985-05-15', '研究员', '海洋中心', '13800138002', '110101198505151234'),
('王五', '男', '1988-08-20', '助理研究员', '海洋实验室', '13800138003', '110101198808201234'),
('赵六', '女', '1992-03-10', '技术员', '海洋监测站', '13800138004', '110101199203101234');
