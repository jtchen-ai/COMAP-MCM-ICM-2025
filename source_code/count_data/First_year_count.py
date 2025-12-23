import pandas as pd

# Step 1: 读取 first_medal_year_per_country.csv 文件
input_path = "first_medal_year_per_country.csv"  # 替换为你的文件路径
data = pd.read_csv(input_path)

# Step 2: 按年份分组，并统计每年有多少个国家首次获得奖牌
yearly_counts = data.groupby("First_Medal_Year").size().reset_index(name="Country_Count")

# Step 3: 保存结果到新的 CSV 文件
output_path = "medal_yearly_counts.csv"  # 输出文件路径
yearly_counts.to_csv(output_path, index=False)

print(f"统计结果已保存到 {output_path}")