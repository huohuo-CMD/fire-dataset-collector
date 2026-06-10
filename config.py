#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 - 机房火灾预警数据集采集器
"""
from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent.parent / 'dataset'
BASE_DIR.mkdir(parents=True, exist_ok=True)

# 日志路径
LOG_DIR = Path(__file__).parent.parent / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# HTTP 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://image.baidu.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 请求延时（秒）
REQUEST_DELAY = 0.5
PAGE_DELAY = 1.0

# 每批次采集数量
BATCH_SIZE = 500

# 每个关键词采集上限
MAX_PER_KEYWORD = 500

# 重试次数
MAX_RETRIES = 3

# 图片最小大小（字节）
MIN_IMAGE_SIZE = 5000

# 数据集类别配置
CATEGORIES = {
    'positive': {
        'data_center_fire': {
            'name': '数据中心火灾',
            'keywords': [
                '数据中心火灾', '机房着火', '服务器着火', 'IDC火灾',
                '机房火灾现场', '机柜烧毁', '云数据中心火灾', '机房短路起火',
                '电气火灾', 'UPS电池火灾', '电力机房起火', '服务器机房起火',
                'data center fire', 'server room fire', 'computer room fire',
                'server rack fire', 'cloud data center blaze'
            ]
        },
        'wire_aging': {
            'name': '电线老化',
            'keywords': [
                '电线老化', '电缆老化', '绝缘层破损', '老化电缆', '破皮电线',
                '铜线裸露', '电线短路', '线路起火', '配电箱老化', '插座老化',
                '插头烧焦', '线路发热', '电源线老化', 'electrical wire aging',
                'cable degradation', 'frayed wire', 'exposed wiring'
            ]
        },
        'battery_failure': {
            'name': '锂电池故障',
            'keywords': [
                '锂电池着火', '电池鼓包', '电池热失控', '电动车起火',
                '储能电站火灾', 'UPS电池起火', '电池冒烟', '电芯泄漏',
                '电池膨胀', '移动电源爆炸', '手机电池起火', 'lithium battery fire',
                'battery swelling', 'thermal runaway', 'battery explosion'
            ]
        },
        'smoke': {
            'name': '烟雾',
            'keywords': [
                '火灾烟雾', '浓烟', '机房烟雾', '服务器冒烟', '设备烟雾',
                '电气烟雾', '塑料燃烧烟', '电线烟雾', '焦烟', '黑烟',
                '起火冒烟', '电线短路烟', '燃烧烟雾', '阴燃烟', '烟雾报警器',
                'fire smoke', 'dense smoke', 'smoke from fire', 'burning smoke'
            ]
        },
        'equipment_overheat': {
            'name': '设备过热',
            'keywords': [
                '设备过热', '服务器过热', '路由器发烫', '设备高温', '过热报警',
                'CPU过热', '显卡高温', '交换机发热', '路由器过热', '散热不良',
                '温度过高', '热成像异常', 'equipment overheating', 'server overheating',
                'device overheating', 'thermal imaging anomaly'
            ]
        },
        'electric_arc': {
            'name': '电弧/打火',
            'keywords': [
                '电弧放电', '电火花', '电气打火', '拉弧', '闪络', '电闸打火',
                '开关打火', '短路电弧', '高压电弧', '电容器放电', '配电箱打火',
                '插座打火', 'electric arc', 'electrical spark', 'arc flash',
                'arcing fault', 'switching arc'
            ]
        }
    },
    'negative': {
        'normal_light': {
            'name': '正常电灯',
            'keywords': [
                '日光灯', 'LED灯', '荧光灯', '白炽灯', '办公室灯光', '机房照明',
                '应急照明', '绿色指示灯', '蓝色指示灯', '电源指示灯',
                '正常运行指示灯', 'fluorescent light', 'LED lamp', 'office lighting'
            ]
        },
        'normal_device': {
            'name': '正常设备',
            'keywords': [
                '服务器机房', '正常运行服务器', '机柜', '路由器正常', '交换机正常',
                '防火墙正常', '存储设备', '磁带库', '光纤交换机', '负载均衡器',
                'server rack', 'network equipment', 'normal server room',
                'server rack normal', 'IT equipment normal'
            ]
        },
        'static_discharge': {
            'name': '静电放电',
            'keywords': [
                '静电放电', '静电现象', '防静电地板', '静电手环', '防静电服',
                '静电测试', '离子风机', 'ESD', 'static electricity',
                'electrostatic discharge', 'ESD spark', 'static discharge'
            ]
        },
        'sunlight_reflection': {
            'name': '阳光反射',
            'keywords': [
                '阳光反射', '金属反光', '镜面反射', '不锈钢反光', '铝合金反光',
                '塑料反光', '玻璃反光', '显示器反光', '屏幕反光', '窗户反光',
                '地板抛光', '光滑表面', 'sunlight reflection', 'metal reflection',
                'glare', 'light reflection', 'specular reflection'
            ]
        }
    }
}

# 统计信息
STATS_FILE = BASE_DIR / 'stats.json'