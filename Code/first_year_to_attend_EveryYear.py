import pandas as pd

# 读取 CSV 文件
data = pd.read_csv("cleaned_summerOly_medal_counts.csv")

# 按 NOC 分组，取每组 Year 最小值对应的数据行
result_by_noc = data.loc[data.groupby("NOC")["Year"].idxmin()]

# 按 Year 分组
result_by_year = result_by_noc.groupby("Year")

# 保存按 NOC 分组取 Year 最小值的结果到 CSV
result_by_noc.to_csv("grouped_by_noc_min_year.csv", index=False)

# 打印按 Year 分组的统计信息（每个 Year 对应的 NOC 数量）
for year, group in result_by_year:
    print(f"Year: {year}, Number of NOCs: {len(group)}")

# 如果需要保存按 Year 分组的结果到 Excel，每个 Year 一张表：
with pd.ExcelWriter("grouped_by_year.xlsx") as writer:
    for year, group in result_by_year:
        group.to_excel(writer, sheet_name=str(year), index=False)

print("处理完成，结果已保存为 grouped_by_noc_min_year.csv 和 grouped_by_year.xlsx 文件。")