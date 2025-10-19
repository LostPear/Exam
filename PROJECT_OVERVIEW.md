# 驾照理论模拟考试系统 - 完整项目

## 项目简介

这是一个完整的驾照理论模拟考试系统，包含Vue.js前端和Django REST API后端。

## 🎯 功能特性

### 用户功能
- ✅ 用户注册、登录、个人资料管理
- ✅ 顺序练习和随机练习
- ✅ 模拟考试（智能组卷、自动评分、错题解析）
- ✅ 学习统计和考试历史

### 管理员功能
- ✅ 题库管理（增删改查）
- ✅ 用户管理
- ✅ 批量导入题目（支持Excel、CSV、JSON）

## 📁 项目结构

```
.
├── frontend/              # Vue.js前端（当前目录的前端文件）
│   ├── src/
│   │   ├── api/          # API接口定义
│   │   ├── views/        # 页面组件
│   │   ├── stores/       # 状态管理
│   │   └── router/       # 路由配置
│   ├── package.json
│   └── vite.config.js
│
├── backend/              # Django后端
│   ├── api/             # API应用
│   ├── exam_system/     # Django项目配置
│   ├── manage.py
│   ├── requirements.txt
│   ├── start.sh         # 快速启动脚本
│   └── README.md        # 后端详细文档
│
├── README.md            # 前端说明（原有）
└── PROJECT_OVERVIEW.md  # 本文件
```

## 🚀 快速开始

### 前置要求

- Node.js 16+
- Python 3.8+
- pip

### 第一步：启动后端

```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 初始化数据库（首次运行）
python3 manage.py migrate
python3 manage.py init_data

# 启动后端服务器
python3 manage.py runserver 0.0.0.0:8000

# 或使用启动脚本
./start.sh
```

后端将运行在: http://localhost:8000

### 第二步：启动前端

打开新的终端：

```bash
# 安装前端依赖（首次运行）
npm install

# 启动前端开发服务器
npm run dev
```

前端将运行在: http://localhost:3000

### 第三步：开始使用

打开浏览器访问: http://localhost:3000

使用默认账户登录：
- **管理员**: `admin` / `admin`
- **普通用户**: `user` / `password`

## 🔗 系统架构

```
┌─────────────────┐         ┌─────────────────┐
│   Vue.js 前端    │         │  Django 后端     │
│  (Port 3000)    │ <-----> │  (Port 8000)    │
│                 │  HTTP   │                 │
│  - 用户界面      │  REST   │  - API端点       │
│  - 路由管理      │  API    │  - 数据库        │
│  - 状态管理      │         │  - 业务逻辑      │
└─────────────────┘         └─────────────────┘
```

### 技术栈

**前端**
- Vue 3 (Composition API)
- Vite
- TailwindCSS
- Vue Router
- Pinia
- Axios

**后端**
- Django 4.2
- Django REST Framework
- SimpleJWT (认证)
- SQLite (开发) / PostgreSQL (生产)
- pandas & openpyxl (数据导入)

## 📡 API端点概览

### 认证相关
```
POST   /api/auth/register/        用户注册
POST   /api/auth/login/           用户登录
POST   /api/auth/logout/          用户登出
GET    /api/auth/profile/         获取个人资料
PUT    /api/auth/profile/         更新个人资料
POST   /api/auth/change-password/ 修改密码
```

### 题目管理
```
GET    /api/questions/                   获取题目列表
GET    /api/questions/random/            获取随机题目
GET    /api/questions/sequential/        获取顺序题目
POST   /api/questions/                   创建题目
POST   /api/questions/import_questions/  批量导入
```

### 考试相关
```
POST   /api/exams/               创建考试
GET    /api/exams/{id}/          获取考试详情
POST   /api/exams/{id}/submit/   提交答案
GET    /api/exams/{id}/result/   获取结果
GET    /api/exams/history/       考试历史
```

### 用户管理（管理员）
```
GET    /api/users/            用户列表
GET    /api/users/{id}/       用户详情
GET    /api/users/{id}/stats/ 用户统计
```

## 📊 数据模型

### User（用户）
- 用户名、邮箱、密码
- 角色（user/admin）
- 个人信息

### Question（题目）
- 题目类型（单选/判断）
- 难度等级
- 题目内容和选项
- 正确答案和解析

### Exam（考试）
- 关联用户和题目
- 考试状态和分数
- 答题记录

### UserStats（统计）
- 练习统计
- 考试统计
- 学习时长

## 🎨 界面预览

### 用户界面
- 登录/注册页面
- 个人中心
- 练习页面（顺序/随机）
- 考试页面
- 成绩查询

### 管理员界面
- 题库管理
- 用户管理
- 数据导入

## 🔒 安全特性

- JWT Token认证
- 密码加密存储
- CORS跨域保护
- 权限分级控制
- 参数验证

## 📝 开发指南

### 添加新的API端点

1. **后端** (backend/api/)
   - 在 `models.py` 定义数据模型
   - 在 `serializers.py` 创建序列化器
   - 在 `views.py` 实现视图逻辑
   - 在 `urls.py` 配置路由

2. **前端** (src/api/)
   - 在相应的API文件中添加接口函数
   - 在组件中调用API

### 添加新页面

1. 在 `src/views/` 创建Vue组件
2. 在 `src/router/index.js` 添加路由
3. 根据需要添加权限控制

### 数据库迁移

```bash
cd backend
python3 manage.py makemigrations
python3 manage.py migrate
```

## 🧪 测试

### 后端测试
```bash
cd backend
python3 manage.py test

# 或使用测试脚本
python3 test_api.py
```

### 前端测试
```bash
npm run test  # 如果配置了测试
```

## 📦 部署

### 开发环境（当前配置）
- 前端: Vite开发服务器
- 后端: Django开发服务器
- 数据库: SQLite

### 生产环境建议

**前端**
```bash
npm run build
# 将dist/目录部署到静态服务器或CDN
```

**后端**
```bash
# 使用Gunicorn + Nginx
pip install gunicorn
gunicorn exam_system.wsgi:application

# 配置Nginx反向代理
# 使用PostgreSQL数据库
# 配置HTTPS
```

详细部署指南请查看 `backend/BACKEND_GUIDE.md`

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| `README.md` | 前端项目说明 |
| `backend/README.md` | 后端API完整文档 |
| `backend/BACKEND_GUIDE.md` | 后端使用和部署指南 |
| `backend/QUICKSTART_CN.md` | 后端5分钟快速启动 |
| `BACKEND_SUMMARY.md` | 后端开发总结 |

## ❓ 常见问题

### Q: 如何重置所有数据？
```bash
# 后端
cd backend
rm db.sqlite3
python3 manage.py migrate
python3 manage.py init_data
```

### Q: 如何添加更多题目？
1. 使用管理后台手动添加: http://localhost:8000/admin
2. 使用管理员账号批量导入
3. 直接在数据库中添加

### Q: 如何修改端口？
- **前端**: 修改 `vite.config.js` 中的 `server.port`
- **后端**: 启动时指定 `python3 manage.py runserver 0.0.0.0:端口`

### Q: CORS错误怎么办？
检查 `backend/exam_system/settings.py` 中的 `CORS_ALLOWED_ORIGINS` 配置

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 License

MIT

## 🎉 致谢

感谢使用本项目！如有问题，请查看相关文档或提Issue。

---

**当前状态**: ✅ 前后端开发完成，可以正常运行

**快速启动命令**:
```bash
# 终端1：启动后端
cd backend && ./start.sh

# 终端2：启动前端
npm run dev

# 然后访问 http://localhost:3000
```
