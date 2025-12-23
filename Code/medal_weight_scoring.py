import pandas as pd

# 读取 Excel 数据
file_path = "transformed_summerOly_programs_country_filled.csv"  # 替换为实际文件路径
df = pd.read_csv(file_path)

# 1. 过滤 Year 在 1984 到 2024 之间的数据
filtered_df = df[(df["Year"] >= 1984) & (df["Year"] <= 2024)]

# 2. 处理从 Australia1 开始的列
# 找到从 Australia1 开始的列的索引
start_col = filtered_df.columns.get_loc("Australia1")

# 创建一个新 DataFrame 用于存储处理后的结果
processed_df = filtered_df.iloc[:, :start_col]  # 保留前面的列（如 Year）

# 遍历国家列的每组（4列为一组）
columns = filtered_df.columns[start_col:]
for i in range(0, len(columns), 4):
    # 获取每组的 4 列
    group = columns[i:i+4]
    if len(group) < 3:  # 如果列数少于 3，跳过
        break

    # 处理每组列
    country = group[0][:-1]  # 提取国家名（去掉数字后缀）
    col1, col2, col3 = group[0], group[1], group[2]  # 第一列、第二列、第三列

    # 计算新的列值
    processed_col = (
        filtered_df[col1] * 5 +
        filtered_df[col2] * 3 +
        filtered_df[col3]  # 第三列直接加
    )

    # 将结果添加到新 DataFrame
    processed_df[country] = processed_col

# 3. 打印结果
print(processed_df)

# 如果需要将处理后的数据保存到新的 CSV 文件：
processed_df.to_csv("processed_olympic_data.csv", index=False)