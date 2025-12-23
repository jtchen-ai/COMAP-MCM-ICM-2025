import pandas as pd

# 读取之前生成的 CSV 文件
grouped_by_sport = pd.read_csv("11111team_year_sport_medal_stats11111.csv")

# 筛选 2000 年及以后的数据
filtered_data = grouped_by_sport[grouped_by_sport['Year'] >= 2000]

# 获取每个年份都存在的 Sport
sports_per_year = filtered_data.groupby(['Year', 'Sport']).size().reset_index(name='Count')
common_sports = sports_per_year.groupby('Sport')['Year'].nunique()
sports_in_all_years = common_sports[common_sports == len(filtered_data['Year'].unique())].index

# 筛选出这些 Sport 对应的数据
final_data = filtered_data[filtered_data['Sport'].isin(sports_in_all_years)]

# 保存到新的 Excel 文件
final_data.to_excel("sports_present_every_year.xlsx", index=False)

# 打印输出示例
print(final_data.head())