import pandas as pd

# 1. 导入 CSV 数据
file_path = "transformed_summerOly_programs_country.csv"
data = pd.read_csv(file_path)

# 2. 检查数据结构
print("数据结构：")
print(data.head())  # 查看前几行
print("列名：", data.columns)  # 打印列名

# 3. 获取从 Australia1 开始的所有列
columns_to_interpolate = data.columns[data.columns.get_loc("Australia1"):]

# 4. 对每列进行时间序列插值
for column in columns_to_interpolate:
    print(f"正在对列 {column} 进行时间序列插值...")
    # 使用线性插值方法填充缺失值
    data[column] = data[column].interpolate(method='linear')

# 5. 检查是否还有缺失值
missing_values = data[columns_to_interpolate].isnull().sum()
print("各列缺失值统计：")
print(missing_values)

# 6. 保存处理后的数据到新的 CSV 文件
output_file = "transformed_summerOly_programs_country_interpolated.csv"
data.to_csv(output_file, index=False)
print(f"插值后的数据已保存到文件：{output_file}")