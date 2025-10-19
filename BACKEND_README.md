# 驾照理论模拟考试系统 - Django后端

这是一个基于Django REST Framework的驾照理论模拟考试系统后端API，为前端Vue.js应用提供数据支持。

## 功能特性

### 用户认证
- ✅ 用户注册（邮箱、用户名、密码）
- ✅ 用户登录（JWT认证）
- ✅ 用户登出
- ✅ 个人资料管理
- ✅ 密码修改

### 题目管理
- ✅ 题目CRUD操作
- ✅ 题目搜索和筛选
- ✅ 随机题目获取
- ✅ 顺序题目获取
- ✅ 题目批量导入（Excel、CSV、JSON）

### 考试功能
- ✅ 创建模拟考试
- ✅ 提交考试答案
- ✅ 自动评分
- ✅ 考试结果查看
- ✅ 考试历史记录

### 练习功能
- ✅ 顺序练习
- ✅ 随机练习
- ✅ 练习会话管理

### 管理员功能
- ✅ 用户管理
- ✅ 题库管理
- ✅ 题目导入
- ✅ 用户统计查看

## 技术栈

- **框架**: Django 5.2.7
- **API**: Django REST Framework 3.16.1
- **认证**: JWT (djangorestframework-simplejwt)
- **CORS**: django-cors-headers
- **数据库**: SQLite (开发环境)
- **文件处理**: pandas, openpyxl

## 项目结构

```
driver_license_backend/
├── api/                    # 主应用
│   ├── management/         # 管理命令
│   │   └── commands/
│   │       └── create_sample_questions.py
│   ├── migrations/         # 数据库迁移
│   ├── admin.py           # 后台管理
│   ├── models.py          # 数据模型
│   ├── serializers.py     # 序列化器
│   ├── urls.py           # URL配置
│   └── views.py          # 视图
├── driver_license_backend/ # 项目配置
│   ├── settings.py        # 设置
│   └── urls.py           # 主URL配置
├── media/                 # 媒体文件
├── staticfiles/           # 静态文件
├── db.sqlite3            # 数据库
├── manage.py             # 管理脚本
├── requirements.txt      # 依赖包
└── start_backend.sh      # 启动脚本
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py migrate
```

### 3. 创建超级用户

```bash
python manage.py createsuperuser
```

### 4. 创建示例数据

```bash
python manage.py create_sample_questions
```

### 5. 启动服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

或者使用启动脚本：

```bash
./start_backend.sh
```

服务器将在 `http://localhost:8000` 启动。

## API接口文档

### 认证接口

#### 用户注册
```
POST /api/auth/register/
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "password_confirm": "string",
    "first_name": "string",
    "last_name": "string"
}
```

#### 用户登录
```
POST /api/auth/login/
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}

Response:
{
    "token": "string",
    "refresh": "string",
    "user": {
        "id": 1,
        "username": "string",
        "email": "string",
        "role": "user|admin"
    }
}
```

#### 用户登出
```
POST /api/auth/logout/
Authorization: Bearer <token>
Content-Type: application/json

{
    "refresh": "string"
}
```

#### 获取/更新个人资料
```
GET /api/auth/profile/
PUT /api/auth/profile/
Authorization: Bearer <token>
```

#### 修改密码
```
POST /api/auth/change-password/
Authorization: Bearer <token>
Content-Type: application/json

{
    "old_password": "string",
    "new_password": "string",
    "new_password_confirm": "string"
}
```

### 题目接口

#### 获取题目列表
```
GET /api/questions/
Authorization: Bearer <token>
Query Parameters:
- search: 搜索关键词
- type: 题目类型 (single|judge)
- difficulty: 难度 (easy|medium|hard)
- page: 页码
```

#### 获取单个题目
```
GET /api/questions/{id}/
Authorization: Bearer <token>
```

#### 创建题目
```
POST /api/questions/
Authorization: Bearer <token>
Content-Type: application/json

{
    "type": "single|judge",
    "difficulty": "easy|medium|hard",
    "question": "string",
    "options": ["A.选项1", "B.选项2", "C.选项3", "D.选项4"],
    "correct_answer": 0,
    "explanation": "string"
}
```

#### 更新题目
```
PUT /api/questions/{id}/
Authorization: Bearer <token>
```

#### 删除题目
```
DELETE /api/questions/{id}/
Authorization: Bearer <token>
```

#### 获取随机题目
```
GET /api/questions/random/
Authorization: Bearer <token>
Query Parameters:
- count: 题目数量 (默认10)
```

#### 获取顺序题目
```
GET /api/questions/sequential/
Authorization: Bearer <token>
Query Parameters:
- offset: 偏移量 (默认0)
- limit: 限制数量 (默认10)
```

#### 批量导入题目
```
POST /api/questions/import/
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: 文件 (支持Excel、CSV、JSON)
```

### 考试接口

#### 创建考试
```
POST /api/exams/
Authorization: Bearer <token>
Content-Type: application/json

{
    "time_limit": 45
}
```

#### 获取考试详情
```
GET /api/exams/{id}/
Authorization: Bearer <token>
```

#### 提交考试
```
POST /api/exams/{id}/submit/
Authorization: Bearer <token>
Content-Type: application/json

{
    "answers": {
        "question_id": answer_index,
        ...
    }
}
```

#### 获取考试结果
```
GET /api/exams/{id}/result/
Authorization: Bearer <token>
```

#### 获取考试历史
```
GET /api/exams/history/
Authorization: Bearer <token>
```

### 练习接口

#### 创建练习会话
```
POST /api/practice/
Authorization: Bearer <token>
Content-Type: application/json

{
    "practice_type": "sequential|random"
}
```

#### 获取练习会话详情
```
GET /api/practice/{id}/
Authorization: Bearer <token>
```

#### 获取练习历史
```
GET /api/practice/
Authorization: Bearer <token>
```

### 用户管理接口（管理员）

#### 获取用户列表
```
GET /api/users/
Authorization: Bearer <token>
```

#### 获取用户详情
```
GET /api/users/{id}/
Authorization: Bearer <token>
```

#### 更新用户
```
PUT /api/users/{id}/
Authorization: Bearer <token>
```

#### 删除用户
```
DELETE /api/users/{id}/
Authorization: Bearer <token>
```

#### 获取用户统计
```
GET /api/users/{id}/stats/
GET /api/users/stats/  # 获取自己的统计
Authorization: Bearer <token>
```

## 数据模型

### UserProfile
- user: 关联用户
- role: 角色 (user|admin)
- phone: 电话
- avatar: 头像
- created_at: 创建时间
- updated_at: 更新时间

### Question
- type: 题目类型 (single|judge)
- difficulty: 难度 (easy|medium|hard)
- question: 题目内容
- options: 选项 (JSON)
- correct_answer: 正确答案索引
- explanation: 解析
- created_at: 创建时间
- updated_at: 更新时间

### Exam
- user: 关联用户
- questions: 题目 (多对多)
- answers: 用户答案 (JSON)
- score: 得分
- total_questions: 总题数
- correct_count: 正确题数
- passed: 是否通过
- time_limit: 时间限制
- created_at: 创建时间
- submitted_at: 提交时间

### PracticeSession
- user: 关联用户
- questions: 题目 (多对多)
- practice_type: 练习类型 (sequential|random)
- answers: 用户答案 (JSON)
- current_question_index: 当前题目索引
- completed: 是否完成
- created_at: 创建时间
- updated_at: 更新时间

## 默认账户

- **管理员**: username: `admin`, password: `admin`
- **普通用户**: 可通过注册接口创建

## 开发说明

### 添加新功能
1. 在 `models.py` 中定义数据模型
2. 在 `serializers.py` 中创建序列化器
3. 在 `views.py` 中实现视图
4. 在 `urls.py` 中配置路由
5. 运行 `python manage.py makemigrations` 和 `python manage.py migrate`

### 数据库管理
- 使用 `python manage.py shell` 进入Django shell
- 使用 `python manage.py createsuperuser` 创建超级用户
- 使用 `python manage.py runserver` 启动开发服务器

### 生产部署
1. 修改 `settings.py` 中的 `DEBUG = False`
2. 配置生产数据库（PostgreSQL/MySQL）
3. 设置 `SECRET_KEY` 和 `ALLOWED_HOSTS`
4. 配置静态文件和媒体文件服务
5. 使用 Gunicorn 或 uWSGI 部署

## 许可证

MIT