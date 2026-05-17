# Food5 YOLOv5 食物识别系统

基于 YOLOv5 的食物识别项目，支持 5 类常见食物检测，已完成从训练到 Hi3516CV610 板端部署的完整流程。

## 项目概述

**核心功能**: 输入一张食物图片，模型输出食物类别、检测框和置信度。

**支持类别** (5 类):

| 编号 | 英文名 | 中文 |
|---:|---|---|
| 0 | chicken_wings | 鸡翅 |
| 1 | dumplings | 饺子 |
| 2 | fried_rice | 炒饭 |
| 3 | hamburger | 汉堡 |
| 4 | ice_cream | 冰淇淋 |

---

## 项目结构

```
food_yolo_3516/
├── food5_dataset/           # 训练数据集
│   ├── images/train         # 训练图片 (3000 张)
│   ├── images/val           # 验证图片 (750 张)
│   ├── labels/train         # 训练标签
│   ├── labels/val           # 验证标签
│   └── food5.yaml           # 数据集配置
├── yolov5/                  # YOLOv5 源码
├── models/                  # 训练输出的模型
│   └── food5_yolov5s_640/
│       ├── best.pt          # PyTorch 最佳权重
│       ├── last.pt          # PyTorch 最后权重
│       └── best.onnx        # ONNX 模型
├── final_models/            # 最终部署模型
│   ├── food5_yolov5s_best.pt
│   ├── food5_yolov5s_best.onnx
│   └── food5_yolov5s_best.om    # Hi3516CV610 板端模型
├── deploy_package/          # 部署包
│   ├── model/
│   │   ├── food5_yolov5s_best.om
│   │   ├── food5_yolov5s_best.onnx
│   │   └── food5_yolov5s_best.pt
│   ├── demo/                # 推理 Demo
│   ├── docs/                # 部署文档
│   └── labels.txt           # 标签文件
├── onnx_food5_demo.py       # ONNX 推理脚本
└── prepare_food5_dataset.py # 数据集准备脚本
```

---

## 模型训练

### 训练配置
- **模型**: YOLOv5s
- **输入尺寸**: 640 × 640
- **训练轮数**: 50 epochs
- **Batch size**: 32
- **训练设备**: RTX 3090 GPU

### 训练结果

| 指标 | 数值 | 说明 |
|---|---:|---|
| Precision | 0.938 | 93.8% 准确率 |
| Recall | 0.924 | 92.4% 召回率 |
| mAP@0.5 | 0.977 | 97.7% 平均精度 |
| mAP@0.5:0.95 | 0.975 | 97.5% 高精度 |

### 各类别 mAP@0.5

| 类别 | mAP@0.5 |
|---|---:|
| chicken_wings | 0.981 |
| dumplings | 0.969 |
| fried_rice | 0.989 |
| hamburger | 0.977 |
| ice_cream | 0.968 |

> 注：当前采用整图标注方式，指标主要证明流程跑通，不完全等价于真实场景检测能力。

---

## 模型文件说明

### 训练阶段
| 文件 | 说明 |
|---|---|
| `best.pt` | PyTorch 训练最佳权重 |
| `last.pt` | PyTorch 最后一轮权重 |

### 部署阶段
| 文件 | 说明 |
|---|---|
| `best.onnx` | ONNX 中间格式，用于 PC 推理 |
| `food5_yolov5s_best.om` | Hi3516CV610 板端模型 (ATC 转换) |

### 模型输入输出

```
输入： [1, 3, 640, 640]  # 1 张 640x640 RGB 图片
输出：[1, 25200, 10]    # 25200 个候选框，每框 10 个值 (x,y,w,h,conf,5 类分数)
```

---

## 快速开始

### PC 端 ONNX 推理

```bash
cd D:\Projects\food_yolo_3516
conda activate qianrushi
python onnx_food5_demo.py
```

输出示例:
```
====== 检测结果 ======
ice_cream  conf=0.696  box=(0,0,507,511)
结果图片保存到：onnx_demo_result.jpg
```

---

## 板端部署流程

```
best.onnx
    ↓ (ATC 工具转换)
food5_yolov5s_best.om
    ↓
部署到 Hi3516CV610 文件系统
    ↓
调用 SVP_NPU / AIDETECT sample
    ↓
板端推理 + 后处理
    ↓
输出食物类别和置信度
```

---

## 当前状态

- [x] 数据集准备 (3000 训练 + 750 验证)
- [x] YOLOv5s 模型训练
- [x] 导出 ONNX 模型
- [x] PC 端 ONNX 推理验证
- [x] **转换 OM 板端模型**
- [ ] 板端部署验证 (下一步)

---

## 已知局限

1. 仅支持 5 类食物
2. 整图标注，检测框不够精细
3. 复杂场景效果待验证
4. 板端部署尚未完成

---

## 后续计划

1. 完成 Hi3516CV610 板端部署
2. 实现板端 C/C++ 后处理
3. 接入营养数据库查询
4. 开发 Web 展示界面

---

## 许可证

本项目用于学习和研究目的。
