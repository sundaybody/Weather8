# -*-codeing = utf-8 -*-
# Time : 2025/3/13 11:31
# @Author: 沐
# @Description:
# @FileName：
import pandas as pd

# 读取UTF-8编码的CSV文件
df = pd.read_csv('E:\Weather\Weather2\hisweather.csv', encoding='utf-8')

# 将DataFrame写入GBK编码的CSV文件
df.to_csv('output.csv', encoding='E:\Weather\Weather2\hisweather.csv', index=False)