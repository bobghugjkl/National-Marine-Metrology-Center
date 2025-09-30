-- 1. 给 tb_user 表添加自增主键 id
-- 首先检查是否已有 id 列
ALTER TABLE tb_user ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;

-- 如果上面的命令失败（因为已有主键），先删除主键，再添加
-- ALTER TABLE tb_user DROP PRIMARY KEY;
-- ALTER TABLE tb_user ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
-- ALTER TABLE tb_user MODIFY COLUMN name VARCHAR(45) NOT NULL UNIQUE;

-- 2. 给 tb_task_info 表添加 user_id 列
ALTER TABLE tb_task_info ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建任务的用户ID';

-- 3. 给 tb_task_hqzljdjcjlb 表添加 user_id 列
ALTER TABLE tb_task_hqzljdjcjlb ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建检查记录的用户ID';

-- 4. 给 tb_base_master 表添加 user_id 列（如果需要）
ALTER TABLE tb_base_master ADD COLUMN user_id INT DEFAULT 3 COMMENT '创建人员信息的用户ID';

-- 5. 更新现有数据，将所有现有记录关联到 id=3 的用户
UPDATE tb_task_info SET user_id = 3 WHERE user_id IS NULL;
UPDATE tb_task_hqzljdjcjlb SET user_id = 3 WHERE user_id IS NULL;
UPDATE tb_base_master SET user_id = 3 WHERE user_id IS NULL;
