#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数
"""
import hashlib
import time
import random
from pathlib import Path
from urllib.parse import quote


def safe_filename(keyword: str, url: str, index: int) -> str:
    """生成安全的文件名"""
    # 使用 URL 的 hash 作为文件名的一部分
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    safe_keyword = keyword[:15].replace(' ', '_').replace('/', '_')
    return f"{safe_keyword}_{url_hash}_{index}.jpg"


def create_session_headers():
    """创建随机化的请求头"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

    return {
        'User-Agent': random.choice(user_agents),
        'Referer': 'https://image.baidu.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }


def is_valid_image(content: bytes) -> bool:
    """检查是否为有效的图片"""
    if len(content) < 5000:
        return False

    # 检查图片格式
    valid_signatures = [
        b'\xff\xd8\xff',  # JPEG
        b'\x89PNG',       # PNG
        b'GIF8',          # GIF
        b'RIFF',          # WebP
        b'BM',            # BMP
    ]

    return any(content.startswith(sig) for sig in valid_signatures)


def get_image_hash(content: bytes) -> str:
    """获取图片内容的哈希"""
    return hashlib.md5(content[:10000]).hexdigest()


def parse_pn(query: str, pn: int) -> str:
    """构建分页 URL"""
    return f"https://image.baidu.com/search/index?tn=baiduimage&word={quote(query)}&pn={pn}"


def parse_json_url(query: str, pn: int = 0, rn: int = 60) -> str:
    """构建 JSON API URL"""
    return f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={quote(query)}&pn={pn}&rn={rn}"


def sleep_random(min_sec: float = 0.3, max_sec: float = 1.0):
    """随机延时"""
    time.sleep(random.uniform(min_sec, max_sec))


def count_images_in_dir(directory: Path) -> dict:
    """统计目录下各类别的图片数量"""
    counts = {}
    if directory.exists():
        for subdir in directory.iterdir():
            if subdir.is_dir():
                counts[subdir.name] = len(list(subdir.glob('*.jpg'))) + len(list(subdir.glob('*.png')))
    return counts


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def log_progress(current: int, total: int, message: str = ""):
    """打印进度"""
    pct = current / total * 100 if total > 0 else 0
    bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
    print(f"\r[{bar}] {pct:.1f}% {message}", end='', flush=True)