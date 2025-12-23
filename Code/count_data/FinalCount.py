import pandas as pd
import matplotlib.pyplot as plt

# 读取之前的 Excel 文件
data = pd.read_excel("us_team_weighted_scores.xlsx", index_col=0)

# 确保 2024 年存在
if 2024 not in data.index:
    # 添加一行全为 0 的 2024 年数据
    data.loc[2024] = 0

# 定义年份递增权重
# 权重从 0 开始，每年递增 0.1
years = data.index  # 获取年份索引
weights = [0 + 0.1 * i for i in range(len(years))]  # 包括所有年份的权重

# 打印权重（可选）
print(f"Year weights: {dict(zip(years, weights))}")

# 将权重转换为 DataFrame，与数据形状对齐
weights_df = pd.DataFrame(weights, index=years, columns=['Weight'])

# 按行应用权重，将权重乘以每年的数据
weighted_data = data.loc[:, 'Archery':].mul(weights_df['Weight'], axis=0)

# 对所有年份（包括 2024 年）的加权求和
weighted_sum_vector = weighted_data.sum(axis=0)

# 更新 2020 年的数据
if 2020 in data.index:
    data.loc[2020, 'Archery':] = weighted_sum_vector
else:
    # 如果不存在 2020 年的行，则新增一行
    new_row = pd.Series(weighted_sum_vector, index=data.columns, name=2020)
    data = data.append(new_row)

# 打印 2020 年结果
print("2020 年加权求和结果（未排序）：")
print(data.loc[2020])

# 对 2020 年数据排序（降序，最大值在顶部）
sorted_2020_data = data.loc[2020, 'Archery':].sort_values(ascending=True)  # ascending=True 最大值在上
print("2020 年加权求和结果（排序后）：")
print(sorted_2020_data)

# 绘制 2020 年的水平柱状图（排序后，最大值在上）
plt.figure(figsize=(10, 6))
sorted_2020_data.plot(kind='barh', title="", color='skyblue')
plt.xlabel('Importance')
plt.ylabel('Sports')
plt.tight_layout()
plt.savefig("2020_weighted_sum_with_2024_sorted_horizontal.png")  # 保存柱状图为图片
plt.show()

# 单独检查 2024 年的数据
if 2024 in data.index:
    print("2024 年数据（未排序）：")
    print(data.loc[2024])

    # 对 2024 年数据排序（降序）
    sorted_2024_data = data.loc[2024, 'Archery':].sort_values(ascending=True)  # ascending=True 最大值在上面
    print("2024 年数据（排序后）：")
    print(sorted_2024_data)

    # 绘制 2024 年的水平柱状图（排序后，最大值在上）
    plt.figure(figsize=(10, 6))
    sorted_2024_data.plot(kind='barh', title="", color='orange')
    plt.xlabel('Importance')
    plt.ylabel('Sports')
    plt.tight_layout()
    plt.savefig("2024_data_sorted_horizontal.png")  # 保存柱状图为图片
    plt.show()
else:
    print("数据中没有 2024 年的信息！")

# 保存包含 2024 数据的加权结果到新的 Excel 文件
data.to_excel("us_team_weighted_sums_with_2024.xlsx")