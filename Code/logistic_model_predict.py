import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.metrics import log_loss


# Logistic 回归函数
def logistic_model(E, T_participation, eta):
    """
    Logistic 回归模型
    P_medal = 1 / (1 + exp(-(eta_0 + eta_1 * E + eta_2 * T_participation)))
    :param E: 项目参与数（数组）
    :param T_participation: 累计参与届数（数组）
    :param eta: 模型参数 [eta_0, eta_1, eta_2]
    :return: P_medal, 获奖概率（数组）
    """
    eta_0, eta_1, eta_2 = eta
    linear_part = -(eta_0 + eta_1 * E + eta_2 * T_participation)
    return 1 / (1 + np.exp(linear_part))


# 损失函数（对数损失，用于优化参数）
def loss_function(eta, E, T_participation, y_true):
    """
    损失函数，计算真实值与预测值之间的对数损失
    :param eta: 模型参数 [eta_0, eta_1, eta_2]
    :param E: 项目参与数（数组）
    :param T_participation: 累计参与届数（数组）
    :param y_true: 真实值（数组）
    :return: 对数损失
    """
    y_pred = logistic_model(E, T_participation, eta)
    return log_loss(y_true, y_pred)


# 优化参数
def optimize_parameters(E, T_participation, y_true):
    """
    使用 scipy.optimize.minimize 优化 eta 参数
    :param E: 项目参与数（数组）
    :param T_participation: 累计参与届数（数组）
    :param y_true: 真实值（数组）
    :return: 优化后的参数 eta
    """
    # 初始参数猜测
    initial_eta = [0.1, 0.1, 0.1]

    # 优化
    result = minimize(
        loss_function,
        initial_eta,
        args=(E, T_participation, y_true),
        method='BFGS'
    )

    return result.x  # 返回优化后的参数


# 示例数据（假设有10个国家的数据）
data = {
    'E': [10, 15, 8, 20, 12, 5, 25, 30, 18, 22],  # 项目参与数
    'T_participation': [5, 10, 3, 15, 8, 2, 20, 25, 12, 18],  # 累计参与届数
    'P_medal_actual': [0, 1, 0, 1, 0, 0, 1, 1, 1, 1]  # 实际是否获奖（0 或 1）
}

# 转换为 DataFrame
df = pd.DataFrame(data)

# 提取特征和目标值
E = df['E'].values
T_participation = df['T_participation'].values
y_true = df['P_medal_actual'].values

# 优化 eta 参数
optimized_eta = optimize_parameters(E, T_participation, y_true)

# 打印优化结果
print("优化后的参数：", optimized_eta)

# 使用优化后的参数计算预测值
P_medal_pred = logistic_model(E, T_participation, optimized_eta)
print("预测的获奖概率：", P_medal_pred)