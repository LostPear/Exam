# 驾照理论模拟考试系统 - Django后端

基于 Django REST Framework 开发的驾照理论模拟考试系统后端API。

## 功能特性

### 用户管理
- ✅ 用户注册、登录、登出
- ✅ JWT Token 认证
- ✅ 个人资料管理
- ✅ 密码修改
- ✅ 用户角色管理（普通用户、管理员）

### 题库管理
- ✅ 题目增删改查
- ✅ 题目搜索和筛选（按类型、难度、分类）
- ✅ 随机题目获取
- ✅ 顺序题目获取
- ✅ 批量导入题目（支持Excel、CSV、JSON）

### 考试功能
- ✅ 创建考试（可指定题目数量和难度）
- ✅ 提交考试答案
- ✅ 自动评分
- ✅ 考试结果查询
- ✅ 考试历史记录

### 练习功能
- ✅ 练习记录保存
- ✅ 自动判断答案正确性
- ✅ 练习统计

### 统计功能
- ✅ 用户学习统计
- ✅ 练习正确率
- ✅ 考试通过率

## 技术栈

- **后端框架**: Django 4.2
- **API框架**: Django REST Framework
- **认证**: JWT (djangorestframework-simplejwt)
- **数据库**: SQLite（开发环境）/ PostgreSQL/MySQL（生产环境）
- **跨域**: django-cors-headers
- **数据处理**: pandas, openpyxl

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

建议使用虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 初始化数据

创建默认用户和示例题目：

```bash
python manage.py init_data
```

这将创建：
- 管理员账户：`admin` / `admin`
- 普通用户账户：`user` / `password`
- 10道示例题目

### 4. 创建超级管理员（可选）

```bash
python manage.py createsuperuser
```

### 5. 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

服务器将在 `http://localhost:8000` 运行。

访问管理后台：`http://localhost:8000/admin`

## API 接口文档

### 基础URL
```
http://localhost:8000/api/
```

### 认证接口

#### 注册
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "password2": "password123"
}
```

响应：
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "role": "user"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 登录
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

#### 登出
```http
POST /api/auth/logout/
Authorization: Bearer <token>
Content-Type: application/json

{
  "refresh": "refresh_token"
}
```

#### 获取/更新个人资料
```http
GET /api/auth/profile/
Authorization: Bearer <token>

PUT /api/auth/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "phone": "13800138000"
}
```

#### 修改密码
```http
POST /api/auth/change-password/
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "oldpass123",
  "new_password": "newpass456"
}
```

### 题目接口

#### 获取题目列表
```http
GET /api/questions/
GET /api/questions/?search=红灯
GET /api/questions/?type=single
GET /api/questions/?difficulty=easy
GET /api/questions/?category=交通信号
Authorization: Bearer <token>
```

#### 获取单个题目
```http
GET /api/questions/{id}/
Authorization: Bearer <token>
```

#### 创建题目（管理员）
```http
POST /api/questions/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "type": "single",
  "difficulty": "medium",
  "category": "交通信号",
  "question": "红灯表示什么？",
  "options": ["禁止通行", "准许通行", "警示", "减速"],
  "correct_answer": 0,
  "explanation": "红灯表示禁止通行。"
}
```

#### 更新题目（管理员）
```http
PUT /api/questions/{id}/
Authorization: Bearer <admin_token>
```

#### 删除题目（管理员）
```http
DELETE /api/questions/{id}/
Authorization: Bearer <admin_token>
```

#### 获取随机题目
```http
GET /api/questions/random/?count=10
GET /api/questions/random/?count=10&difficulty=medium
Authorization: Bearer <token>
```

#### 获取顺序题目
```http
GET /api/questions/sequential/?offset=0&limit=10
Authorization: Bearer <token>
```

#### 批量导入题目（管理员）
```http
POST /api/questions/import_questions/
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

file: <Excel/CSV/JSON文件>
```

### 考试接口

#### 创建考试
```http
POST /api/exams/
Authorization: Bearer <token>
Content-Type: application/json

{
  "question_count": 50,
  "difficulty": "all"  // all, easy, medium, hard
}
```

#### 获取考试详情
```http
GET /api/exams/{id}/
Authorization: Bearer <token>
```

#### 提交考试
```http
POST /api/exams/{id}/submit/
Authorization: Bearer <token>
Content-Type: application/json

{
  "answers": {
    "1": 0,
    "2": 1,
    "3": 2
  }
}
```

#### 获取考试结果
```http
GET /api/exams/{id}/result/
Authorization: Bearer <token>
```

#### 获取考试历史
```http
GET /api/exams/history/
Authorization: Bearer <token>
```

### 练习接口

#### 创建练习记录
```http
POST /api/practice/
Authorization: Bearer <token>
Content-Type: application/json

{
  "question": 1,
  "user_answer": 0,
  "practice_type": "sequential"  // sequential 或 random
}
```

#### 获取练习记录
```http
GET /api/practice/
Authorization: Bearer <token>
```

### 用户管理接口（管理员）

#### 获取用户列表
```http
GET /api/users/
GET /api/users/?search=username
Authorization: Bearer <admin_token>
```

#### 获取用户详情
```http
GET /api/users/{id}/
Authorization: Bearer <admin_token>
```

#### 更新用户
```http
PUT /api/users/{id}/
Authorization: Bearer <admin_token>
```

#### 删除用户
```http
DELETE /api/users/{id}/
Authorization: Bearer <admin_token>
```

#### 获取用户统计
```http
GET /api/users/{id}/stats/
Authorization: Bearer <admin_token>
```

### 统计接口

#### 获取当前用户统计
```http
GET /api/stats/
Authorization: Bearer <token>
```

响应：
```json
{
  "id": 1,
  "user": 1,
  "total_exams": 5,
  "passed_exams": 4,
  "total_practice": 100,
  "correct_practice": 85,
  "study_time": 300,
  "practice_accuracy": 85.0,
  "exam_pass_rate": 80.0,
  "last_practice_at": "2025-10-19T10:30:00",
  "updated_at": "2025-10-19T12:00:00"
}
```

## 数据模型

### User（用户）
- username: 用户名
- email: 邮箱
- password: 密码
- role: 角色（user/admin）
- phone: 手机号
- avatar: 头像

### Question（题目）
- type: 题目类型（single单选/judge判断）
- difficulty: 难度（easy/medium/hard）
- category: 分类
- question: 题目内容
- options: 选项数组
- correct_answer: 正确答案索引
- explanation: 答案解析
- image: 题目图片

### Exam（考试）
- user: 考生
- status: 状态（in_progress/completed）
- score: 分数
- passed: 是否通过
- total_questions: 题目总数
- correct_count: 正确数量
- wrong_count: 错误数量
- duration: 考试时长（秒）

### ExamQuestion（考试题目关联）
- exam: 考试
- question: 题目
- user_answer: 用户答案
- is_correct: 是否正确
- order: 题目顺序

### PracticeRecord（练习记录）
- user: 用户
- question: 题目
- user_answer: 用户答案
- is_correct: 是否正确
- practice_type: 练习类型（sequential/random）

### UserStats（用户统计）
- user: 用户
- total_exams: 考试总数
- passed_exams: 通过考试数
- total_practice: 练习总数
- correct_practice: 练习正确数
- study_time: 学习时长
- practice_accuracy: 练习正确率
- exam_pass_rate: 考试通过率

## 题目导入格式

### Excel/CSV 格式

| type | difficulty | category | question | options | correct_answer | explanation |
|------|-----------|----------|----------|---------|----------------|-------------|
| single | easy | 交通信号 | 红灯表示？ | ["禁止通行","准许通行","警示","减速"] | 0 | 红灯表示禁止通行 |

### JSON 格式

```json
[
  {
    "type": "single",
    "difficulty": "easy",
    "category": "交通信号",
    "question": "红灯表示？",
    "options": ["禁止通行", "准许通行", "警示", "减速"],
    "correct_answer": 0,
    "explanation": "红灯表示禁止通行"
  }
]
```

## 配置说明

### 生产环境配置

在生产环境中，建议修改以下配置：

1. **SECRET_KEY**: 修改为随机生成的安全密钥
2. **DEBUG**: 设置为 `False`
3. **ALLOWED_HOSTS**: 添加你的域名
4. **数据库**: 使用 PostgreSQL 或 MySQL
5. **CORS**: 限制允许的源

### 环境变量

可以使用 `.env` 文件管理配置：

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## 部署

### 使用 Gunicorn

```bash
pip install gunicorn
gunicorn exam_system.wsgi:application --bind 0.0.0.0:8000
```

### 使用 Nginx

配置 Nginx 作为反向代理：

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/backend/staticfiles/;
    }

    location /media/ {
        alias /path/to/backend/media/;
    }
}
```

### 收集静态文件

```bash
python manage.py collectstatic
```

## 测试

运行测试：

```bash
python manage.py test
```

## 常见问题

### Q: 如何重置数据库？
```bash
rm db.sqlite3
python manage.py migrate
python manage.py init_data
```

### Q: 如何修改JWT过期时间？
在 `settings.py` 中修改 `SIMPLE_JWT` 配置。

### Q: 如何添加更多题目类型？
在 `models.py` 的 `Question.TYPE_CHOICES` 中添加新类型。

## License

MIT
