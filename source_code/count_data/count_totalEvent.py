import pandas as pd

# 读取CSV文件
df = pd.read_csv('summerOly_athletes_sorted.csv')

# 筛选Year >= 1948的数据
filtered_df = df[df['Year'] >= 1948]

# 按Year分组并计算每组的不同Event数量
event_counts = filtered_df.groupby('Year')['Event'].nunique().reset_index()

# 重命名列
event_counts.columns = ['Year', 'Event_num']

# 添加addEvent列，计算当前行的Event_num减去上一行的Event_num
event_counts['addEvent'] = event_counts['Event_num'].diff().fillna(0).astype(int)

# 导出为Excel文件
event_counts.to_excel('Year_Event_num_with_addEvent.xlsx', index=False)

print("文件已导出为 Year_Event_num_with_addEvent.xlsx")