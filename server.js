const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const db = require('./database');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = 'your-secret-key-change-in-production';
const SALT_ROUNDS = 10;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// API 路由应该在静态文件服务之前定义
app.get('/', (req, res) => {
    res.json({ message: '欢迎来到个人作品集 API', version: '1.0.0' });
});

function generateToken(user) {
    return jwt.sign(
        { id: user.id, username: user.username, email: user.email },
        JWT_SECRET,
        { expiresIn: '7d' }
    );
}

function verifyToken(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: '未提供Token，请先登录' });
    }

    const token = authHeader.substring(7);

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token已过期，请重新登录' });
        }
        return res.status(401).json({ error: '无效的Token' });
    }
}

app.get('/api/articles', (req, res) => {
    db.all('SELECT * FROM articles ORDER BY created_at DESC', (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ success: true, data: rows });
        }
    });
});

app.get('/api/articles/:id', (req, res) => {
    const id = req.params.id;
    db.get('SELECT * FROM articles WHERE id = ?', [id], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (!row) {
            res.status(404).json({ error: '文章不存在' });
        } else {
            res.json({ success: true, data: row });
        }
    });
});

app.post('/api/articles', verifyToken, (req, res) => {
    const { title, content, category } = req.body;
    if (!title || !content) {
        return res.status(400).json({ error: '标题和内容不能为空' });
    }

    db.run('INSERT INTO articles (title, content, category) VALUES (?, ?, ?)',
        [title, content, category || '其他'],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
            } else {
                res.json({
                    success: true,
                    message: '文章创建成功',
                    id: this.lastID
                });
            }
        }
    );
});

app.put('/api/articles/:id', verifyToken, (req, res) => {
    const id = req.params.id;
    const { title, content, category } = req.body;

    db.run('UPDATE articles SET title = ?, content = ?, category = ? WHERE id = ?',
        [title, content, category, id],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
            } else if (this.changes === 0) {
                res.status(404).json({ error: '文章不存在' });
            } else {
                res.json({ success: true, message: '文章更新成功' });
            }
        }
    );
});

app.delete('/api/articles/:id', verifyToken, (req, res) => {
    const id = req.params.id;

    db.run('DELETE FROM articles WHERE id = ?', [id], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (this.changes === 0) {
            res.status(404).json({ error: '文章不存在' });
        } else {
            res.json({ success: true, message: '文章删除成功' });
        }
    });
});

app.get('/api/projects', (req, res) => {
    db.all('SELECT * FROM projects ORDER BY created_at DESC', (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ success: true, data: rows });
        }
    });
});

app.get('/api/projects/:id', (req, res) => {
    const id = req.params.id;
    db.get('SELECT * FROM projects WHERE id = ?', [id], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (!row) {
            res.status(404).json({ error: '项目不存在' });
        } else {
            res.json({ success: true, data: row });
        }
    });
});

app.post('/api/projects', verifyToken, (req, res) => {
    const { name, description, category, tech_stack } = req.body;
    if (!name) {
        return res.status(400).json({ error: '项目名称不能为空' });
    }

    db.run('INSERT INTO projects (name, description, category, tech_stack) VALUES (?, ?, ?, ?)',
        [name, description || '', category || '其他', tech_stack || ''],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
            } else {
                res.json({
                    success: true,
                    message: '项目创建成功',
                    id: this.lastID
                });
            }
        }
    );
});

app.post('/api/register', async (req, res) => {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
        return res.status(400).json({ error: '用户名、邮箱和密码不能为空' });
    }

    if (username.length < 3) {
        return res.status(400).json({ error: '用户名至少需要3个字符' });
    }

    if (password.length < 6) {
        return res.status(400).json({ error: '密码至少需要6个字符' });
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return res.status(400).json({ error: '请输入有效的邮箱地址' });
    }

    try {
        const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);

        db.run('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            [username, email, hashedPassword],
            function(err) {
                if (err) {
                    if (err.message.includes('UNIQUE constraint failed: users.username')) {
                        return res.status(400).json({ error: '用户名已存在' });
                    }
                    if (err.message.includes('UNIQUE constraint failed: users.email')) {
                        return res.status(400).json({ error: '邮箱已被注册' });
                    }
                    return res.status(500).json({ error: err.message });
                }

                const user = { id: this.lastID, username, email };
                const token = generateToken(user);

                res.json({
                    success: true,
                    message: '注册成功',
                    token: token,
                    user: { id: user.id, username: user.username, email: user.email }
                });
            }
        );
    } catch (err) {
        res.status(500).json({ error: '密码加密失败' });
    }
});

app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: '用户名和密码不能为空' });
    }

    db.get('SELECT * FROM users WHERE username = ?', [username], async (err, user) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }

        if (!user) {
            return res.status(401).json({ error: '用户名或密码错误' });
        }

        try {
            const isPasswordValid = await bcrypt.compare(password, user.password);

            if (!isPasswordValid) {
                return res.status(401).json({ error: '用户名或密码错误' });
            }

            const token = generateToken(user);

            res.json({
                success: true,
                message: '登录成功',
                token: token,
                user: { id: user.id, username: user.username, email: user.email }
            });
        } catch (err) {
            res.status(500).json({ error: '密码验证失败' });
        }
    });
});

app.get('/api/user/info', verifyToken, (req, res) => {
    res.json({
        success: true,
        user: req.user
    });
});

app.post('/api/user/logout', (req, res) => {
    res.json({
        success: true,
        message: '退出登录成功'
    });
});

// GitHub 热点追踪器 API
app.get('/api/github/trending', (req, res) => {
    const { period = 'daily', limit = 20 } = req.query;
    
    const githubApiPath = path.join(__dirname, 'github', 'github_api.py');
    
    if (!fs.existsSync(githubApiPath)) {
        return res.status(500).json({ 
            success: false, 
            error: 'GitHub API 脚本不存在',
            data: [] 
        });
    }
    
    exec(`python "${githubApiPath}" trending ${period} ${limit}`, { encoding: 'utf-8' }, (error, stdout, stderr) => {
        if (error) {
            console.error('GitHub API 错误:', error);
            return res.status(500).json({ 
                success: false, 
                error: '调用 GitHub API 失败: ' + error.message,
                data: [] 
            });
        }
        
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (parseError) {
            console.error('JSON 解析错误:', parseError);
            res.status(500).json({ 
                success: false, 
                error: '数据解析失败',
                data: [] 
            });
        }
    });
});

app.get('/api/github/languages', (req, res) => {
    const githubApiPath = path.join(__dirname, 'github', 'github_api.py');
    
    if (!fs.existsSync(githubApiPath)) {
        return res.status(500).json({ 
            success: false, 
            error: 'GitHub API 脚本不存在',
            languages: [] 
        });
    }
    
    exec(`python "${githubApiPath}" languages`, { encoding: 'utf-8' }, (error, stdout, stderr) => {
        if (error) {
            console.error('GitHub API 错误:', error);
            return res.status(500).json({ 
                success: false, 
                error: '调用 GitHub API 失败: ' + error.message,
                languages: [] 
            });
        }
        
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (parseError) {
            console.error('JSON 解析错误:', parseError);
            res.status(500).json({ 
                success: false, 
                error: '数据解析失败',
                languages: [] 
            });
        }
    });
});

app.use(express.static(__dirname));

app.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
    console.log('API 接口列表:');
    console.log('GET    /api/articles       - 获取所有文章（公开）');
    console.log('GET    /api/articles/:id  - 获取单篇文章（公开）');
    console.log('POST   /api/articles      - 创建文章（需Token）');
    console.log('PUT    /api/articles/:id  - 更新文章（需Token）');
    console.log('DELETE /api/articles/:id  - 删除文章（需Token）');
    console.log('GET    /api/projects      - 获取所有项目（公开）');
    console.log('GET    /api/projects/:id  - 获取单个项目（公开）');
    console.log('POST   /api/projects      - 创建项目（需Token）');
    console.log('POST   /api/register      - 用户注册');
    console.log('POST   /api/login         - 用户登录');
    console.log('GET    /api/user/info     - 获取用户信息（需Token）');
    console.log('POST   /api/user/logout   - 退出登录');
    console.log('GET    /api/github/trending - 获取 GitHub 热点（公开）');
    console.log('GET    /api/github/languages - 获取可用编程语言（公开）');
});