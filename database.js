const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const bcrypt = require('bcryptjs');

const dbPath = path.join(__dirname, 'database.sqlite');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('数据库连接失败:', err.message);
    } else {
        console.log('数据库连接成功');
        initDatabase();
    }
});

function initDatabase() {
    db.serialize(() => {
        db.run(`CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )`, (err) => {
            if (err) console.error('创建articles表失败:', err.message);
        });

        db.run(`CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            tech_stack TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )`, (err) => {
            if (err) console.error('创建projects表失败:', err.message);
        });

        db.run(`CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )`, (err) => {
            if (err) console.error('创建users表失败:', err.message);
        });

        insertInitialData();
    });
}

function insertInitialData() {
    db.get('SELECT COUNT(*) AS count FROM articles', (err, row) => {
        if (err) {
            console.error('查询articles失败:', err.message);
            return;
        }
        if (row && row.count === 0) {
            const articles = [
                { title: '代码筑界，像素生光', content: '以HTML搭建骨架，用CSS雕琢肌理，让每一段代码都兼具逻辑与美感。', category: '技术' },
                { title: '深耕前端方寸，重构视觉万象', content: '用标准化语义化代码，打造流畅、高效、适配全端的网页体验。', category: '技术' },
                { title: '以技术为笔，以设计为墨', content: '依托HTML5全新特性与CSS3动态样式，解锁网页交互无限可能。', category: '设计' },
                { title: '摒弃冗余代码，坚守极简美学', content: '用简洁规范的前端语法，实现性能与视觉的双向极致。', category: '技术' },
                { title: '跨越屏幕边界，适配多元场景', content: '响应式布局自适应设备尺寸，让网页呈现始终恰到好处。', category: '技术' },
                { title: '细节雕琢质感，动态赋予活力', content: '通过过渡动画、光影层级、留白构图，让静态页面拥有动态生命力。', category: '设计' }
            ];

            articles.forEach(article => {
                db.run('INSERT INTO articles (title, content, category) VALUES (?, ?, ?)',
                    [article.title, article.content, article.category]);
            });
            console.log('初始化文章数据完成');
        }
    });

    db.get('SELECT COUNT(*) AS count FROM projects', (err, row) => {
        if (err) {
            console.error('查询projects失败:', err.message);
            return;
        }
        if (row && row.count === 0) {
            const projects = [
                { name: '电商管理平台', description: '基于Vue3 + TypeScript开发的电商管理后台系统', category: '前端项目', tech_stack: 'Vue3 / TypeScript' },
                { name: '健康管理App', description: '健康管理类移动应用，支持步数统计、饮食记录', category: '移动端', tech_stack: 'React Native' },
                { name: '个人作品集网站', description: '使用HTML5 + CSS3构建的现代化个人作品集网站', category: 'UI设计', tech_stack: 'HTML5 / CSS3' },
                { name: '数据可视化图表库', description: '基于Canvas开发的轻量级图表库', category: '开源项目', tech_stack: 'JavaScript / Canvas' },
                { name: '技术博客平台', description: '基于Next.js开发的现代化博客平台', category: '前端项目', tech_stack: 'Next.js / React' },
                { name: '任务管理系统', description: '支持任务创建、分类、优先级设置的任务管理应用', category: '前端项目', tech_stack: 'Vue3 / Pinia' }
            ];

            projects.forEach(project => {
                db.run('INSERT INTO projects (name, description, category, tech_stack) VALUES (?, ?, ?, ?)',
                    [project.name, project.description, project.category, project.tech_stack]);
            });
            console.log('初始化项目数据完成');
        }
    });

    db.get('SELECT COUNT(*) AS count FROM users', (err, row) => {
        if (err) {
            console.error('查询users失败:', err.message);
            return;
        }
        if (row && row.count === 0) {
            const adminPassword = bcrypt.hashSync('admin123', 10);
            db.run('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                ['admin', 'admin@example.com', adminPassword], (err) => {
                    if (err) {
                        console.error('创建管理员用户失败:', err.message);
                    } else {
                        console.log('管理员用户创建完成: admin / admin123');
                    }
                });
        }
    });
}

module.exports = db;