#!/bin/bash

# 启动Django后端服务器
echo "Starting Django backend server..."

# 检查数据库迁移
echo "Checking database migrations..."
python3 manage.py migrate

# 创建超级用户（如果不存在）
echo "Creating superuser if not exists..."
python3 manage.py shell -c "
from django.contrib.auth.models import User
from api.models import UserProfile
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    UserProfile.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})
    print('Admin user created')
else:
    print('Admin user already exists')
"

# 创建示例题目（如果不存在）
echo "Creating sample questions if not exists..."
python3 manage.py create_sample_questions

# 启动服务器
echo "Starting Django development server on http://localhost:8000"
python3 manage.py runserver 0.0.0.0:8000