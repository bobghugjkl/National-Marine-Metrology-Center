@echo off
chcp 65001 >nul
echo ================================================
echo 🌊 海洋调查管理系统 - 快速启动脚本
echo ================================================
echo.

echo [1/6] 检查环境...
echo 检查 Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js 16.x 或更高版本
    pause
    exit /b 1
)
echo ✅ Node.js 已安装

echo 检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装，请先安装 Python 3.11 或更高版本
    pause
    exit /b 1
)
echo ✅ Python 已安装

echo 检查 MySQL...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ MySQL 未安装，请先安装 MySQL 8.0 或更高版本
    pause
    exit /b 1
)
echo ✅ MySQL 已安装

echo.
echo [2/6] 导入数据库...
echo 正在导入数据库结构和数据...
mysql -u root -p < marine_survey_db_complete_final.sql
if %errorlevel% neq 0 (
    echo ❌ 数据库导入失败，请检查 MySQL 连接和密码
    pause
    exit /b 1
)
echo ✅ 数据库导入成功

echo.
echo [3/6] 安装后端依赖...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 后端依赖安装失败
    pause
    exit /b 1
)
echo ✅ 后端依赖安装成功

echo.
echo [4/6] 启动后端服务...
echo 正在启动后端服务...
start "后端服务" cmd /k "python app.py"
timeout /t 3 /nobreak >nul
echo ✅ 后端服务已启动 (http://localhost:5000)

echo.
echo [5/6] 安装前端依赖...
cd ..
npm install
if %errorlevel% neq 0 (
    echo ❌ 前端依赖安装失败
    pause
    exit /b 1
)
echo ✅ 前端依赖安装成功

echo.
echo [6/6] 启动前端服务...
echo 正在启动前端服务...
start "前端服务" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul
echo ✅ 前端服务已启动 (http://localhost:5173)

echo.
echo ================================================
echo 🎉 系统启动完成！
echo ================================================
echo.
echo 📱 访问地址：
echo    前端: http://localhost:5173
echo    后端: http://localhost:5000
echo.
echo 🔑 测试账号：
echo    用户名: test    密码: 123456
echo    用户名: admin   密码: 123456
echo    用户名: 123     密码: 123456
echo.
echo 📚 详细说明请查看: 部署指南.md
echo.
echo 按任意键退出...
pause >nul
