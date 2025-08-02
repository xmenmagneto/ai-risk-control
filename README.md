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
├── app.py # 主服务入口，融合模型与规则判断
├── llm_infer.py # 模型加载与推理（支持融合规则）
├── rule_engine.py # 规则引擎：可配置静态规则
├── model_train.py # 模型训练脚本
├── model.pkl # 已训练好的模型
├── pressure_test.py # 并发压力测试脚本
├── test_request.json # 单个测试请求数据
├── test_request_block.json # 单个测试请求数据
├── requirements.txt # Python 项目依赖
└── README.md # 当前说明文档
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

## 📊 接口响应说明

```
{
  "decision": "BLOCK",                  # 最终融合后的决策结果
  "rule_hits": ["RULE_UA_BOT"],         # 命中的规则名（如有）
  "model_prob_block": 0.87              # 模型判断为 BLOCK 的概率
}
```

## 🧠 判定逻辑融合策略

当前系统支持三种风控模式，可在 app.py 中配置切换：

模式                | 说明
-----------------  |------------------------------------------------
rule               | 仅使用规则引擎进行判断
model              | 仅使用机器学习模型进行判断
fuse               | 融合规则和模型（推荐）
示例配置：
```
final_decision = fuse_decision(rule_decision, model_decision, mode="fuse")
```

## 🚨 异常处理与降级
- 模型推理失败时自动降级使用规则引擎
- 设置超时时间防止模型卡死拖慢请求（默认 1.5 秒）
- 日志记录异常信息，方便监控系统健康

## 📈 并发压力测试
使用 `pressure_test.py` 模拟多线程高并发请求：
`python pressure_test.py`
输出包括：
- 成功 / 失败请求数
- 平均响应时间
- 最小 / 最大响应时间
- 吞吐量（QPS）

## 📊 模型训练与更新
`python model_train.py`
说明：
- 使用已标注的样本进行训练（可扩展采集方式）
- 训练完成后自动生成 model.pkl
- 可定期更新模型以提升准确率


## 📈 模块说明

模块名               | 说明
--------------------|------------------------------------------------
llm_infer.py            | 模型推理模块 + 决策融合逻辑
rule_engine.py           | 简单可配置规则引擎（IP、UA、频率等）
model_train.py          | 使用历史数据训练模型
pressure_test.py        | 并发测试性能瓶颈与响应延迟

## 🚀 后续可拓展方向
- 集成 Kafka + 异步流处理
- 热更新模型或规则配置
- 模型改进（XGBoost、深度学习）
- 与 Java 秒杀系统联调接入
- 引入缓存与 IP 信誉分机制
