import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# 1. 导入数据
file_path = "transformed_summerOly_programs_country_filled.csv"  # 输入文件路径
data = pd.read_csv(file_path)

# 2. 检查数据结构
print("数据结构：")
print(data.head())  # 查看前几行
print("数据行数：", len(data))  # 检查行数
print("列名：", data.columns)  # 打印列名

# 3. 确保 'Index' 列存在
if "Index" not in data.columns:
    raise KeyError("文件中未找到 'Index' 列，请检查文件内容。")

# 初始化保存真实值和预测值的列表
y_true_list = []
y_pred_list = []

# 找到从 `China1` 开始的所有列
columns_to_predict = data.columns[data.columns.get_loc("China1"):]

# 遍历每一行，从 Index=13 到最后一行
for idx in range(13, len(data) ):  # 从 Index=13 开始
    print(f"正在预测 Index={idx} 的目标列...")

    # 检查当前行是否存在
    test_data = data[data["Index"] == idx]
    if test_data.empty:
        print(f"Index={idx} 的数据为空，跳过...")
        continue

    # 准备训练集：使用当前行之前的所有数据作为训练集
    train_data = data[data["Index"] < idx]
    if train_data.empty:
        print(f"没有足够的训练数据用于 Index={idx} 的预测，跳过...")
        continue

    # 遍历目标列，逐个预测
    for column in columns_to_predict:
        print(f"正在处理目标列：{column}")

        # 检查目标列是否存在
        if column not in data.columns:
            print(f"目标列 {column} 不存在，跳过...")
            continue

        # 准备训练数据和真实值
        y_train = train_data[column]
        y_true = test_data[column].values[0]  # 获取真实值（当前 Index 的值）

        # 检查 y_train 是否为空
        if y_train.empty:
            print(f"列 {column} 的训练数据为空或缺失，跳过。")
            continue

        # 处理缺失值
        if y_train.isnull().sum() > 0:
            print(f"列 {column} 的训练数据存在缺失值，使用前向填充处理。")
            y_train = y_train.fillna(method="ffill")

        # 构建 ARIMA 模型
        try:
            model = ARIMA(y_train, order=(1, 1, 1))  # 使用 ARIMA(1, 1, 1) 模型
            model_fit = model.fit()
            forecast_steps = 1  # 预测未来 1 步
            forecast = model_fit.forecast(steps=forecast_steps)
            predicted_value = forecast.iloc[0]  # 获取预测值
        except Exception as e:
            print(f"列 {column} 的 ARIMA 模型训练或预测失败，错误信息：{e}")
            continue

        # 将预测值填入当前行的对应列
        data.loc[data["Index"] == idx, column] = predicted_value
        print(f"列 {column} 的预测值已填充：{predicted_value:.2f}")

        # 保存真实值和预测值
        y_true_list.append(y_true)
        y_pred_list.append(predicted_value)

# 计算 MSE Loss
if len(y_true_list) > 0 and len(y_pred_list) > 0:
    mse_loss = mean_squared_error(y_true_list, y_pred_list)
    print(f"所有列的 MSE Loss: {mse_loss:.4f}")
else:
    print("没有足够的真实值和预测值来计算 MSE Loss。")

# 保存结果到新的 Excel 文件
output_file = "111111transformed_summerOly_programs_country_predictions.xlsx"
data.to_excel(output_file, index=False)
print(f"预测结果已保存到文件：{output_file}")