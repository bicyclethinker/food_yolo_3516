# AI 食物热量与营养智能识别系统：板端部署包

本目录用于整理 Hi3516CV610 板端部署所需文件。

## 目录说明

- `bin/`：板端可执行程序和启动脚本
- `model/`：OM 模型和类别文件
- `config/`：项目配置文件
- `data/`：营养数据库和测试输入
- `web/`：网页展示文件
- `history/`：历史记录目录
- `output/`：调试输出、日志、截图
- `lib/`：额外动态库
- `scripts/`：部署脚本

## 模型说明

- `food5_yolov5s_best.pt`：PyTorch 训练权重
- `food5_yolov5s_best.onnx`：ONNX 中间模型
- `food5_yolov5s_best.om`：Hi3516CV610 板端 NPU 部署模型

板端实际运行只需要 `.om` 文件。

## 程序语言

- 板端核心推理：C / C++
- 训练和辅助脚本：Python
- 启动部署：Shell
- 网页展示：HTML + CSS + JavaScript

## 板端目标路径

部署到板子后，统一放在：

`/opt/food_ai/`

最终启动方式：

```sh
cd /opt/food_ai
./bin/start_food_ai.sh
```
