import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

# 1. 加载数据
data = pd.read_csv("First_medal_yearly_counts.csv")

# 设置时间索引为 Index 列
data.set_index('Index', inplace=True)

# 提取需要处理的列
time_series = data['Country_Count']

# 绘制原始时间序列
plt.figure(figsize=(10, 6))
plt.plot(time_series, label='Original Data')
plt.title('Original Time Series')
plt.xlabel('Index')
plt.ylabel('Country_Count')
plt.legend()
plt.show()

# 2. ADF 检验 (Augmented Dickey-Fuller Test)
def adf_test(series):
    print("Performing ADF Test...")
    result = adfuller(series)
    print('ADF Test Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:', result[4])
    if result[1] <= 0.05:
        print("数据是平稳的（拒绝原假设）。\n")
    else:
        print("数据是非平稳的（无法拒绝原假设）。\n")

adf_test(time_series)

# 3. KPSS 检验 (Kwiatkowski-Phillips-Schmidt-Shin Test)
def kpss_test(series):
    print("Performing KPSS Test...")
    result = kpss(series, regression='c', nlags='auto')
    print('KPSS Test Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:', result[3])
    if result[1] <= 0.05:
        print("数据是非平稳的（拒绝原假设）。\n")
    else:
        print("数据是平稳的（无法拒绝原假设）。\n")

kpss_test(time_series)

# 4. 差分处理
# 一阶差分
diff_series = time_series.diff().dropna()

# 绘制差分后的时间序列
plt.figure(figsize=(10, 6))
plt.plot(diff_series, label='Differenced Data')
plt.title('Differenced Time Series')
plt.xlabel('Index')
plt.ylabel('Differenced Country_Count')
plt.legend()
plt.show()

# 再次进行 ADF 和 KPSS 检验
print("差分后数据的平稳性测试：")
adf_test(diff_series)
kpss_test(diff_series)

# 5. 使用 ARIMA 模型进行预测
# 检查差分后的序列是否平稳，如果平稳，使用 ARIMA 进行建模
print("正在拟合 ARIMA 模型...")

# 使用 ARIMA(1, 1, 1) 模型（根据差分后数据的平稳性结果选择）
model = ARIMA(time_series, order=(1, 1, 1))  # (p, d, q)
model_fit = model.fit()

# 打印模型摘要
print(model_fit.summary())

# 预测下一个时间步
forecast = model_fit.forecast(steps=1)  # 预测未来 1 步
print("\n预测的下一个时间步值:", forecast.iloc[0])

# 绘制预测结果
plt.figure(figsize=(10, 6))
plt.plot(time_series, label='Original Data')
plt.axhline(forecast.iloc[0], color='red', linestyle='--', label='Next Step Forecast')
plt.title('ARIMA Forecast')
plt.xlabel('Index')
plt.ylabel('Country_Count')
plt.legend()
plt.show()