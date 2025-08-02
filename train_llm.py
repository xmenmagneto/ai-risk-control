import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

def detect_bot_useragent(ua):
    if ua is None:
        return 0
    ua = ua.lower()
    for bot in ['curl', 'python', 'bot', 'scrapy']:
        if bot in ua:
            return 1
    return 0

# 1. 读取数据
data = pd.read_csv('training_data.csv')

# 加入新特征
data['is_bot_ua'] = data['userAgent'].apply(detect_bot_useragent)

# 2. 标签转数字
data['label_binary'] = data['label'].map({'ALLOW': 0, 'BLOCK': 1})

# 3. 特征和标签
X = data[['ip', 'userAgent', 'requestCountLastMinute', 'userId', 'productId', 'timestamp', 'is_bot_ua']]
y = data['label_binary']

# 4. 特征预处理流水线
preprocessor = ColumnTransformer(
    transformers=[
        ('ip_vect', CountVectorizer(), 'ip'),  # 把ip当文本向量化
        ('ua_vect', CountVectorizer(), 'userAgent'),
        ('num', StandardScaler(), ['requestCountLastMinute']),
        ('userId_ohe', OneHotEncoder(handle_unknown='ignore'), ['userId']),
        ('productId_ohe', OneHotEncoder(handle_unknown='ignore'), ['productId']),
        ('bot_flag', 'passthrough', ['is_bot_ua'])
        # timestamp这里先不处理，或者自己转换成时间特征
    ])

# 5. 建立完整pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000))
])

# 6. 训练
pipeline.fit(X, y)

# 7. 保存模型
joblib.dump(pipeline, 'model.pkl')

print("多特征模型训练完成，保存为model.pkl")