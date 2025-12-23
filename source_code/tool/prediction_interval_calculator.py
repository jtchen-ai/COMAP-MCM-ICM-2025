import numpy as np
from scipy.stats import t

# 1. 回归系数 (从训练中获得的结果)
final_coefficients = np.array([
    [1.00000000e+00, 1.75423740e-16, 9.45640566e-17],
    [4.98652805e-01, 4.98652805e-01, 1.71856795e+01],
    [-5.49108427e-01, 1.55422671e+00, 2.55172450e+00],
    [-4.06170069e-02, 1.23392553e+00, -2.56083703e-01],
    [-6.06883921e-02, 9.47750226e-01, 2.22918959e+01],
    [1.89170210e+00, -1.04108096e+00, 5.22446478e+00],
    [2.55491818e+00, -1.41087167e+00, 1.20094612e+00],
    [1.42321297e+00, -6.27650726e-01, 0.00000000e+00],
    [-4.83377257e-01, 3.14466697e+00, 1.62231784e+00],
    [-5.06074937e-01, 1.55902985e+00, 4.04173901e+00]
])

# 偏置项 (Bias)
bias = np.array([
    -8.88178420e-15, -6.89536496e-01, -1.90165534e+00, 1.27687897e+00,
    -3.88192306e-01, 1.58496323e+00, -6.33311635e-01, 1.79133064e+00,
    -4.83777087e-01, -3.40140482e+00
])

# 2. 预测数据 (X1^pre, X2^pre, isHost^pre)
X1_pre = np.array([
    16, 15, 16, 53, 37, 22, 20, 84, 11, 15,
    12, 36, 14, 14, 12, 40, 21, 17, 21, 60,
    10, 12, 14, 35, 17, 13, 13, 51, 11, 8,
    10, 34, 12, 8, 10, 30, 40, 33, 31, 104
]).reshape(1, 10, 4)

X2_pre = np.array([
    16, 15, 14, 46, 38, 27, 23, 87, 14, 19,
    18, 50, 12, 12, 12, 36, 18, 20, 24, 61,
    11, 11, 15, 36, 20, 12, 15, 46, 13, 8,
    11, 33, 10, 7, 10, 27, 42, 42, 39, 121
]).reshape(1, 10, 4)

isHost_pre = np.array([
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1
]).reshape(1, 10, 4)

# 3. 初始化 Y^pre
Y_pre = np.zeros((1, 10, 4))

# 初始化置信区间
lower_bound = np.zeros((1, 10, 4))
upper_bound = np.zeros((1, 10, 4))

# 假设的均方误差 (MSE) (通常从训练中获得，这里假设一个值)
MSE = 0.5  # 这里是一个假设值，实际应从模型训练中获取
t_value = t.ppf(0.975, df=0.3)  # 95% 置信水平，自由度 30（根据训练样本调整）

# 遍历每个国家 (10 个国家)
for country_idx in range(10):
    # 提取当前国家的回归系数
    coefficients = final_coefficients[country_idx]  # [coef_X1, coef_X2, coef_X3]
    bias_term = bias[country_idx]  # 当前国家的偏置项

    # 提取当前国家的特征矩阵
    X1_pre_country = X1_pre[:, country_idx, :]  # (1, 4)
    X2_pre_country = X2_pre[:, country_idx, :]  # (1, 4)
    isHost_pre_country = isHost_pre[:, country_idx, :]  # (1, 4)

    # 按照线性回归公式计算 Y^pre
    Y_pre[:, country_idx, :] = (
        coefficients[0] * X1_pre_country +
        coefficients[1] * X2_pre_country +
        coefficients[2] * isHost_pre_country +
        bias_term
    )

    # 计算预测区间
    for time_idx in range(4):  # 遍历每个时间点
        X0 = np.array([
            X1_pre_country[0, time_idx],
            X2_pre_country[0, time_idx],
            isHost_pre_country[0, time_idx]
        ])
        standard_error = np.sqrt(MSE * (1 + X0.T @ np.linalg.inv(np.eye(3)) @ X0))
        lower_bound[:, country_idx, time_idx] = Y_pre[:, country_idx, time_idx] - t_value * standard_error
        upper_bound[:, country_idx, time_idx] = Y_pre[:, country_idx, time_idx] + t_value * standard_error

# 打印预测结果及其置信区间
print("预测的 Y^pre 矩阵：")
print(Y_pre)
print("预测的置信区间下界：")
print(lower_bound)
print("预测的置信区间上界：")
print(upper_bound)