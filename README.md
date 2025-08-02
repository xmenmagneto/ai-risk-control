# 🛡️ AI 风控系统 | AI Risk Control for E-Commerce Seckill

本项目是一个独立的 AI 风控子系统，集成于电商秒杀系统中。通过实时提取用户请求特征，利用机器学习模型判断用户行为是否正常（例如判断是否为机器人），在请求到达核心服务前完成风险拦截。

> ✅ 目标：提高系统稳定性，防止恶意流量冲击，保障秒杀公平性。

## 📦 技术栈

- 语言：Python 3
- 框架：Flask
- ML模型：scikit-learn
- 数据处理：pandas
- 部署环境：本地 / Docker（可选）

## 📁 项目结构

```
ai-risk-control/
├── app.py                # Flask 主程序，定义 API 接口
├── model.py              # 模型训练与加载逻辑
├── request_features.py   # 请求特征提取模块
├── test_request.json     # 模拟请求样本
├── requirements.txt      # Python 依赖
├── .gitignore            # Git 忽略配置
└── README.md             # 项目说明文档
```

## ⚙️ 安装与运行
```
1. 创建虚拟环境（建议）

python -m venv venv
.\venv\Scripts\activate       # Windows PowerShell 启动虚拟环境

2. 安装依赖

pip install -r requirements.txt

3. 启动服务

python app.py

默认服务运行在：http://localhost:5000
```

## 🧪 测试接口

确保服务已运行后，使用命令行测试（Windows PowerShell）：

```
Invoke-RestMethod -Uri http://localhost:5000/score `
  -Method POST `
  -ContentType "application/json" `
  -InFile "test_request.json"
```

## 📄 示例请求数据（test_request.json）

```
{
  "ip": "192.168.1.100",
  "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  "ts": 1720000000,
  "user_id": 12345,
  "product_id": 987
}
```

## 📈 模块说明

模块名               | 说明
--------------------|------------------------------------------------
request_features.py | 将请求数据转为模型可用的特征向量
model.py            | 加载/训练一个简单分类器（后续可扩展）
app.py              | 定义 /score 接口，返回请求风险评分

## 🚀 后续可拓展方向

- 更复杂的模型（如 XGBoost、深度学习）
- 模型线上热更新机制
- Kafka 实时特征收集与风控决策流
- 与 Java 秒杀系统集成，实现全链路风控
