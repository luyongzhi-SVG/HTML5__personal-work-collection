# 个人作品集网站

> 现代化响应式个人作品集网站，基于 HTML5 + CSS3 构建，包含完整的后端 API 服务和 GitHub 热点追踪器。

## 📋 项目简介

这是一个功能完善的个人作品集网站，采用前后端分离架构。前端使用纯 HTML5 + CSS3 实现，后端基于 Node.js + Express + SQLite 提供 RESTful API 服务，并集成了 GitHub 热点追踪器功能。

### 核心特性

- 🎨 **现代化 UI 设计** - 毛玻璃效果、渐变背景、CSS 动画
- 📱 **响应式布局** - 自适应桌面端、平板、手机
- 🔧 **后端 API** - Express + SQLite 提供数据接口
- 🔐 **用户系统** - 支持注册、登录功能
- 📝 **文章系统** - 完整的 CRUD 操作
- 💼 **项目展示** - 分类筛选、项目详情页
- 🐙 **GitHub 热点追踪器** - 实时追踪 GitHub 热门项目

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
- Python（用于 GitHub 数据抓取）

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
├── github.html            # GitHub 热点追踪器页面
├── css/
│   └── style.css           # 样式文件
├── github/                 # GitHub 热点追踪器
│   ├── github_tracker.py   # 数据抓取脚本
│   ├── github_api.py       # API 包装脚本
│   ├── generate_test_data.py # 测试数据生成
│   └── github_trending.db   # SQLite 数据库
├── database.js             # 数据库配置
├── server.js               # 服务器入口
├── package.json            # 项目配置
└── Operation manual/
    ├── README.md            # 项目文档
    └── GIT_GUIDE.md         # Git 使用指南
```

## 🚀 快速开始

### 环境要求

- Node.js >= 14.x
- npm 或 yarn
- Python 3.7+（用于 GitHub 数据抓取）

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

3. **初始化数据库**
   - 运行 `npm start` 时会自动初始化数据库
   - 如需 GitHub 数据，运行 `python github/generate_test_data.py` 生成测试数据

4. **启动服务器**
   ```bash
   node server.js
   ```

5. **访问网站**
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
| POST | `/api/articles` | 创建文章（需Token） |
| PUT | `/api/articles/:id` | 更新文章（需Token） |
| DELETE | `/api/articles/:id` | 删除文章（需Token） |

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
Authorization: Bearer <token>

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
| POST | `/api/projects` | 创建项目（需Token） |

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
| GET | `/api/user/info` | 获取用户信息（需Token） |
| POST | `/api/user/logout` | 退出登录 |

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

**默认管理员账号：** `admin` / `admin123`

### GitHub 热点追踪器接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/github/trending` | 获取 GitHub 热门项目 |
| GET | `/api/github/languages` | 获取可用编程语言 |

#### 获取 GitHub 热门项目

```bash
GET /api/github/trending?period=daily&limit=20
```

**参数说明：**
- `period`：时间范围（daily/weekly/monthly）
- `limit`：返回数量（默认 20）

**响应示例：**
```json
{
  "success": true,
  "data": [
    {
      "author": "colbymchenry",
      "repo_name": "codegraph",
      "description": "Pre-indexed code knowledge graph for AI coding...",
      "stars": 12580,
      "forks": 890,
      "today_stars": 234,
      "url": "https://github.com/colbymchenry/codegraph",
      "language": "Python",
      "trend_period": "daily",
      "crawled_at": "2026-05-30T21:54:52.140529"
    }
  ],
  "count": 5
}
```

#### 获取可用编程语言

```bash
GET /api/github/languages
```

**响应示例：**
```json
{
  "success": true,
  "languages": ["Python", "TypeScript", "JavaScript", "Rust", "Go"]
}
```

## 🐙 GitHub 热点追踪器

GitHub 热点追踪器是一个实时展示 GitHub 热门项目的功能模块。

### 功能特点

- 📊 **多时间维度** - 支持日榜、周榜、月榜
- 🏷️ **语言筛选** - 按编程语言过滤项目
- ⭐ **热度指标** - 显示 star 数、fork 数、今日增长
- 🔄 **动态更新** - 支持重新抓取最新数据
- 🎨 **现代化 UI** - 毛玻璃卡片、动画效果

### 使用方法

#### 方式一：使用预置数据

```bash
# 生成测试数据
python github/generate_test_data.py
```

#### 方式二：抓取最新数据

```bash
# 进入 github 目录
cd github

# 运行抓取脚本（交互模式）
python github_tracker.py

# 运行抓取脚本（自动模式，使用默认选项）
echo "1" | python github_tracker.py
```

### 前端页面

访问 `http://localhost:3000/github.html` 查看 GitHub 热点追踪器页面。

## 🎨 页面说明

### 首页 (index.html)

- 英雄区域展示
- GitHub 热点追踪器入口
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

### GitHub 热点追踪器 (github.html)

- 热门项目列表
- 时间范围切换（日/周/月）
- 编程语言筛选
- 项目详情卡片
- 数据加载动画

## 🎯 CSS 特效

项目使用了多种现代 CSS 特效：

- **毛玻璃效果** - `backdrop-filter: blur()`
- **渐变背景** - `linear-gradient()`
- **过渡动画** - `transition`
- **关键帧动画** - `@keyframes`
- **响应式设计** - 媒体查询
- **Flex 布局** - 圣杯布局
- **Grid 布局** - 瀑布流卡片
- **滤镜效果** - `filter: brightness()`

## 🌐 部署说明

### GitHub Pages（仅前端）

1. 创建 GitHub 仓库
2. 上传所有 HTML、CSS 文件
3. 在 Settings → Pages 中启用
4. 访问 `https://yourusername.github.io/repo-name`

**注意：** GitHub Pages 不支持后端 API，GitHub 热点追踪器功能需要单独部署后端服务。

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
| password | TEXT | 密码（加密存储） |
| created_at | TIMESTAMP | 创建时间 |

### repositories 表（GitHub 热点数据）

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| author | TEXT | 项目作者 |
| repo_name | TEXT | 仓库名称 |
| description | TEXT | 项目描述 |
| stars | INTEGER | Star 数量 |
| forks | INTEGER | Fork 数量 |
| today_stars | INTEGER | 今日增长 Star |
| url | TEXT | GitHub 地址 |
| language | TEXT | 编程语言 |
| trend_period | TEXT | 趋势周期 |
| crawled_at | TIMESTAMP | 抓取时间 |

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

### 扩展 GitHub 热点追踪器

如需抓取更详细的 GitHub 数据，可以修改 `github/github_tracker.py`：

```python
# 添加新的抓取逻辑
def fetch_more_details(repo_url):
    # 获取仓库详细信息
    pass
```

## 📄 许可证

MIT License

## 👤 作者

luyongzhi-SVG - [GitHub](https://github.com/luyongzhi-SVG)

## 🙏 致谢

- [Font Awesome](https://fontawesome.com/) - 图标库
- [Express.js](https://expressjs.com/) - 后端框架
- [SQLite](https://www.sqlite.org/) - 数据库
- [GitHub](https://github.com/) - 热门项目数据来源
