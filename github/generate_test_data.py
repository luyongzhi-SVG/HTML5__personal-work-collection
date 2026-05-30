#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from datetime import datetime

# 测试数据
test_data = [
    {"author": "colbymchenry", "repo_name": "codegraph", "description": "Pre-indexed code knowledge graph for Claude Code, Codex, Gemini, Cursor, OpenCode, AntiGravity, Kiro, and Hermes Agent — fewer tokens, fewer tool calls, 100% local", "stars": 12580, "forks": 890, "today_stars": 234, "url": "https://github.com/colbymchenry/codegraph", "language": "Python", "trend_period": "daily"},
    {"author": "CloakHQ", "repo_name": "CloakBrowser", "description": "Stealth Chromium that passes every bot detection test. Drop-in Playwright replacement with source-level fingerprint patches. 30/30 tests passed.", "stars": 8765, "forks": 567, "today_stars": 156, "url": "https://github.com/CloakHQ/CloakBrowser", "language": "TypeScript", "trend_period": "daily"},
    {"author": "Lum1104", "repo_name": "Understand-Anything", "description": "Graphs that teach > graphs that impress. Turn any code into an interactive knowledge graph you can explore, search, and ask questions about.", "stars": 6543, "forks": 345, "today_stars": 123, "url": "https://github.com/Lum1104/Understand-Anything", "language": "JavaScript", "trend_period": "daily"},
    {"author": "decolua", "repo_name": "9router", "description": "Unlimited FREE AI coding. Connect Claude Code, Codex, Cursor, Cline, Copilot, Antigravity to FREE Claude/GPT/Gemini via 40+ providers.", "stars": 5432, "forks": 456, "today_stars": 98, "url": "https://github.com/decolua/9router", "language": "Rust", "trend_period": "daily"},
    {"author": "ruvnet", "repo_name": "ruflo", "description": "The leading agent orchestration platform for Claude. Deploy intelligent multi-agent swarms, coordinate autonomous workflows.", "stars": 9876, "forks": 678, "today_stars": 345, "url": "https://github.com/ruvnet/ruflo", "language": "Python", "trend_period": "daily"},
    {"author": "bytedance", "repo_name": "UI-TARS-desktop", "description": "The Open-Source Multimodal AI Agent Stack: Connecting Cutting-Edge AI Models and Agent Infra", "stars": 15678, "forks": 1234, "today_stars": 567, "url": "https://github.com/bytedance/UI-TARS-desktop", "language": "Rust", "trend_period": "weekly"},
    {"author": "AIDC-AI", "repo_name": "Pixelle-Video", "description": "AI 全自动短视频引擎 | AI Fully Automated Short Video Engine", "stars": 7654, "forks": 456, "today_stars": 234, "url": "https://github.com/AIDC-AI/Pixelle-Video", "language": "Python", "trend_period": "weekly"},
    {"author": "TauricResearch", "repo_name": "TradingAgents", "description": "TradingAgents: Multi-Agents LLM Financial Trading Framework", "stars": 4321, "forks": 234, "today_stars": 123, "url": "https://github.com/TauricResearch/TradingAgents", "language": "Python", "trend_period": "weekly"},
    {"author": "multica-ai", "repo_name": "andrej-karpathy-skills", "description": "A single CLAUDE.md file to improve Claude Code behavior, derived from Andrej Karpathy's observations.", "stars": 3456, "forks": 189, "today_stars": 89, "url": "https://github.com/multica-ai/andrej-karpathy-skills", "language": "", "trend_period": "weekly"},
    {"author": "1jehuang", "repo_name": "jcode", "description": "Coding Agent Harness", "stars": 2876, "forks": 156, "today_stars": 78, "url": "https://github.com/1jehuang/jcode", "language": "Go", "trend_period": "monthly"},
    {"author": "anthropics", "repo_name": "financial-services", "description": "Financial services with AI integration", "stars": 21000, "forks": 2300, "today_stars": 890, "url": "https://github.com/anthropics/financial-services", "language": "TypeScript", "trend_period": "monthly"},
    {"author": "yikart", "repo_name": "AiToEarn", "description": "Let's use AI to Earn!", "stars": 1890, "forks": 123, "today_stars": 45, "url": "https://github.com/yikart/AiToEarn", "language": "JavaScript", "trend_period": "monthly"},
]

def create_database():
    db_path = os.path.join(os.path.dirname(__file__), 'github_trending.db')
    
    # 删除旧数据库
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # 创建数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repositories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            repo_name TEXT NOT NULL,
            description TEXT,
            stars INTEGER DEFAULT 0,
            forks INTEGER DEFAULT 0,
            today_stars INTEGER DEFAULT 0,
            url TEXT NOT NULL,
            language TEXT,
            trend_period TEXT NOT NULL,
            crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(author, repo_name, trend_period)
        )
    ''')
    
    # 插入测试数据
    inserted = 0
    for item in test_data:
        try:
            cursor.execute('''
                INSERT INTO repositories 
                (author, repo_name, description, stars, forks, today_stars, url, language, trend_period, crawled_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['author'], item['repo_name'], item['description'],
                item['stars'], item['forks'], item['today_stars'],
                item['url'], item['language'], item['trend_period'], datetime.now().isoformat()
            ))
            inserted += 1
        except Exception as e:
            print(f"跳过重复数据: {item['author']}/{item['repo_name']}")
    
    conn.commit()
    conn.close()
    print(f"✅ 已创建数据库并插入 {inserted} 条测试数据")

if __name__ == "__main__":
    create_database()
