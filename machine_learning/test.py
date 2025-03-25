# -*-codeing = utf-8 -*-
# Time : 2025/3/3 14:09
# @Author: 沐
# @Description:
# @FileName：
from sklearn.linear_model import LinearRegression
import joblib

# 生成虚拟数据（确保无中文干扰）
X = [[0, 1, 2], [3, 4, 5]]
y = [10, 20]

# 训练并保存模型
model = LinearRegression()
model.fit(X, y)
joblib.dump(model, "test_model.joblib", protocol=4)

# 加载模型
loaded_model = joblib.load("test_model.joblib")
print("模型加载成功")