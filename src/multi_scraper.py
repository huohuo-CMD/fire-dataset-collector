#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多源图片采集器 - 支持 Google、Bing、Yahoo、Naver
"""
import re
import time
import requests
from typing import List, Optional
from .utils import create_session_headers, sleep_random


class GoogleScraper:
    """Google 图片爬虫"""

    def __init__(self):
        self.session = requests.Session()

    def collect_urls(self, query: str, max_pages: int = 15) -> List[str]:
        """收集 Google 图片 URL"""
        urls = []
        print(f"    Google 采集: {query}")

        for start in range(0, max_pages * 20, 20):
            url = f"https://www.google.com/search?q={query}&tbm=isch&start={start}"
            try:
                resp = self.session.get(url, headers=create_session_headers(), timeout=15)
                # 提取图片 URL
                matches = re.findall(r'\["(https?://[^"]+\.(?:jpg|jpeg|png))",\d+,\d+\]', resp.text)
                urls.extend(matches)
                sleep_random(1, 2)
            except Exception as e:
                print(f"    Google 错误: {e}")
                break

        return list(dict.fromkeys([u for u in urls if 'gstatic.com' not in u]))


class YahooScraper:
    """Yahoo 图片爬虫"""

    def __init__(self):
        self.session = requests.Session()

    def collect_urls(self, query: str, max_pages: int = 15) -> List[str]:
        """收集 Yahoo 图片 URL"""
        urls = []
        print(f"    Yahoo 采集: {query}")

        for start in range(0, max_pages * 30, 30):
            url = f"https://images.search.yahoo.com/search/images?p={query}&b={start}"
            try:
                resp = self.session.get(url, headers=create_session_headers(), timeout=15)
                matches = re.findall(r'"ou":"(https?://[^"]+)"', resp.text)
                urls.extend(matches)
                sleep_random(0.5, 1)
            except Exception as e:
                print(f"    Yahoo 错误: {e}")
                break

        return list(dict.fromkeys(urls))


class NaverScraper:
    """Naver 图片爬虫 (韩国，但有中文图片)"""

    def __init__(self):
        self.session = requests.Session()

    def collect_urls(self, query: str, max_pages: int = 10) -> List[str]:
        """收集 Naver 图片 URL"""
        urls = []
        print(f"    Naver 采集: {query}")

        for start in range(0, max_pages * 48, 48):
            url = f"https://search.pstatic.net/common/?type=all&size=large&query={query}&resnum=0&grouping=photo&start={start}"
            try:
                resp = self.session.get(url, headers=create_session_headers(), timeout=15)
                matches = re.findall(r'"image_url":"(https?://[^"]+)"', resp.text)
                urls.extend(matches)
                sleep_random(0.5, 1)
            except Exception as e:
                print(f"    Naver 错误: {e}")
                break

        return list(dict.fromkeys(urls))


class MultiSourceDownloader:
    """多源下载器"""

    def __init__(self):
        self.sources = {
            'baidu': None,  # 使用 baidu_scraper
            'google': GoogleScraper(),
            'yahoo': YahooScraper(),
            'naver': NaverScraper(),
        }

    def collect_from_all(self, query: str) -> List[str]:
        """从所有源收集"""
        all_urls = []

        for name, scraper in self.sources.items():
            if scraper is None:
                continue
            try:
                urls = scraper.collect_urls(query)
                all_urls.extend(urls)
                sleep_random(1, 2)
            except Exception as e:
                print(f"  {name} 采集失败: {e}")

        return list(dict.fromkeys(all_urls))

    def download(self, url: str) -> Optional[bytes]:
        """下载图片"""
        try:
            resp = requests.get(url, headers=create_session_headers(), timeout=15)
            if resp.status_code == 200:
                return resp.content
        except:
            pass
        return None