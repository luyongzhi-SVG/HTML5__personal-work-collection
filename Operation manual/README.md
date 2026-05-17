# 个人作品集网站

> 现代化响应式个人作品集网站，基于 HTML5 + CSS3 构建，包含完整的后端 API 服务。

## 📋 项目简介

这是一个功能完善的个人作品集网站，采用前后端分离架构。前端使用纯 HTML5 + CSS3 实现，后端基于 Node.js + Express + SQLite 提供 RESTful API 服务。

### 核心特性

- 🎨 **现代化 UI 设计** - 毛玻璃效果、渐变背景、CSS 动画
- 📱 **响应式布局** - 自适应桌面端、平板、手机
- 🔧 **后端 API** - Express + SQLite 提供数据接口
- 🔐 **用户系统** - 支持注册、登录功能
- 📝 **文章系统** - 完整的 CRUD 操作
- 💼 **项目展示** - 分类筛选、项目详情页

## 🛠 技术栈

### 前端

- HTML5 语义化标签
- CSS3（Flexbox、Grid、动画、毛玻璃效果）
- Font Awesome 6 图标库
- 原生 JavaScript

### 后端

- Node.js
- Express.js
- SQLite3
- CORS 跨域支持

## 📁 项目结构

```
work/
├── index.html              # 首页
├── about.html              # 关于页面
├── projects.html           # 项目展示页
├── contact.html            # 联系页面
├── login.html              # 登录页面
├── article.html            # 文章详情页
├── notes.html              # 学习笔记页
├── css/
│   └── style.css           # 样式文件
├── database.js             # 数据库配置
├── server.js               # 服务器入口
├── package.json            # 项目配置
└── README.md               # 项目文档
```

## 🚀 快速开始

### 环境要求

- Node.js >= 14.x
- npm 或 yarn

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd work
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动服务器**
   ```bash
   node server.js
   ```

4. **访问网站**
   - 前端页面：http://localhost:3000
   - API 接口：http://localhost:3000/api

### 启动前端开发服务器

如果只需要查看前端页面（无需 API），可以使用 Python：

```bash
# Python 3
python -m http.server 8080

# 访问 http://localhost:8080
```

## 📡 API 文档

### 文章接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/articles` | 获取所有文章 |
| GET | `/api/articles/:id` | 获取单篇文章 |
| POST | `/api/articles` | 创建文章 |
| PUT | `/api/articles/:id` | 更新文章 |
| DELETE | `/api/articles/:id` | 删除文章 |

#### 获取所有文章

```bash
GET /api/articles
```

**响应示例：**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "代码筑界，像素生光",
      "content": "以HTML搭建骨架，用CSS雕琢肌理...",
      "category": "技术",
      "created_at": "2026-05-17 12:00:00"
    }
  ]
}
```

#### 创建文章

```bash
POST /api/articles
Content-Type: application/json

{
  "title": "新文章标题",
  "content": "文章内容...",
  "category": "技术"
}
```

### 项目接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/projects` | 获取所有项目 |
| GET | `/api/projects/:id` | 获取单个项目 |
| POST | `/api/projects` | 创建项目 |

#### 获取所有项目

```bash
GET /api/projects
```

**响应示例：**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "电商管理平台",
      "description": "基于Vue3 + TypeScript开发的电商管理后台系统",
      "category": "前端项目",
      "tech_stack": "Vue3 / TypeScript",
      "created_at": "2026-05-17 12:00:00"
    }
  ]
}
```

### 用户接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/register` | 用户注册 |
| POST | `/api/login` | 用户登录 |

#### 用户注册

```bash
POST /api/register
Content-Type: application/json

{
  "username": "用户名",
  "email": "email@example.com",
  "password": "密码"
}
```

#### 用户登录

```bash
POST /api/login
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码"
}
```

## 🎨 页面说明

### 首页 (index.html)

- 英雄区域展示
- 瀑布流文章卡片
- 分类标签筛选
- 毛玻璃导航栏

### 关于页面 (about.html)

- 个人介绍
- 技术栈展示
- 专业经验
- 教育背景

### 项目展示 (projects.html)

- 项目卡片展示
- 分类标签筛选
- 项目详情链接
- 技术栈标签

### 联系页面 (contact.html)

- 联系信息展示
- 联系表单
- 社交媒体链接

### 登录页面 (login.html)

- 毛玻璃表单效果
- 用户登录表单
- 登录按钮动画

### 文章详情页

- 文章内容展示
- 代码块高亮
- 阅读统计
- 分类标签

## 🎯 CSS 特效

项目使用了多种现代 CSS 特效：

- **毛玻璃效果** - `backdrop-filter: blur()`
- **渐变背景** - `linear-gradient()`
- **过渡动画** - `transition`
- **关键帧动画** - `@keyframes`
- **响应式设计** - 媒体查询
- **Flex 布局** - 圣杯布局
- **Grid 布局** - 瀑布流卡片

## 🌐 部署说明

### GitHub Pages（仅前端）

1. 创建 GitHub 仓库
2. 上传所有 HTML、CSS 文件
3. 在 Settings → Pages 中启用
4. 访问 `https://yourusername.github.io/repo-name`

### 完整部署（前端 + 后端）

#### 使用 Vercel + Railway

1. 前端部署到 Vercel
2. 后端部署到 Railway（支持 SQLite）
3. 配置环境变量

#### 使用 Heroku

```bash
heroku create
git push heroku main
```

## 📝 数据库结构

### articles 表

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| title | TEXT | 文章标题 |
| content | TEXT | 文章内容 |
| category | TEXT | 分类 |
| created_at | TIMESTAMP | 创建时间 |

### projects 表

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 项目名称 |
| description | TEXT | 项目描述 |
| category | TEXT | 分类 |
| tech_stack | TEXT | 技术栈 |
| created_at | TIMESTAMP | 创建时间 |

### users 表

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| username | TEXT | 用户名（唯一） |
| email | TEXT | 邮箱（唯一） |
| password | TEXT | 密码 |
| created_at | TIMESTAMP | 创建时间 |

## 🔧 开发指南

### 添加新页面

1. 在根目录创建 HTML 文件
2. 引入 `css/style.css`
3. 遵循现有的导航结构

### 添加新 API 接口

在 `server.js` 中添加：

```javascript
app.get('/api/new-endpoint', (req, res) => {
    db.all('SELECT * FROM table', (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ success: true, data: rows });
        }
    });
});
```

## 📄 许可证

MIT License

## 👤 作者:luyongzhi-SVG

您的名字 - [GitHub](https://github.com/luyongzhi-SVG)

## 🙏 致谢

- [Font Awesome](https://fontawesome.com/) - 图标库
- [Express.js](https://expressjs.com/) - 后端框架
- [SQLite](https://www.sqlite.org/) - 数据库