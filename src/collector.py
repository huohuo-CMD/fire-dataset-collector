#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主采集器 - 机房火灾预警数据集
"""
import os
import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime

# 添加父目录和当前目录到路径
BASE_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_PATH))
sys.path.insert(0, str(Path(__file__).parent))

from config import BASE_DIR, CATEGORIES, STATS_FILE, MIN_IMAGE_SIZE, MAX_PER_KEYWORD
from src.utils import safe_filename, is_valid_image, get_image_hash, sleep_random, count_images_in_dir
from src.baidu_scraper import BaiduScraper
from src.bing_scraper import BingScraper
from src.multi_scraper import MultiSourceDownloader


class DatasetCollector:
    """数据集采集器"""

    def __init__(self):
        self.baidu = BaiduScraper()
        self.bing = BingScraper()
        self.multi = MultiSourceDownloader()
        self.session_hashes = set()  # 去重
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'total_downloaded': 0,
            'categories': {},
            'keywords': {}
        }
        self.deadline = time.time() + 350 * 60 - 30  # 提前 30 秒结束

    def save_stats(self):
        """保存统计信息"""
        self.stats['end_time'] = datetime.now().isoformat()
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)

    def download_single_image(self, url: str, category: str, keyword: str, folder: Path, index: int) -> bool:
        """下载单个图片"""
        filename = safe_filename(keyword, url, index)
        filepath = folder / filename

        # 跳过已存在的
        if filepath.exists():
            return False

        # 下载
        content = self.baidu.download_image(url)
        if not content:
            content = self.bing.download_image(url)

        if not content:
            return False

        # 验证
        if not is_valid_image(content):
            return False

        # 去重
        img_hash = get_image_hash(content)
        if img_hash in self.session_hashes:
            return False
        self.session_hashes.add(img_hash)

        # 保存
        try:
            with open(filepath, 'wb') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"    保存失败: {e}")
            return False

    def process_keyword(self, category: str, folder_name: str, keyword: str, save_dir: Path, target: int = 300) -> dict:
        """处理单个关键词"""
        print(f"\n  [{folder_name}] {keyword}")

        # 多源收集 URL（百度 + Bing + Google + Yahoo）
        baidu_urls = self.baidu.collect_urls(keyword, max_pages=10, max_urls=500)
        sleep_random(0.5, 1)

        bing_urls = self.bing.collect_urls(keyword, max_pages=8, max_urls=300)
        sleep_random(0.5, 1)

        # 多源补充
        try:
            extra_urls = self.multi.collect_from_all(keyword)
        except:
            extra_urls = []

        all_urls = list(dict.fromkeys(baidu_urls + bing_urls + extra_urls))
        print(f"    共获取 {len(all_urls)} 个 URL")

        # 下载
        save_path = save_dir / folder_name
        save_path.mkdir(parents=True, exist_ok=True)

        downloaded = 0
        for i, url in enumerate(all_urls):
            # 检查时间
            if time.time() > self.deadline:
                print(f"    时间到，停止采集")
                break

            if self.download_single_image(url, folder_name, keyword, save_path, i):
                downloaded += 1

            if downloaded >= target:
                break

            if i % 20 == 0:
                print(f"    进度: {downloaded}/{target}")
                sys.stdout.flush()

            sleep_random(0.05, 0.15)  # 快速采集

        print(f"    完成: {downloaded} 张")

        return {
            'keyword': keyword,
            'total_urls': len(all_urls),
            'downloaded': downloaded,
            'folder': folder_name
        }

    def process_category(self, category_name: str, category_info: dict, category_type: str) -> dict:
        """处理整个类别"""
        print(f"\n{'='*60}")
        print(f"类别: {category_name} ({category_type})")
        print(f"{'='*60}")

        results = []
        save_dir = BASE_DIR / category_type

        for keyword in category_info['keywords']:
            result = self.process_keyword(
                category_name,
                category_name,
                keyword,
                save_dir,
                target=300
            )
            results.append(result)

            # 每处理完一个关键词保存一次进度
            self.save_stats()
            sleep_random(2, 4)

        return {
            'category': category_name,
            'results': results,
            'total_downloaded': sum(r['downloaded'] for r in results)
        }

    def run(self):
        """运行采集"""
        print("="*70)
        print("机房火灾预警数据集采集器")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

        # 处理正样本
        print("\n\n>>> 正样本采集开始 <<<")
        for category_name, category_info in CATEGORIES['positive'].items():
            result = self.process_category(category_name, category_info, 'positive')
            self.stats['categories'][f"positive/{category_name}"] = result['total_downloaded']
            sleep_random(5, 10)

        # 处理负样本
        print("\n\n>>> 负样本采集开始 <<<")
        for category_name, category_info in CATEGORIES['negative'].items():
            result = self.process_category(category_name, category_info, 'negative')
            self.stats['categories'][f"negative/{category_name}"] = result['total_downloaded']
            sleep_random(5, 10)

        # 最终统计
        self.print_summary()
        self.save_stats()

        print("\n\n采集完成!")

    def print_summary(self):
        """打印汇总"""
        print("\n" + "="*70)
        print("采集汇总")
        print("="*70)

        counts = count_images_in_dir(BASE_DIR)
        total = 0

        for category_type in ['positive', 'negative']:
            type_dir = BASE_DIR / category_type
            if not type_dir.exists():
                continue

            print(f"\n【{category_type.upper()}】")
            type_total = 0

            for subdir in sorted(type_dir.iterdir()):
                if subdir.is_dir():
                    count = len(list(subdir.glob('*.jpg'))) + len(list(subdir.glob('*.png')))
                    type_total += count
                    print(f"  {subdir.name}: {count}")

            print(f"  小计: {type_total}")
            total += type_total

        print(f"\n总计: {total} 张图片")
        self.stats['total_downloaded'] = total


def main():
    """主入口"""
    collector = DatasetCollector()
    collector.run()


if __name__ == "__main__":
    main()