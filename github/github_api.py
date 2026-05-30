#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending API - 用于 Node.js 后端调用的简单 API
"""

import json
import sqlite3
import sys
import os

def get_trending(period='daily', limit=20):
    """获取趋势榜数据"""
    db_path = os.path.join(os.path.dirname(__file__), 'github_trending.db')
    
    if not os.path.exists(db_path):
        return {'success': False, 'error': '数据库文件不存在，请先运行 github_tracker.py 抓取数据', 'data': []}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query = "SELECT author, repo_name, description, stars, forks, today_stars, url, language, trend_period, crawled_at FROM repositories WHERE 1=1"
        params = []
        
        if period and period != 'all':
            query += " AND trend_period = ?"
            params.append(period)
        
        query += " ORDER BY stars DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'author': row[0],
                'repo_name': row[1],
                'description': row[2] or '',
                'stars': row[3],
                'forks': row[4],
                'today_stars': row[5],
                'url': row[6],
                'language': row[7] or '',
                'trend_period': row[8],
                'crawled_at': row[9]
            })
        
        return {'success': True, 'data': data, 'count': len(data)}
        
    except Exception as e:
        return {'success': False, 'error': str(e), 'data': []}

def get_languages():
    """获取所有可用的编程语言"""
    db_path = os.path.join(os.path.dirname(__file__), 'github_trending.db')
    
    if not os.path.exists(db_path):
        return {'success': False, 'error': '数据库文件不存在', 'languages': []}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT language FROM repositories WHERE language IS NOT NULL AND language != '' ORDER BY language")
        rows = cursor.fetchall()
        conn.close()
        
        languages = [row[0] for row in rows]
        return {'success': True, 'languages': languages}
        
    except Exception as e:
        return {'success': False, 'error': str(e), 'languages': []}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': '缺少参数'}, ensure_ascii=False))
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'trending':
        period = sys.argv[2] if len(sys.argv) > 2 else 'daily'
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        result = get_trending(period, limit)
        print(json.dumps(result, ensure_ascii=False))
    
    elif action == 'languages':
        result = get_languages()
        print(json.dumps(result, ensure_ascii=False))
    
    else:
        print(json.dumps({'success': False, 'error': '未知操作'}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
