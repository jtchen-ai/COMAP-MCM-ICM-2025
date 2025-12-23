import pandas as pd

# 读取 CSV 文件
data = pd.read_csv("summerOly_athletes_sorted.csv")

# 按照 Team, Year, Sport, Medal 分组统计
grouped_by_sport = data.groupby(['Team', 'Year', 'Event', 'Medal']).size().unstack(fill_value=0)

# 重命名列名
grouped_by_sport = grouped_by_sport.rename(columns={'Gold': 'Gold', 'Silver': 'Silver', 'Bronze': 'Bronze'})

# 重置索引，方便输出
grouped_by_sport = grouped_by_sport.reset_index()

# 保存为新的 CSV 文件
grouped_by_sport.to_csv("team_year_Event_medal_stats11111.csv", index=False)

# 打印输出示例
print(grouped_by_sport.head())