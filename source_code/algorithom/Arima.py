import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# 1. 导入数据
file_path = "transformed_summerOly_programs_country_filled.csv"
data = pd.read_csv(file_path)

# 2. 检查数据结构
print("数据结构：")
print(data.head())  # 查看前几行
print("数据行数：", len(data))  # 检查行数
print("列名：", data.columns)  # 打印列名

# 3. 确保 'Index' 列存在
if "Index" not in data.columns:
    raise KeyError("CSV 文件中未找到 'Index' 列，请检查文件内容。")

# 4. 确保数据有至少 33 行
if len(data) < 32:
    raise ValueError("数据不足 33 行，无法进行训练和测试划分。")

# 5. 对 `China1` 列及其后的每一列进行预测
# 找到从 `China1` 开始的所有列
columns_to_predict = data.columns[data.columns.get_loc("China1"):]

# 初始化保存真实值和预测值的列表
y_true_list = []
y_pred_list = []

# 遍历所有需要预测的列
for column in columns_to_predict:
    print(f"\n正在处理列：{column}")

    # 使用 `Index` 列值为 1 到 30 的数据作为训练集
    train_data = data[data["Index"].between(1, 30)]
    true_data = data[data["Index"] == 30]  # `Index == 30` 的行为真实值
    test_data = data[data["Index"] == 33]  # `Index == 33` 的行为测试集

    # 确保列数据存在
    if column not in data.columns:
        print(f"列 {column} 不存在，跳过。")
        continue

    y_train = train_data[column]
    y_true = true_data[column].values[0]  # 获取真实值（Index == 30 的值）

    # 检查 y_train 是否为空
    if y_train.empty:
        print(f"列 {column} 的训练数据为空或缺失，跳过。")
        continue

    # 处理缺失值
    if y_train.isnull().sum() > 0:
        print(f"列 {column} 的训练数据存在缺失值，使用前向填充处理。")
        y_train = y_train.fillna(method="ffill")

    # ADF 检验 - 检查数据是否平稳
    adf_result = adfuller(y_train)
    p_value = adf_result[1]
    print(f"列 {column} 的 ADF 检验 p 值: {p_value:.4f}")

    # 如果数据非平稳（p值 > 0.05），进行差分处理
    if p_value > 0.05:
        print(f"列 {column} 的数据非平稳，进行一阶差分处理。")
        y_train_diff = y_train.diff().dropna()  # 一阶差分
    else:
        print(f"列 {column} 的数据平稳，无需差分。")
        y_train_diff = y_train

    # 构建 ARIMA 模型
    try:
        model = ARIMA(y_train_diff, order=(1, 1, 1))  # ARIMA(1, 1, 1) 模型
        model_fit = model.fit()
        forecast_steps = 1  # 预测未来 1 步
        forecast = model_fit.forecast(steps=forecast_steps)
        predicted_value = forecast.iloc[0]  # 获取预测值

        # 如果进行了差分，需要还原预测值
        if p_value > 0.05:
            predicted_value += y_train.iloc[-1]  # 还原差分值为实际值
    except Exception as e:
        print(f"列 {column} 的 ARIMA 模型训练或预测失败，错误信息：{e}")
        continue

    # 将预测值填入 `Index == 33` 的行对应列
    data.loc[data["Index"] == 33, column] = predicted_value
    print(f"列 {column} 的预测值已填充：{predicted_value:.2f}")

    # 保存真实值和预测值
    y_true_list.append(y_true)
    y_pred_list.append(predicted_value)

# 6. 计算 MSE Loss
mse_loss = mean_squared_error(y_true_list, y_pred_list)
print(f"\n所有列的 MSE Loss: {mse_loss:.4f}")

# 7. 保存结果到新的 CSV 文件
output_file = "transformed_summerOly_programs_country _forestloss111.csv"
data.to_csv(output_file, index=False)
print(f"预测结果已保存到文件：{output_file}")