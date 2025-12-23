import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# 1. 导入数据
file_path = "transformed_summerOly_programs_country_filled.csv"
data = pd.read_csv(file_path)

# 2. 检查数据结构
print("数据结构：")
print(data.head())  # 查看前几行
print("数据行数：", len(data))  # 检查行数
print("列名：", data.columns)  # 打印列名

# 3. 确保特征列存在
feature_columns = [
    "SWA", "DIV", "OWS", "SWM", "WPO", "ARC", "ATH", "BDM", "BSB", "SBL", "BK3", "BKB", "PEL", "BOX", "BKG",
    "CSP", "CSL", "CKT", "CQT", "BMF", "BMX", "MTB", "CRD", "CTR", "EDR", "EVE", "EJP", "EVL", "EDV", "FEN",
    "HOC", "AFB", "FBL", "GLF", "GAR", "GRY", "GTR", "HBLI", "HBLF", "JDP", "JUD", "KTE", "LAX", "LAX.1",
    "MPN", "POL", "RQT", "RQQ", "ROC", "ROW", "RU7", "RUG", "SAL", "SHO", "SKB", "CLB", "SQU", "SRF", "TTE",
    "TKW", "TEN", "TRI", "TOW", "VBV", "VVO", "PBT", "WLF", "WRF", "WRG"
]

# 获取从 "Australia1" 开始的所有目标列
target_columns = data.columns[data.columns.get_loc("Australia1"):]

# 确保 `Index=31` 和 `Index=32` 存在
true_data = data[data["Index"] == 31]  # 真实值
test_data = data[data["Index"] == 32]  # 测试数据
if true_data.empty or test_data.empty:
    raise ValueError("测试或真实数据为空，请检查 'Index=31' 和 'Index=32' 是否存在。")

# 初始化字典存储预测值和真实值
predictions = {}
y_true_list = []
y_pred_list = []

# 遍历每一个目标列，从 "Australia1" 开始
for target_column in target_columns:
    print(f"正在处理目标列：{target_column}")

    # 检查目标列是否存在
    if target_column not in data.columns:
        print(f"目标列 {target_column} 不存在，跳过...")
        continue

    # 4. 准备训练集和测试集
    # 使用第 2 行到第 30 行作为训练数据
    train_data = data.iloc[1:30]  # 第 2 至第 30 行（索引从 0 开始，因此索引为 1:30）
    X_train = train_data[feature_columns]
    y_train = train_data[target_column]
    X_test = test_data[feature_columns]
    y_true = true_data[target_column].values[0]  # 真实值（Index=31）

    # 检查是否有缺失值
    if X_train.isnull().sum().sum() > 0:
        print("训练数据存在缺失值，使用前向填充处理。")
        X_train = X_train.fillna(method="ffill")
    if y_train.isnull().sum() > 0:
        print(f"目标值 '{target_column}' 存在缺失值，使用前向填充处理。")
        y_train = y_train.fillna(method="ffill")
    if X_test.isnull().sum().sum() > 0:
        print("测试数据存在缺失值，使用前向填充处理。")
        X_test = X_test.fillna(method="ffill")

    # 5. 构建随机森林模型并训练
    model = RandomForestRegressor(random_state=42, n_estimators=100)  # 使用 100 棵树
    model.fit(X_train, y_train)

    # 6. 预测目标列的值
    predicted_value = model.predict(X_test)

    # 输出预测结果
    print(f"预测 'Index=32' 的 {target_column} 值：{predicted_value[0]:.2f}")

    # 将预测值填充到 'Index=32' 的所在行的对应列
    data.loc[data["Index"] == 32, target_column] = predicted_value[0]

    # 存储真实值和预测值
    y_true_list.append(y_true)
    y_pred_list.append(predicted_value[0])

    # 存储预测结果
    predictions[target_column] = predicted_value[0]

# 7. 计算 MSE Loss
mse_loss = mean_squared_error(y_true_list, y_pred_list)
print(f"所有目标列的 MSE Loss: {mse_loss:.4f}")

# 8. 保存结果到新的 CSV 文件
output_file = "transformed_summerOly_programs_country_forest_loss.csv"
data.to_csv(output_file, index=False)
print(f"预测结果已保存到文件：{output_file}")