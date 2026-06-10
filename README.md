# 机房火灾预警数据集采集器

基于 GitHub Actions 的自动化图片采集系统，目标采集 **40,000+** 张高质量图片用于训练火灾预警 AI 模型。

## 🎯 目标数据集规模

| 类别 | 类型 | 目标数量 |
|------|------|----------|
| 数据中心火灾 | 正样本 | 5000+ |
| 电线老化 | 正样本 | 5000+ |
| 锂电池故障 | 正样本 | 5000+ |
| 烟雾 | 正样本 | 5000+ |
| 设备过热 | 正样本 | 5000+ |
| 电弧/打火 | 正样本 | 5000+ |
| 正常设备 | 负样本 | 5000+ |
| 正常电灯 | 负样本 | 2000+ |
| 静电放电 | 负样本 | 2000+ |
| 阳光反射 | 负样本 | 2000+ |

## 🚀 部署到 GitHub

### 方法一：手动创建

1. 在 GitHub 创建新仓库 `fire-dataset-collector`
2. 将本项目所有文件推送到仓库
3. Actions 会自动运行

### 方法二：使用脚本一键部署

```bash
# 在本项目目录运行
./deploy.sh
```

## 📁 项目结构

```
├── .github/
│   └── workflows/
│       └── collect.yml      # GitHub Actions 工作流
├── src/
│   ├── collector.py         # 主采集器
│   ├── baidu_scraper.py     # 百度图片爬虫
│   ├── bing_scraper.py       # Bing 图片爬虫
│   └── utils.py             # 工具函数
├── dataset/                 # 采集的数据集（Git LFS 存储）
├── logs/                    # 运行日志
├── requirements.txt
├── config.py               # 配置文件
└── README.md
```

## ⏰ 自动运行策略

- **定时触发**: 每天 UTC 0:00 自动运行
- **手动触发**: 在 Actions 页面点击 "Run workflow"
- **分批采集**: 每次运行采集约 500-1000 张，避免超时

## 🔧 本地运行

```bash
pip install -r requirements.txt
python src/collector.py
```

## 📊 数据统计

运行后查看 `dataset/stats.json` 或 GitHub Actions 日志。

## ⚠️ 注意事项

1. 百度图片 API 有频率限制，代码已加入延时
2. 采集的图片可能包含无关内容，建议后续人工筛选
3. 部分图片可能有版权，请仅用于学术研究

## 📜 License

MIT License