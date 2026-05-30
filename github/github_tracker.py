#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3
import os
import time
import schedule
import random
import re
from datetime import datetime
from typing import List, Dict, Optional

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

class GitHubTrending:
    def __init__(self, use_browser=False, proxies=None):
        self.base_url = "https://github.com/trending"
        self.db_path = "github_trending.db"
        self.json_path = "github_trending.json"
        self.use_browser = use_browser
        self.proxies = proxies
        self.browser = None
        self.page = None
        self.is_paused = False
        self.running = True
        self.setup_database()
    
    def setup_database(self):
        """创建数据库表"""
        conn = sqlite3.connect(self.db_path)
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
        
        conn.commit()
        conn.close()
    
    async def init_browser(self):
        """初始化浏览器"""
        if self.browser:
            return
        
        print('正在启动浏览器...')
        playwright = await async_playwright().start()
        
        args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
        ]
        
        self.browser = await playwright.chromium.launch(
            headless=False,
            args=args
        )
        
        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
        )
        
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
                configurable: true
            });
        """)
        
        self.page = await context.new_page()
        print('浏览器启动完成')
    
    async def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None
    
    def _parse_number(self, num_str: str) -> int:
        """解析数字字符串（处理 K/M 后缀）"""
        if not num_str:
            return 0
        
        num_str = num_str.strip().replace(',', '')
        if num_str.endswith('k') or num_str.endswith('K'):
            return int(float(num_str[:-1]) * 1000)
        elif num_str.endswith('m') or num_str.endswith('M'):
            return int(float(num_str[:-1]) * 1000000)
        try:
            return int(num_str)
        except:
            return 0
    
    def _parse_html(self, html: str, period: str) -> List[Dict]:
        """解析 HTML 提取仓库信息"""
        repositories = []
        
        try:
            article_pattern = r'<article[^>]*class="Box-row"[^>]*>(.*?)</article>'
            matches = re.findall(article_pattern, html, re.DOTALL)
            
            if not matches:
                print("⚠️ 未找到仓库列表，可能需要使用浏览器模式")
                return []
            
            print(f"找到 {len(matches)} 个仓库")
            
            for idx, match in enumerate(matches):
                try:
                    author_match = re.search(r'<a href="/([^/"]+)/([^"]+)"[^>]*class="[^"]*Link[^"]*"[^>]*>', match)
                    if not author_match:
                        continue
                    
                    author = author_match.group(1)
                    repo_name = author_match.group(2)
                    
                    desc_match = re.search(r'<p[^>]*class="[^"]*color-fg-muted[^"]*"[^>]*>\s*(.*?)\s*</p>', match, re.DOTALL)
                    description = ""
                    if desc_match:
                        description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
                    
                    lang_match = re.search(r'<span[^>]*itemprop="programmingLanguage"[^>]*>([^<]+)</span>', match)
                    if not lang_match:
                        lang_match = re.search(r'<span[^>]*class="[^"]*text-bold[^"]*"[^>]*>([^<]+)</span>', match)
                    language = lang_match.group(1).strip() if lang_match else ""
                    
                    star_match = re.search(r'([\d,.]+[kKmM]?)\s*stars?', match)
                    stars = self._parse_number(star_match.group(1)) if star_match else 0
                    
                    fork_match = re.search(r'([\d,.]+[kKmM]?)\s*forks?', match)
                    forks = self._parse_number(fork_match.group(1)) if fork_match else 0
                    
                    today_match = re.search(r'<span[^>]*class="[^"]*text-green[^"]*"[^>]*>\s*\+?([\d,.]+[kKmM]?)\s*</span>', match)
                    today_stars = self._parse_number(today_match.group(1)) if today_match else 0
                    
                    url = f"https://github.com/{author}/{repo_name}"
                    
                    repositories.append({
                        "author": author,
                        "repo_name": repo_name,
                        "description": description,
                        "stars": stars,
                        "forks": forks,
                        "today_stars": today_stars,
                        "url": url,
                        "language": language,
                        "trend_period": period,
                        "crawled_at": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    print(f"解析仓库 {idx + 1} 失败: {e}")
                    continue
        
        except Exception as e:
            print(f"解析HTML失败: {e}")
        
        return repositories
    
    async def fetch_trending_browser(self, period: str = "daily", language: str = "") -> List[Dict]:
        """使用浏览器抓取"""
        url = f"{self.base_url}/{language}?since={period}" if language else f"{self.base_url}?since={period}"
        
        try:
            await self.init_browser()
            
            print(f"正在访问: {url}")
            await self.page.goto(url, timeout=60000, wait_until='domcontentloaded')
            
            # 等待页面加载
            await self.page.wait_for_timeout(2000)
            
            # 获取页面HTML
            html = await self.page.content()
            
            return self._parse_html(html, period)
            
        except Exception as e:
            print(f"浏览器抓取失败: {e}")
            return []
    
    def fetch_trending_requests(self, period: str = "daily", language: str = "") -> List[Dict]:
        """使用requests抓取"""
        import requests
        
        url = f"{self.base_url}/{language}?since={period}" if language else f"{self.base_url}?since={period}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://github.com/",
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"尝试第 {attempt + 1}/{max_retries} 次...")
                response = requests.get(url, headers=headers, timeout=30, proxies=self.proxies, verify=False)
                response.raise_for_status()
                print("✓ 请求成功")
                return self._parse_html(response.text, period)
            except Exception as e:
                print(f"第 {attempt + 1} 次请求失败: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
        
        print(f"❌ 已重试 {max_retries} 次，仍然失败")
        return []
    
    async def fetch_trending(self, period: str = "daily", language: str = "") -> List[Dict]:
        """抓取 GitHub 趋势榜"""
        if self.use_browser and HAS_PLAYWRIGHT:
            return await self.fetch_trending_browser(period, language)
        else:
            return self.fetch_trending_requests(period, language)
    
    def save_to_json(self, data: List[Dict], filename: str = None):
        """保存数据到 JSON 文件"""
        path = filename or self.json_path
        try:
            existing_data = []
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            existing_keys = {(item['author'], item['repo_name'], item['trend_period']) for item in existing_data}
            new_count = 0
            for item in data:
                key = (item['author'], item['repo_name'], item['trend_period'])
                if key not in existing_keys:
                    existing_data.append(item)
                    existing_keys.add(key)
                    new_count += 1
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ 已保存 {len(data)} 条记录（新增 {new_count} 条）到 {path}")
        except Exception as e:
            print(f"保存 JSON 失败: {e}")
    
    def save_to_database(self, data: List[Dict]):
        """保存数据到 SQLite 数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inserted = 0
        updated = 0
        
        for item in data:
            try:
                cursor.execute('SELECT id FROM repositories WHERE author=? AND repo_name=? AND trend_period=?',
                            (item['author'], item['repo_name'], item['trend_period']))
                exists = cursor.fetchone()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO repositories 
                    (author, repo_name, description, stars, forks, today_stars, url, language, trend_period, crawled_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['author'], item['repo_name'], item['description'],
                    item['stars'], item['forks'], item['today_stars'],
                    item['url'], item['language'], item['trend_period'], item['crawled_at']
                ))
                
                if exists:
                    updated += 1
                else:
                    inserted += 1
                    
            except Exception as e:
                print(f"保存仓库失败 {item['author']}/{item['repo_name']}: {e}")
        
        conn.commit()
        conn.close()
        print(f"✓ 已保存到数据库（新增 {inserted} 条，更新 {updated} 条）")
    
    def query_database(self, period: str = "", language: str = "") -> List[Dict]:
        """查询数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM repositories WHERE 1=1"
        params = []
        
        if period:
            query += " AND trend_period = ?"
            params.append(period)
        
        if language:
            query += " AND language = ?"
            params.append(language)
        
        query += " ORDER BY stars DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "id": row[0], "author": row[1], "repo_name": row[2], "description": row[3],
                "stars": row[4], "forks": row[5], "today_stars": row[6], "url": row[7],
                "language": row[8], "trend_period": row[9], "crawled_at": row[10]
            })
        
        conn.close()
        return result
    
    def display_trending(self, data: List[Dict], limit: int = 10):
        """控制台格式化展示热点列表"""
        if not data:
            print("暂无数据")
            return
        
        print("\n" + "="*85)
        print(f"🎯 GitHub 热点追踪器 - 共 {len(data)} 个仓库")
        print("="*85)
        
        for i, repo in enumerate(data[:limit], 1):
            period_map = {"daily": "日榜", "weekly": "周榜", "monthly": "月榜"}
            period = period_map.get(repo['trend_period'], repo['trend_period'])
            
            print(f"\n📌 TOP {i}")
            print(f"  🏠 仓库: {repo['author']}/{repo['repo_name']}")
            print(f"  🔗 地址: {repo['url']}")
            print(f"  📝 简介: {repo['description'][:60]}..." if len(repo['description']) > 60 else f"  📝 简介: {repo['description']}")
            print(f"  🎯 周期: {period}")
            print(f"  💻 语言: {repo['language'] if repo['language'] else '未知'}")
            print(f"  ⭐ Stars: {repo['stars']:,}")
            print(f"  🔀 Forks: {repo['forks']:,}")
            print(f"  📈 今日新增: +{repo['today_stars']:,} stars")
        
        print("\n" + "="*85)
    
    async def run_scheduled_task(self, period: str = "daily", language: str = ""):
        """执行定时任务"""
        print(f"\n⏰ 开始抓取 GitHub 趋势榜 ({period})...")
        data = await self.fetch_trending(period, language)
        
        if data:
            self.save_to_json(data)
            self.save_to_database(data)
            self.display_trending(data)
        else:
            print("❌ 未获取到数据")
    
    def pause(self):
        """暂停定时任务"""
        self.is_paused = True
        print("⏸️ 定时任务已暂停")
    
    def resume(self):
        """恢复定时任务"""
        self.is_paused = False
        print("▶️ 定时任务已恢复")
    
    def stop(self):
        """停止定时任务"""
        self.running = False
        print("⏹️ 定时任务已停止")
    
    async def start_scheduler(self, interval_minutes: int = 60):
        """启动定时调度器"""
        print(f"🚀 GitHub 热点追踪器已启动，每 {interval_minutes} 分钟更新一次")
        print("💡 按 Ctrl+C 暂停，输入 'r' 恢复，输入 'q' 退出")
        
        await self.run_scheduled_task("daily")
        
        schedule.every(interval_minutes).minutes.do(lambda: asyncio.create_task(self.run_scheduled_task("daily")))
        
        import threading
        
        def input_handler():
            while self.running:
                try:
                    line = input().strip().lower()
                    if line == 'q' or line == 'quit':
                        self.stop()
                        print("👋 程序即将退出...")
                    elif line == 'p' or line == 'pause':
                        self.pause()
                    elif line == 'r' or line == 'resume':
                        self.resume()
                    elif line == 'h' or line == 'help':
                        print("""
可用命令:
  q / quit   - 退出程序
  p / pause  - 暂停定时任务
  r / resume - 恢复定时任务
  h / help   - 显示帮助
                        """)
                except:
                    pass
        
        input_thread = threading.Thread(target=input_handler, daemon=True)
        input_thread.start()
        
        try:
            while self.running:
                if not self.is_paused:
                    schedule.run_pending()
                else:
                    print("\r⏸️ 任务已暂停，输入 'r' 恢复...", end='')
                time.sleep(1)
        except KeyboardInterrupt:
            self.pause()
            print("\n⏸️ 定时任务已暂停")
            print("输入 'r' 恢复任务，输入 'q' 退出程序")
        
        await self.close_browser()
        print("\n👋 程序已退出")

async def main():
    print('''
╔══════════════════════════════════════════════════════════════╗
║                    GitHub 热点追踪器                        ║
╚══════════════════════════════════════════════════════════════╝
''')
    
    # 选择抓取方式
    use_browser = False
    if HAS_PLAYWRIGHT:
        choice = input("是否使用浏览器模式？(y/n，默认n): ").strip().lower()
        use_browser = choice == 'y'
        if use_browser:
            print("✓ 将使用浏览器模式")
    
    # 代理配置
    use_proxy = input("是否使用代理？(y/n，默认n): ").strip().lower()
    proxies = None
    
    if use_proxy == 'y':
        proxy_url = input("请输入代理地址（例如：http://127.0.0.1:7890）: ").strip()
        if proxy_url:
            proxies = {'http': proxy_url, 'https': proxy_url}
            print(f"✓ 已配置代理: {proxy_url}")
    
    tracker = GitHubTrending(use_browser=use_browser, proxies=proxies)
    
    print('''
╔══════════════════════════════════════════════════════════════╗
║                        操作菜单                              ║
╠══════════════════════════════════════════════════════════════╣
║  1. 抓取日榜                                                  ║
║  2. 抓取周榜                                                  ║
║  3. 抓取月榜                                                  ║
║  4. 按语言筛选抓取                                            ║
║  5. 查看本地数据                                              ║
║  6. 启动定时追踪 (每60分钟)                                   ║
║  0. 退出程序                                                  ║
╚══════════════════════════════════════════════════════════════╝
''')
    
    while True:
        choice = input("请选择操作 (0-6，或输入 quit/q 退出): ").strip().lower()
        
        if choice == '0' or choice == 'quit' or choice == 'q' or choice == 'exit':
            await tracker.close_browser()
            print("👋 退出程序")
            break
        
        elif choice == '1':
            data = await tracker.fetch_trending("daily")
            tracker.save_to_json(data)
            tracker.save_to_database(data)
            tracker.display_trending(data)
        
        elif choice == '2':
            data = await tracker.fetch_trending("weekly")
            tracker.save_to_json(data)
            tracker.save_to_database(data)
            tracker.display_trending(data)
        
        elif choice == '3':
            data = await tracker.fetch_trending("monthly")
            tracker.save_to_json(data)
            tracker.save_to_database(data)
            tracker.display_trending(data)
        
        elif choice == '4':
            language = input("请输入编程语言 (如 Python/Java/Go): ").strip()
            period = input("请选择周期 (daily/weekly/monthly，默认daily): ").strip() or "daily"
            data = await tracker.fetch_trending(period, language)
            tracker.save_to_json(data)
            tracker.save_to_database(data)
            tracker.display_trending(data)
        
        elif choice == '5':
            period = input("请选择周期筛选 (daily/weekly/monthly，留空全部): ").strip()
            language = input("请选择语言筛选 (留空全部): ").strip()
            data = tracker.query_database(period, language)
            tracker.display_trending(data)
        
        elif choice == '6':
            await tracker.start_scheduler()
        
        else:
            print("❌ 无效选择，请输入 0-6")

import asyncio

if __name__ == "__main__":
    asyncio.run(main())