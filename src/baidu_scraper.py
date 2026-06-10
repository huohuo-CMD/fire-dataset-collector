#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度图片爬虫
"""
import re
import json
import time
import requests
from typing import List, Optional
from .utils import create_session_headers, parse_json_url, parse_pn, sleep_random


class BaiduScraper:
    """百度图片爬虫"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(create_session_headers())
        self.session.headers['Referer'] = 'https://image.baidu.com/'

    def get_headers(self):
        """获取更新后的请求头"""
        headers = create_session_headers()
        headers['Referer'] = 'https://image.baidu.com/'
        return headers

    def fetch_json_api(self, query: str, pn: int = 0, rn: int = 60) -> List[str]:
        """从 JSON API 获取图片 URL"""
        urls = []
        url = parse_json_url(query, pn, rn)

        try:
            resp = self.session.get(url, headers=self.get_headers(), timeout=15)
            resp.encoding = 'utf-8'
            data = resp.json()

            for item in data.get('data', []):
                thumb_url = item.get('thumbURL')
                middle_url = item.get('middleURL')
                obj_url = item.get('objURL')

                if thumb_url:
                    urls.append(thumb_url)
                elif middle_url:
                    urls.append(middle_url)
                elif obj_url and not obj_url.startswith('http://hbimg'):
                    urls.append(obj_url)

        except Exception as e:
            print(f"    JSON API 错误: {e}")

        return urls

    def fetch_html_page(self, query: str, pn: int = 0) -> List[str]:
        """从 HTML 页面提取图片 URL"""
        urls = []
        url = parse_pn(query, pn)

        try:
            resp = self.session.get(url, headers=self.get_headers(), timeout=15)
            resp.encoding = 'utf-8'
            text = resp.text

            # 提取 thumbURL
            matches = re.findall(r'"thumbURL"\s*:\s*"([^"]+)"', text)
            urls.extend(matches)

            # 提取 middleURL
            matches = re.findall(r'"middleURL"\s*:\s*"([^"]+)"', text)
            urls.extend(matches)

            # 提取 objURL (排除百度图片自身的 CDN)
            matches = re.findall(r'"objURL"\s*:\s*"([^"]+)"', text)
            urls.extend([u for u in matches if not u.startswith('http://hbimg')])

        except Exception as e:
            print(f"    HTML 解析错误: {e}")

        return urls

    def collect_urls(self, query: str, max_pages: int = 10, max_urls: int = 500) -> List[str]:
        """收集单个关键词的所有图片 URL"""
        all_urls = []

        print(f"    采集关键词: {query}")

        # JSON API (更稳定)
        for pn in range(0, max_pages * 60, 60):
            urls = self.fetch_json_api(query, pn)
            if not urls:
                break
            all_urls.extend(urls)
            sleep_random(0.3, 0.6)

            if len(all_urls) >= max_urls:
                break

        # HTML 页面 (补充)
        for pn in range(0, max_pages * 20, 20):
            urls = self.fetch_html_page(query, pn)
            if not urls:
                break
            all_urls.extend(urls)
            sleep_random(0.5, 1.0)

            if len(all_urls) >= max_urls * 1.5:
                break

        # 去重
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


def test_scraper():
    """测试爬虫"""
    scraper = BaiduScraper()
    urls = scraper.collect_urls('数据中心火灾', max_pages=2, max_urls=20)
    print(f"\n测试结果: 获取 {len(urls)} 个 URL")
    for url in urls[:5]:
        print(f"  - {url[:80]}")


if __name__ == "__main__":
    test_scraper()