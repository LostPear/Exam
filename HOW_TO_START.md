# 🚀 驾照理论模拟考试系统 - 启动指南

## 项目简介

这是一个完整的驾照理论模拟考试系统，包含：
- **前端**: Vue 3 + Vite + TailwindCSS
- **后端**: Django 4.2 + Django REST Framework

## ⚡ 快速启动（2步完成）

### 第一步：启动后端

打开终端1：

```bash
cd backend
./start.sh
```

或者手动启动：
```bash
cd backend
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py init_data
python3 manage.py runserver 0.0.0.0:8000
```

✅ 后端将运行在: http://localhost:8000

### 第二步：启动前端

打开终端2：

```bash
npm install
npm run dev
```

✅ 前端将运行在: http://localhost:3000

## 🎯 开始使用

### 访问系统
打开浏览器访问: **http://localhost:3000**

### 默认账户
| 用户类型 | 用户名 | 密码 |
|---------|--------|------|
| 管理员 | admin | admin |
| 普通用户 | user | password |

### 管理后台
访问: http://localhost:8000/admin/
使用管理员账户登录

## 📚 功能列表

### 👤 普通用户功能
- ✅ 注册和登录
- ✅ 顺序练习题目
- ✅ 随机练习题目
- ✅ 模拟考试（自动组卷、评分）
- ✅ 查看考试历史和成绩
- ✅ 个人资料管理
- ✅ 学习统计数据

### 👨‍💼 管理员功能
- ✅ 题库管理（增删改查）
- ✅ 用户管理
- ✅ 批量导入题目（Excel/CSV/JSON）
- ✅ 查看用户学习数据

## 📁 项目结构

```
项目根目录/
├── src/                    # 前端源代码
├── backend/                # Django后端
│   ├── api/               # API应用
│   ├── exam_system/       # Django配置
│   ├── manage.py
│   └── start.sh           # 快速启动脚本
├── package.json
└── README.md
```

## 🧪 测试后端API

```bash
cd backend
python3 test_api.py
```

## 📖 详细文档

- **前端文档**: `README.md`
- **后端API文档**: `backend/README.md`
- **后端使用指南**: `backend/BACKEND_GUIDE.md`
- **快速开始**: `backend/QUICKSTART_CN.md`
- **项目总览**: `PROJECT_OVERVIEW.md`
- **完成报告**: `DJANGO_BACKEND_COMPLETED.md`

## 🔧 常见问题

### Q: 如何重置数据？
```bash
cd backend
rm db.sqlite3
python3 manage.py migrate
python3 manage.py init_data
```

### Q: 端口被占用怎么办？
修改端口：
- 前端: 编辑 `vite.config.js`
- 后端: `python3 manage.py runserver 0.0.0.0:8001`

### Q: 如何添加更多题目？
1. 使用管理后台: http://localhost:8000/admin
2. 使用管理员账号批量导入
3. 调用API接口添加

## 💡 开发提示

### 查看API文档
访问: http://localhost:8000/api/

### 查看数据库
使用Django shell:
```bash
cd backend
python3 manage.py shell
```

### 查看日志
后端日志会显示在终端中

## 🎉 开始体验

1. 启动后端和前端
2. 访问 http://localhost:3000
3. 使用默认账户登录
4. 开始答题练习或考试！

---

**祝你使用愉快！** 🚗📚
