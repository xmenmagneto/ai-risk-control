import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import joblib

# 1. 读取训练数据
data = pd.read_csv('training_data.csv')

# 2. 标签转换：BLOCK->1，ALLOW->0
data['label_binary'] = data['label'].map({'ALLOW': 0, 'BLOCK': 1})

# 3. 选择训练特征和目标
X = data['userAgent']  # 这里我们只用 userAgent 作为示例特征
y = data['label_binary']

# 4. 创建处理流程：文本向量化 + 逻辑回归模型
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),  # 把 userAgent 里的文字转成数字向量
    ('classifier', LogisticRegression())  # 逻辑回归分类器
])

# 5. 训练模型
pipeline.fit(X, y)

# 6. 保存训练好的模型到文件
joblib.dump(pipeline, 'model.pkl')

print("模型训练完成，文件保存为 model.pkl")