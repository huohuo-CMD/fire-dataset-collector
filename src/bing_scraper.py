#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bing 图片爬虫
"""
import re
import time
import requests
from typing import List, Optional
from .utils import create_session_headers, sleep_random


class BingScraper:
    """Bing 图片爬虫"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(create_session_headers())

    def get_headers(self):
        """获取更新后的请求头"""
        return create_session_headers()

    def fetch_page(self, query: str, offset: int = 0) -> List[str]:
        """从 Bing 图片页面获取 URL"""
        urls = []
        url = f"https://cn.bing.com/images/async?q={query}&first={offset}&count=35"

        try:
            resp = self.session.get(url, headers=self.get_headers(), timeout=15)
            resp.encoding = 'utf-8'
            text = resp.text

            # 提取图片 URL
            matches = re.findall(r'mediaurl="([^"]+)"', text)
            urls.extend(matches)

            # 提取缩略图 URL
            matches = re.findall(r'thumbUrl":"([^"]+)"', text)
            urls.extend(matches)

        except Exception as e:
            print(f"    Bing 错误: {e}")

        return urls

    def collect_urls(self, query: str, max_pages: int = 10, max_urls: int = 300) -> List[str]:
        """收集单个关键词的所有图片 URL"""
        all_urls = []

        print(f"    Bing 采集: {query}")

        for offset in range(0, max_pages * 35, 35):
            urls = self.fetch_page(query, offset)
            if not urls:
                break
            all_urls.extend(urls)
            sleep_random(0.5, 1.0)

            if len(all_urls) >= max_urls:
                break

        return list(dict.fromkeys(all_urls))

    def download_image(self, url: str) -> Optional[bytes]:
        """下载图片内容"""
        try:
            resp = requests.get(url, headers=self.get_headers(), timeout=20)
            if resp.status_code == 200:
                return resp.content
        except Exception as e:
            print(f"    下载失败: {e}")
        return None


def test_bing_scraper():
    """测试 Bing 爬虫"""
    scraper = BingScraper()
    urls = scraper.collect_urls('data center fire', max_pages=2, max_urls=20)
    print(f"\nBing 测试结果: 获取 {len(urls)} 个 URL")


if __name__ == "__main__":
    test_bing_scraper()