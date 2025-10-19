#!/bin/bash

# 启动脚本

echo "正在启动驾照理论模拟考试系统后端..."

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "提示：建议在虚拟环境中运行"
fi

# 检查依赖
echo "检查依赖..."
python3 -c "import django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 运行迁移
echo "运行数据库迁移..."
python3 manage.py migrate --no-input

# 启动开发服务器
echo "启动开发服务器..."
echo "访问地址: http://localhost:8000"
echo "管理后台: http://localhost:8000/admin"
echo "API文档: 查看 README.md"
echo ""
echo "默认账户:"
echo "  管理员: admin / admin"
echo "  用户: user / password"
echo ""

python3 manage.py runserver 0.0.0.0:8000
