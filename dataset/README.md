# 机房火灾预警数据集

## 数据集目录结构

```
fire_detection_dataset/
├── positive/                    # 正样本（异常/火灾）
│   ├── data_center_fire/         # 数据中心火灾
│   ├── wire_aging/              # 电线老化
│   ├── battery_failure/         # 锂电池故障
│   ├── smoke/                   # 烟雾
│   ├── equipment_overheat/      # 设备过热
│   └── electric_arc/            # 电弧/打火
├── negative/                    # 负样本（正常/易误报）
│   ├── normal_light/            # 正常电灯
│   ├── normal_device/            # 正常设备
│   ├── static_discharge/        # 静电放电
│   └── sunlight_reflection/      # 阳光反射
└── external/                    # 外部数据集
    └── github_*/
```

## 数据统计

| 类型 | 类别 | 数量 |
|------|------|------|
| 正样本 | 数据中心火灾 | 30 |
| | 电线老化 | 30 |
| | 锂电池故障 | 30 |
| | 烟雾 | 30 |
| | 设备过热 | 30 |
| | 电弧/打火 | 30 |
| 负样本 | 正常设备 | 30 |
| | 正常电灯 | 30 |
| | 静电放电 | 30 |

## 用途

用于训练机房/数据中心火灾预警 AI 视觉识别模型

## 推荐补充数据集

1. Hugging Face: huggingface.co/datasets (搜索 fire detection)
2. Roboflow: app.roboflow.com (搜索 fire)
3. 百度飞桨: paddlepaddle.org.cn/datasets
4. GitHub: 搜索 "fire detection dataset"
