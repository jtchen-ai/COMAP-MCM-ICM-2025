import pandas as pd

# 读取之前生成的 Excel 文件
data = pd.read_excel("sports_present_every_year.xlsx")

# 筛选 Team 列中为 "United States" 的数据
us_data = data[data['Team'] == "United States"]

# 定义奖牌权重
weights = {'Gold': 5, 'Silver': 3, 'Bronze': 1}

# 创建新的列，计算加权求和
us_data['Weighted_Score'] = (
    us_data['Gold'] * weights['Gold'] +
    us_data['Silver'] * weights['Silver'] +
    us_data['Bronze'] * weights['Bronze']
)

# 按 Year 和 Sport 分组，计算每组的加权总分
grouped_scores = us_data.groupby(['Year', 'Sport'])['Weighted_Score'].sum().reset_index()

# 将数据透视为 Year 为行，Sport 为列的格式
pivot_table = grouped_scores.pivot(index='Year', columns='Sport', values='Weighted_Score').fillna(0)

# 保存到新的 Excel 文件
pivot_table.to_excel("us_team_weighted_scores.xlsx")

# 打印输出示例
print(pivot_table.head())