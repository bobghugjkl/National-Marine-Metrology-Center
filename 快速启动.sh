#!/bin/bash

echo "================================================"
echo "🌊 海洋调查管理系统 - 快速启动脚本"
echo "================================================"
echo

echo "[1/6] 检查环境..."
echo "检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js 16.x 或更高版本"
    exit 1
fi
echo "✅ Node.js 已安装"

echo "检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 未安装，请先安装 Python 3.11 或更高版本"
    exit 1
fi
echo "✅ Python 已安装"

echo "检查 MySQL..."
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL 未安装，请先安装 MySQL 8.0 或更高版本"
    exit 1
fi
echo "✅ MySQL 已安装"

echo
echo "[2/6] 导入数据库..."
echo "正在导入数据库结构和数据..."
mysql -u root -p < marine_survey_db_complete_final.sql
if [ $? -ne 0 ]; then
    echo "❌ 数据库导入失败，请检查 MySQL 连接和密码"
    exit 1
fi
echo "✅ 数据库导入成功"

echo
echo "[3/6] 安装后端依赖..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 后端依赖安装失败"
    exit 1
fi
echo "✅ 后端依赖安装成功"

echo
echo "[4/6] 启动后端服务..."
echo "正在启动后端服务..."
python3 app.py &
BACKEND_PID=$!
sleep 3
echo "✅ 后端服务已启动 (http://localhost:5000) PID: $BACKEND_PID"

echo
echo "[5/6] 安装前端依赖..."
cd ..
npm install
if [ $? -ne 0 ]; then
    echo "❌ 前端依赖安装失败"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo "✅ 前端依赖安装成功"

echo
echo "[6/6] 启动前端服务..."
echo "正在启动前端服务..."
npm run dev &
FRONTEND_PID=$!
sleep 3
echo "✅ 前端服务已启动 (http://localhost:5173) PID: $FRONTEND_PID"

echo
echo "================================================"
echo "🎉 系统启动完成！"
echo "================================================"
echo
echo "📱 访问地址："
echo "   前端: http://localhost:5173"
echo "   后端: http://localhost:5000"
echo
echo "🔑 测试账号："
echo "   用户名: test    密码: 123456"
echo "   用户名: admin   密码: 123456"
echo "   用户名: 123     密码: 123456"
echo
echo "📚 详细说明请查看: 部署指南.md"
echo
echo "按 Ctrl+C 停止服务..."
echo

# 等待用户中断
trap 'echo "正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT
wait
