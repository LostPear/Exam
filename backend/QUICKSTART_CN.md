# 快速开始 - Django后端

## 🚀 5分钟启动后端

### 第一步：安装依赖

```bash
cd backend
pip install -r requirements.txt
```

或使用虚拟环境（推荐）：
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 第二步：初始化数据库（如果还没初始化）

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py init_data
```

### 第三步：启动服务器

```bash
# 方式1：使用启动脚本（推荐）
./start.sh

# 方式2：直接启动
python3 manage.py runserver 0.0.0.0:8000
```

### 第四步：测试API

```bash
# 安装requests库（如果还没有）
pip install requests

# 运行测试脚本
python3 test_api.py
```

## 📍 访问地址

- **API基础地址**: http://localhost:8000/api/
- **管理后台**: http://localhost:8000/admin/
- **前端地址**: http://localhost:3000 (需要单独启动前端)

## 👤 默认账户

| 用户类型 | 用户名 | 密码 |
|---------|--------|------|
| 管理员 | admin | admin |
| 普通用户 | user | password |

## 🧪 快速测试

### 1. 测试登录
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

### 2. 测试获取题目（需要先登录获取token）
```bash
curl -X GET http://localhost:8000/api/questions/ \
  -H "Authorization: Bearer <你的token>"
```

## 📦 已包含数据

- ✅ 2个测试用户（1个管理员 + 1个普通用户）
- ✅ 10道示例题目（涵盖不同类型和难度）
- ✅ 完整的API端点
- ✅ 用户统计系统

## 🔄 前后端联调

### 1. 启动后端
```bash
cd backend
python3 manage.py runserver 0.0.0.0:8000
```

### 2. 启动前端
```bash
cd ..  # 回到项目根目录
npm run dev
```

### 3. 访问前端
打开浏览器访问: http://localhost:3000

使用默认账户登录即可！

## ⚙️ 常用命令

### 查看所有用户
```bash
python3 manage.py shell -c "from api.models import User; [print(f'{u.username} - {u.role}') for u in User.objects.all()]"
```

### 查看题目数量
```bash
python3 manage.py shell -c "from api.models import Question; print(f'题目总数: {Question.objects.count()}')"
```

### 创建超级管理员
```bash
python3 manage.py createsuperuser
```

### 重置数据库
```bash
rm db.sqlite3
python3 manage.py migrate
python3 manage.py init_data
```

## 📚 主要API端点

### 认证
- `POST /api/auth/register/` - 注册
- `POST /api/auth/login/` - 登录
- `POST /api/auth/logout/` - 登出

### 题目
- `GET /api/questions/` - 获取题目列表
- `GET /api/questions/random/?count=10` - 获取随机题目
- `POST /api/questions/` - 创建题目（管理员）

### 考试
- `POST /api/exams/` - 创建考试
- `POST /api/exams/{id}/submit/` - 提交答案
- `GET /api/exams/{id}/result/` - 获取结果

### 练习
- `POST /api/practice/` - 记录练习
- `GET /api/practice/` - 获取练习记录

## 🔧 故障排查

### 问题：端口被占用
```bash
# 使用其他端口
python3 manage.py runserver 0.0.0.0:8001
```

### 问题：CORS错误
检查 `settings.py` 中的 `CORS_ALLOWED_ORIGINS` 配置

### 问题：数据库错误
```bash
# 重建数据库
rm db.sqlite3
rm -rf api/migrations/000*.py
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py init_data
```

## 📖 详细文档

- **完整API文档**: 查看 `README.md`
- **部署指南**: 查看 `BACKEND_GUIDE.md`
- **项目总结**: 查看 `../BACKEND_SUMMARY.md`

## ✨ 下一步

1. 启动前端项目
2. 使用默认账户登录
3. 体验完整功能
4. 根据需要添加更多题目

## 💡 提示

- 开发时建议同时打开两个终端：一个运行后端，一个运行前端
- 使用管理后台可以方便地管理题目和用户
- 查看浏览器控制台可以看到API请求详情
- 使用Django Admin可以快速查看和修改数据

祝你使用愉快！🎉
