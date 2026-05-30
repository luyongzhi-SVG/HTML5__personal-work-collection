# GitHub 热点追踪器

一个用于追踪 GitHub 趋势榜的 Python 工具，支持自动抓取、数据持久化和定时更新。

## ✨ 功能特性

- ✅ **多周期抓取**：支持日榜、周榜、月榜
- ✅ **语言筛选**：按编程语言筛选（Python/Java/Go 等）
- ✅ **数据持久化**：支持 JSON 文件和 SQLite 数据库两种存储方式
- ✅ **定时更新**：周期性自动抓取，无需手动运行
- ✅ **控制台展示**：格式化展示热点列表

## 📋 环境要求

- Python 3.6+
- requests 库

## 🛠️ 安装步骤

```bash
# 进入项目目录
cd d:\b\github

# 安装依赖
pip install requests
```

## 🚀 使用方法

### 启动程序

```bash
python github_tracker.py
```

### 操作菜单

```
╔══════════════════════════════════════════════════════════════╗
║                    GitHub 热点追踪器                        ║
╠══════════════════════════════════════════════════════════════╣
║  1. 抓取日榜                                                  ║
║  2. 抓取周榜                                                  ║
║  3. 抓取月榜                                                  ║
║  4. 按语言筛选抓取                                            ║
║  5. 查看本地数据                                              ║
║  6. 启动定时追踪 (每60分钟)                                   ║
╚══════════════════════════════════════════════════════════════╝
```

### 示例

```bash
# 选择操作 4 按语言筛选
请选择操作 (1-6): 4
请输入编程语言 (如 Python/Java/Go): Python
请选择周期 (daily/weekly/monthly，默认daily): daily

# 输出示例
📌 TOP 1
  🏠 仓库: author/repo-name
  🔗 地址: https://github.com/author/repo-name
  📝 简介: 仓库简介...
  🎯 周期: 日榜
  💻 语言: Python
  ⭐ Stars: 12,345
  🔀 Forks: 4,567
  📈 今日新增: +890 stars
```

## 📁 项目结构

```
github/
├── github_tracker.py      # 主程序
├── github_trending.db     # SQLite 数据库文件（自动生成）
├── github_trending.json   # JSON 数据文件（自动生成）
└── README.md              # 说明文档
```

## 📊 数据存储

### JSON 文件格式

```json
[
  {
    "author": "username",
    "repo_name": "repo-name",
    "description": "项目简介",
    "stars": 12345,
    "forks": 4567,
    "today_stars": 890,
    "url": "https://github.com/username/repo-name",
    "language": "Python",
    "trend_period": "daily",
    "crawled_at": "2024-01-15T10:30:00"
  }
]
```

### 数据库表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| author | TEXT | 作者名 |
| repo_name | TEXT | 仓库名 |
| description | TEXT | 简介 |
| stars | INTEGER | Star 数 |
| forks | INTEGER | Fork 数 |
| today_stars | INTEGER | 当日新增 Star |
| url | TEXT | 仓库地址 |
| language | TEXT | 编程语言 |
| trend_period | TEXT | 趋势周期 |
| crawled_at | TIMESTAMP | 抓取时间 |

## ⏰ 定时任务

选择选项 6 启动定时追踪：

```bash
请选择操作 (1-6): 6

🚀 GitHub 热点追踪器已启动，每 60 分钟更新一次
⏰ 开始抓取 GitHub 趋势榜 (daily)...
```

按 `Ctrl+C` 停止定时任务。

## 📝 代码调用示例

```python
from github_tracker import GitHubTrending

# 创建追踪器实例
tracker = GitHubTrending()

# 抓取日榜
data = tracker.fetch_trending("daily")

# 抓取指定语言周榜
data = tracker.fetch_trending("weekly", language="Python")

# 保存到 JSON
tracker.save_to_json(data)

# 保存到数据库
tracker.save_to_database(data)

# 查询数据库
results = tracker.query_database(period="daily", language="Python")

# 展示结果
tracker.display_trending(results)
```

## 🔧 API 接口

### fetch_trending(period, language)

抓取 GitHub 趋势榜

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| period | str | "daily" | 时间周期 (daily/weekly/monthly) |
| language | str | "" | 编程语言筛选 |

### save_to_json(data, filename)

保存数据到 JSON 文件

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data | list | - | 仓库数据列表 |
| filename | str | None | 文件名，默认 github_trending.json |

### save_to_database(data)

保存数据到 SQLite 数据库

| 参数 | 类型 | 说明 |
|------|------|------|
| data | list | 仓库数据列表 |

### query_database(period, language)

查询数据库

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| period | str | "" | 周期筛选 |
| language | str | "" | 语言筛选 |

### display_trending(data, limit)

控制台展示热点列表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data | list | - | 仓库数据列表 |
| limit | int | 10 | 显示数量限制 |

### start_scheduler(interval_minutes)

启动定时调度器

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| interval_minutes | int | 60 | 更新间隔（分钟） |

## 📌 支持的编程语言

常见编程语言：Python, Java, Go, JavaScript, TypeScript, Rust, C++, C#, PHP, Ruby, Swift, Kotlin 等

## ⚠️ 注意事项

1. 请合理控制抓取频率，避免给 GitHub 服务器造成压力
2. 建议使用定时任务时设置较长的间隔（如 60 分钟以上）
3. 数据仅供学习和研究使用，遵守 GitHub 服务条款

## 📄 许可证

MIT License
