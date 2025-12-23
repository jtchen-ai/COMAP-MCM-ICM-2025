import pandas as pd

# 导入数据
file_path = "team_year_Event_medal_stats11111.csv"  # 替换为文件的实际路径
data = pd.read_csv(file_path)

# 计算 Gold、Silver 和 Bronze 的总和，作为 total 列
data['total'] = data['Gold'] + data['Silver'] + data['Bronze']

# 按 Team 分组，再按 Event 分组，最后按 Year 排序
data = data.sort_values(by=['Team', 'Event', 'Year'])

# 添加辅助列：前1到前6年的 total 值以及对应的 Year
data['Prev_total_1'] = data.groupby(['Team', 'Event'])['total'].shift(1)  # 前一年 total
data['Prev_Year_1'] = data.groupby(['Team', 'Event'])['Year'].shift(1)  # 前一年的 Year

data['Prev_total_2'] = data.groupby(['Team', 'Event'])['total'].shift(2)  # 前两年 total
data['Prev_Year_2'] = data.groupby(['Team', 'Event'])['Year'].shift(2)  # 前两年的 Year

data['Prev_total_3'] = data.groupby(['Team', 'Event'])['total'].shift(3)  # 前三年 total
data['Prev_Year_3'] = data.groupby(['Team', 'Event'])['Year'].shift(3)  # 前三年的 Year

data['Prev_total_4'] = data.groupby(['Team', 'Event'])['total'].shift(4)  # 前四年 total
data['Prev_Year_4'] = data.groupby(['Team', 'Event'])['Year'].shift(4)  # 前四年的 Year

data['Prev_total_5'] = data.groupby(['Team', 'Event'])['total'].shift(5)  # 前五年 total
data['Prev_Year_5'] = data.groupby(['Team', 'Event'])['Year'].shift(5)  # 前五年的 Year

data['Prev_total_6'] = data.groupby(['Team', 'Event'])['total'].shift(6)  # 前六年 total
data['Prev_Year_6'] = data.groupby(['Team', 'Event'])['Year'].shift(6)  # 前六年的 Year

# 筛选条件：
# 1. Prev_total_1 ~ Prev_total_6 均为 0；
# 2. 当前年的 total 不为 0；
# 3. Prev_Year_1 ~ Prev_Year_6 的顺序严格递减（只在相同 Team 和 Event 内比较）。
filtered_data = data[
    (data['Prev_total_1'] == 0) &
    (data['Prev_total_2'] == 0) &
    (data['Prev_total_3'] == 0) &
    (data['Prev_total_4'] == 0) &
    (data['Prev_total_5'] == 0) &
    (data['Prev_total_6'] == 0) &
    (data['total'] != 0) &
    (data['Prev_Year_1'] < data['Year']) &
    (data['Prev_Year_2'] < data['Prev_Year_1']) &
    (data['Prev_Year_3'] < data['Prev_Year_2']) &
    (data['Prev_Year_4'] < data['Prev_Year_3']) &
    (data['Prev_Year_5'] < data['Prev_Year_4']) &
    (data['Prev_Year_6'] < data['Prev_Year_5'])
]

# 删除不需要的列，只保留原始列和辅助列
filtered_data = filtered_data[['Team', 'Year', 'Event', 'Gold', 'Silver', 'Bronze', 'total',
                               'Prev_total_1', 'Prev_total_2', 'Prev_total_3',
                               'Prev_total_4', 'Prev_total_5', 'Prev_total_6']]

# 将结果保存为 Excel 文件
output_file = "bottleneck_with_total111.xlsx"
filtered_data.to_excel(output_file, index=False)

print(f"结果已成功保存到 {output_file}")