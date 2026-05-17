# Git 命令使用指南

## 📚 初始化新仓库

如果你还没有初始化 Git 仓库，按照以下步骤操作：

### 1. 初始化本地仓库

```bash
# 进入项目目录
cd d:\HTML5\work

# 初始化 Git 仓库
git init

# 添加所有文件到暂存区
git add .

# 提交所有文件
git commit -m "Initial commit - 个人作品集网站"
```

### 2. 配置 Git 用户信息

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"
```

### 3. 关联远程仓库

```bash
# 添加远程仓库（将 yourusername 替换为你的 GitHub 用户名）
git remote add origin https://github.com/yourusername/work.git

# 如果 remote origin 已存在，先移除再添加
git remote remove origin
git remote add origin https://github.com/yourusername/work.git
```

### 4. 推送到 GitHub

```bash
# 重命名分支为 main（如果是第一次）
git branch -M main

# 推送代码到远程仓库
git push -u origin main
```

### 5. 验证推送成功

访问 `https://github.com/yourusername/work` 查看你的仓库。

---

## 🔄日常工作流程

### 查看当前状态

```bash
# 查看工作目录状态
git status

# 查看具体修改内容
git diff
```

### 提交更改

```bash
# 添加所有更改到暂存区
git add .

# 或者添加单个文件
git add index.html

# 提交更改
git commit -m "提交说明"

# 推送到远程仓库
git push
```

### 更新本地代码

```bash
# 从远程仓库拉取最新代码
git pull origin main
```

---

## 🏷 Git 常用命令速查

| 命令 | 说明 |
|------|------|
| `git init` | 初始化新仓库 |
| `git clone <url>` | 克隆远程仓库 |
| `git add .` | 添加所有文件到暂存区 |
| `git commit -m "message"` | 提交更改 |
| `git push` | 推送到远程仓库 |
| `git pull` | 拉取远程更新 |
| `git status` | 查看状态 |
| `git log` | 查看提交历史 |
| `git branch` | 查看分支 |
| `git checkout -b <branch>` | 创建并切换分支 |

---

## 🔀 分支管理（可选）

### 创建新分支

```bash
# 创建并切换到新分支
git checkout -b feature/new-feature

# 推送新分支到远程
git push -u origin feature/new-feature
```

### 合并分支

```bash
# 切换到 main 分支
git checkout main

# 合并新分支
git merge feature/new-feature

# 推送合并结果
git push
```

---

## ⚠️ 常见问题解决

### 问题 1：无法推送，提示 authentication failed

**解决方法：**
```bash
# 使用 Personal Access Token 代替密码
# 或配置 SSH Key
git remote set-url origin https://github.com/yourusername/work.git
```

### 问题 2：合并冲突

**解决方法：**
```bash
# 手动编辑冲突文件
# 然后
git add .
git commit -m "解决合并冲突"
git push
```

### 问题 3：想撤销上一次的 commit

**解决方法：**
```bash
# 撤销 commit 但保留更改
git reset --soft HEAD~1

# 撤销 commit 并删除更改
git reset --hard HEAD~1
```

---

## 📦 .gitignore 文件建议

建议在项目根目录创建 `.gitignore` 文件：

```
# Node.js
node_modules/
npm-debug.log*

# 数据库
*.sqlite
*.db

# IDE
.vscode/
.idea/

# 操作系统
.DS_Store
Thumbs.db

# 日志
*.log

# 临时文件
*.tmp
*.temp
```

---

## 🌐 设置 GitHub Pages

1. 进入你的 GitHub 仓库
2. 点击 **Settings**（设置）
3. 左侧菜单选择 **Pages**
4. **Source** 选择：`main` 分支，`/root`
5. 点击 **Save**
6. 等待几分钟，网站将发布到：`https://yourusername.github.io/work`

---

## 💡 提示

- 每次开始工作前，先 `git pull` 拉取最新代码
- 每次完成一个功能后，记得 `git add` 和 `git commit`
- 提交信息要清晰描述做了什么更改
- 定期 `git push` 推送代码到远程仓库