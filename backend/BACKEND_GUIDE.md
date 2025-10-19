# Django后端使用指南

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py init_data
```

### 3. 启动服务器

**方式一：使用启动脚本**
```bash
./start.sh
```

**方式二：手动启动**
```bash
python manage.py runserver 0.0.0.0:8000
```

### 4. 访问系统

- API地址: http://localhost:8000/api/
- 管理后台: http://localhost:8000/admin/
- 默认账户:
  - 管理员: `admin` / `admin`
  - 用户: `user` / `password`

## 项目结构

```
backend/
├── exam_system/          # Django项目配置
│   ├── settings.py       # 项目设置
│   ├── urls.py          # 主URL配置
│   ├── wsgi.py          # WSGI配置
│   └── asgi.py          # ASGI配置
├── api/                 # API应用
│   ├── models.py        # 数据模型
│   ├── serializers.py   # 序列化器
│   ├── views.py         # 视图
│   ├── urls.py          # URL路由
│   ├── permissions.py   # 权限类
│   ├── admin.py         # 管理后台配置
│   └── management/      # 管理命令
│       └── commands/
│           └── init_data.py  # 初始化数据命令
├── manage.py            # Django管理脚本
├── requirements.txt     # Python依赖
├── start.sh            # 启动脚本
├── README.md           # 完整文档
└── .env.example        # 环境变量示例

```

## API端点总览

### 认证相关
- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `GET/PUT /api/auth/profile/` - 获取/更新个人资料
- `POST /api/auth/change-password/` - 修改密码

### 题目管理
- `GET /api/questions/` - 获取题目列表（支持搜索和筛选）
- `GET /api/questions/{id}/` - 获取单个题目
- `POST /api/questions/` - 创建题目（管理员）
- `PUT /api/questions/{id}/` - 更新题目（管理员）
- `DELETE /api/questions/{id}/` - 删除题目（管理员）
- `GET /api/questions/random/` - 获取随机题目
- `GET /api/questions/sequential/` - 获取顺序题目
- `POST /api/questions/import_questions/` - 批量导入（管理员）

### 考试管理
- `POST /api/exams/` - 创建考试
- `GET /api/exams/{id}/` - 获取考试详情
- `POST /api/exams/{id}/submit/` - 提交考试答案
- `GET /api/exams/{id}/result/` - 获取考试结果
- `GET /api/exams/history/` - 获取考试历史

### 练习记录
- `POST /api/practice/` - 创建练习记录
- `GET /api/practice/` - 获取练习记录列表

### 用户管理（管理员）
- `GET /api/users/` - 获取用户列表
- `GET /api/users/{id}/` - 获取用户详情
- `PUT /api/users/{id}/` - 更新用户
- `DELETE /api/users/{id}/` - 删除用户
- `GET /api/users/{id}/stats/` - 获取用户统计

### 统计数据
- `GET /api/stats/` - 获取当前用户统计

## 数据模型说明

### User（用户）
扩展了Django默认用户模型，增加了：
- `role`: 用户角色（user/admin）
- `phone`: 手机号
- `avatar`: 头像

### Question（题目）
- `type`: 题目类型（single单选/judge判断）
- `difficulty`: 难度（easy/medium/hard）
- `category`: 分类
- `question`: 题目内容
- `options`: 选项数组（JSON格式）
- `correct_answer`: 正确答案索引
- `explanation`: 答案解析

### Exam（考试）
- `user`: 考生外键
- `status`: 状态（in_progress/completed）
- `score`: 分数
- `passed`: 是否通过（90分及格）
- `total_questions`: 题目总数
- `correct_count`: 正确数量
- `wrong_count`: 错误数量
- `duration`: 考试时长（秒）

### ExamQuestion（考试题目关联）
考试和题目的多对多关系中间表：
- `exam`: 考试外键
- `question`: 题目外键
- `user_answer`: 用户答案
- `is_correct`: 是否正确
- `order`: 题目顺序

### PracticeRecord（练习记录）
- `user`: 用户外键
- `question`: 题目外键
- `user_answer`: 用户答案
- `is_correct`: 是否正确
- `practice_type`: 练习类型（sequential/random）

### UserStats（用户统计）
- `user`: 用户外键（一对一）
- `total_exams`: 考试总数
- `passed_exams`: 通过考试数
- `total_practice`: 练习总数
- `correct_practice`: 练习正确数
- `study_time`: 学习时长
- `practice_accuracy`: 练习正确率（属性）
- `exam_pass_rate`: 考试通过率（属性）

## 常用管理命令

### 创建超级管理员
```bash
python manage.py createsuperuser
```

### 初始化示例数据
```bash
python manage.py init_data
```

### 重置数据库
```bash
rm db.sqlite3
python manage.py migrate
python manage.py init_data
```

### 收集静态文件
```bash
python manage.py collectstatic
```

### 运行测试
```bash
python manage.py test
```

## 权限说明

系统使用JWT Token进行认证：

1. **AllowAny**: 注册、登录接口
2. **IsAuthenticated**: 需要登录的接口（大部分接口）
3. **IsAdminUser**: 仅管理员可访问（题目管理、用户管理）

请求时需在Header中添加：
```
Authorization: Bearer <token>
```

## 题目导入格式

### Excel/CSV 格式

表头必须包含以下字段：
- type: 题目类型（single/judge）
- difficulty: 难度（easy/medium/hard）
- category: 分类
- question: 题目内容
- options: JSON数组字符串，如 `["选项A","选项B"]`
- correct_answer: 正确答案索引（数字）
- explanation: 答案解析

### JSON 格式

```json
[
  {
    "type": "single",
    "difficulty": "easy",
    "category": "交通信号",
    "question": "红灯表示什么？",
    "options": ["禁止通行", "准许通行", "警示", "减速"],
    "correct_answer": 0,
    "explanation": "红灯表示禁止通行"
  }
]
```

## 配置说明

### 开发环境
默认配置已经适用于开发环境：
- DEBUG = True
- SQLite数据库
- 允许所有主机访问
- CORS允许localhost:3000

### 生产环境

需要修改 `settings.py`：

1. **安全设置**
```python
SECRET_KEY = '使用环境变量或生成新的密钥'
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
```

2. **数据库**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **CORS设置**
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]
```

4. **静态文件**
```bash
python manage.py collectstatic
```

## 部署指南

### 使用Gunicorn

1. 安装Gunicorn
```bash
pip install gunicorn
```

2. 启动服务
```bash
gunicorn exam_system.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 使用Nginx反向代理

配置示例 `/etc/nginx/sites-available/exam_api`:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/backend/staticfiles/;
    }

    location /media/ {
        alias /path/to/backend/media/;
    }
}
```

### 使用Systemd管理服务

创建服务文件 `/etc/systemd/system/exam_api.service`:
```ini
[Unit]
Description=Exam System API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 exam_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl start exam_api
sudo systemctl enable exam_api
```

## 故障排查

### 问题：No module named 'django'
**解决**: 确保已安装依赖 `pip install -r requirements.txt`

### 问题：数据库迁移失败
**解决**: 
```bash
python manage.py makemigrations api
python manage.py migrate
```

### 问题：CORS错误
**解决**: 检查 `settings.py` 中的 `CORS_ALLOWED_ORIGINS` 配置

### 问题：Token认证失败
**解决**: 
1. 检查Header格式：`Authorization: Bearer <token>`
2. 确认token未过期
3. 检查JWT配置

## 性能优化建议

1. **使用缓存**
```python
# 安装Redis
pip install django-redis

# settings.py 配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **数据库优化**
- 使用 `select_related()` 和 `prefetch_related()`
- 添加数据库索引
- 使用PostgreSQL替代SQLite

3. **静态文件CDN**
- 使用CDN托管静态文件
- 配置 `STATIC_URL` 和 `MEDIA_URL`

## 监控和日志

### 配置日志
在 `settings.py` 中添加：
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/path/to/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 安全建议

1. ✅ 使用强密码和安全的SECRET_KEY
2. ✅ 启用HTTPS
3. ✅ 设置合理的CORS策略
4. ✅ 定期更新依赖包
5. ✅ 使用环境变量管理敏感信息
6. ✅ 限制文件上传大小和类型
7. ✅ 启用Django安全中间件

## 技术支持

如有问题，请查看：
1. Django官方文档: https://docs.djangoproject.com/
2. DRF文档: https://www.django-rest-framework.org/
3. 项目README.md

## License

MIT
