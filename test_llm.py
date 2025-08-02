import joblib
import pandas as pd

# 1. 加载训练好的模型
model = joblib.load('model.pkl')

# 2. 构造测试数据（示例）
test_data = pd.DataFrame([
    {
        'ip': '192.168.1.1',
        'userAgent': 'curl/7.68.0',
        'requestCountLastMinute': 20,
        'userId': 'user01',
        'productId': 1001,
        'timestamp': 1690000000000
    },
    {
        'ip': '10.0.0.5',
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'requestCountLastMinute': 2,
        'userId': 'user02',
        'productId': 1002,
        'timestamp': 1690000001000
    }
])

# 3. 使用模型进行预测（输出0或1）
predictions = model.predict(test_data)

# 4. 输出结果（0代表ALLOW，1代表BLOCK）
for i, pred in enumerate(predictions):
    decision = "BLOCK" if pred == 1 else "ALLOW"
    print(f"Test sample {i+1}: {decision}")
