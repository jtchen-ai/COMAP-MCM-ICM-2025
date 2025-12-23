import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. 读取 Excel 文件
file_path1 = "X1.xlsx"  # X1 文件
file_path2 = "X2.xlsx"  # X2 文件
file_path_Y = "Y.xlsx"  # Y 文件
file_path_isHost = "isHost.xlsx"  # isHost 文件

# 读取 X1 和 X2 的数据
data1 = pd.read_excel(file_path1, sheet_name="Sheet1")
data2 = pd.read_excel(file_path2, sheet_name="Sheet1")

# 将数据转换为二维数组形式
X1 = data1.iloc[:19, 1:].values.reshape(19, 10, 4)  # 转换为 19x10x4 的张量
X2 = data2.iloc[:19, 1:].values.reshape(19, 10, 4)  # 转换为 19x10x4 的张量

# 读取 Y 数据
Y_data = pd.read_excel(file_path_Y, sheet_name="Sheet1")
Y = Y_data.iloc[:19, 1:].values.reshape(19, 10, 4)  # 转换为 19x10x4 的张量

# 读取 isHost 数据
isHost_data = pd.read_excel(file_path_isHost, sheet_name="Sheet1")
isHost = isHost_data.iloc[:19, 1:].fillna(0).values.reshape(19, 10, 4)  # 转换为 19x10x4 的张量

# 2. 计算 X3
# 定义主办方效应参数
lamda = 0.3
beita1 = 0.3
beita2 = 0.3
gama = 0.5

# 定义 P 和 N
P = np.array([0, 0.78, 0.89, 0.93, 0, 8, 0, 0, 0.98, 0.92, 0, 0.96, 0.72, 0, 0.83, 0.81, 0, 1.53, 0.68])
N = np.array([4, 2, 1, 13, 9, 21, 5, 5, 18, 16, 20, 14, 29, 1, 1, 0, 4, 0, 17])

# 计算 Y_matrix
Y_temp = beita1 * P + beita2 * N + gama
Y_matrix = np.tile(Y_temp.reshape(-1, 1), 40).reshape(19, 10, 4)  # 转换为 19x10x4 的张量

# 计算 X3
X3 = Y_matrix * isHost  # 按元素相乘，形成 19x10x4 的张量

# 3. 多元线性回归
# 初始化回归模型
model = LinearRegression()

# 存储最终的回归系数及性能指标
# 存储最终的回归系数、偏置项及性能指标
final_coefficients = []  # 回归系数
final_intercepts = []  # 偏置项
mse_list = []  # 每个国家的均方误差
r2_list = []  # 每个国家的 R^2

# 对每个国家（10 个国家）进行回归
for country_idx in range(10):
    # 提取当前国家的数据
    X1_country = X1[:, country_idx, :]  # 取出维度为 (19, 4)
    X2_country = X2[:, country_idx, :]  # 取出维度为 (19, 4)
    X3_country = X3[:, country_idx, :]  # 取出维度为 (19, 4)
    Y_country = Y[:, country_idx, :]  # 取出维度为 (19, 4)

    # 将 X1, X2, X3 合并为特征矩阵 (19*4, 3)
    X = np.hstack([X1_country.flatten().reshape(-1, 1),
                   X2_country.flatten().reshape(-1, 1),
                   X3_country.flatten().reshape(-1, 1)])

    # 将 Y_country 展平为目标向量 (19*4,)
    y = Y_country.flatten()

    # 拟合线性回归模型
    model.fit(X, y)

    # 提取当前国家的回归系数和偏置项
    coefficients = model.coef_  # 回归系数
    intercept = model.intercept_  # 偏置项
    final_coefficients.append(coefficients)
    final_intercepts.append(intercept)

    # 预测值
    y_pred = model.predict(X)

    # 计算精度指标
    mse = mean_squared_error(y, y_pred)  # 均方误差
    r2 = r2_score(y, y_pred)  # 决定系数 R^2
    mse_list.append(mse)
    r2_list.append(r2)

    # 打印当前国家的回归系数、偏置项和精度
    print(f"国家 {country_idx + 1} 的回归系数: {coefficients}")
    print(f"国家 {country_idx + 1} 的偏置项 (Intercept): {intercept:.4f}")
    print(f"国家 {country_idx + 1} 的均方误差 (MSE): {mse:.4f}")
    print(f"国家 {country_idx + 1} 的决定系数 (R^2): {r2:.4f}")

# 将最终回归系数和偏置项转为 numpy 数组 (10,)
final_coefficients = np.array(final_coefficients)
final_intercepts = np.array(final_intercepts)

# 打印最终的回归系数和偏置项
print("\n最终的回归系数 (每个国家一个):")
print(final_coefficients)
print("\n最终的偏置项 (每个国家一个):")
print(final_intercepts)

# 打印总体精度
avg_mse = np.mean(mse_list)
avg_r2 = np.mean(r2_list)
print(f"\n平均均方误差 (MSE): {avg_mse:.4f}")
print(f"平均决定系数 (R^2): {avg_r2:.4f}")