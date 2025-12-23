import pandas as pd

# 导入数据
file_path = "team_year_Event_medal_stats11111.csv"  # 替换为文件的实际路径
data = pd.read_csv(file_path)

# 按 Team 分组，再按 Event 分组，最后按 Year 排序
data = data.sort_values(by=['Team', 'Event', 'Year'])

# 添加辅助列：前1到前6年的 No medal 值以及对应的 Year
data['Prev_No_medal_1'] = data.groupby(['Team', 'Event'])['No medal'].shift(1)  # 前一年 No medal
data['Prev_Year_1'] = data.groupby(['Team', 'Event'])['Year'].shift(1)  # 前一年的 Year

data['Prev_No_medal_2'] = data.groupby(['Team', 'Event'])['No medal'].shift(2)  # 前两年 No medal
data['Prev_Year_2'] = data.groupby(['Team', 'Event'])['Year'].shift(2)  # 前两年的 Year

data['Prev_No_medal_3'] = data.groupby(['Team', 'Event'])['No medal'].shift(3)  # 前三年 No medal
data['Prev_Year_3'] = data.groupby(['Team', 'Event'])['Year'].shift(3)  # 前三年的 Year

data['Prev_No_medal_4'] = data.groupby(['Team', 'Event'])['No medal'].shift(4)  # 前四年 No medal
data['Prev_Year_4'] = data.groupby(['Team', 'Event'])['Year'].shift(4)  # 前四年的 Year

data['Prev_No_medal_5'] = data.groupby(['Team', 'Event'])['No medal'].shift(5)  # 前五年 No medal
data['Prev_Year_5'] = data.groupby(['Team', 'Event'])['Year'].shift(5)  # 前五年的 Year

data['Prev_No_medal_6'] = data.groupby(['Team', 'Event'])['No medal'].shift(6)  # 前六年 No medal
data['Prev_Year_6'] = data.groupby(['Team', 'Event'])['Year'].shift(6)  # 前六年的 Year

# 筛选条件：
# 1. Prev_No_medal_1 ~ Prev_No_medal_6 均不为 0；
# 2. Current_No_medal 为 0；
# 3. Prev_Year_1 ~ Prev_Year_6 的顺序严格递减（只在相同 Team 和 Event 内比较）。
filtered_data = data[
    (data['Prev_No_medal_1'] != 0) &
    (data['Prev_No_medal_2'] != 0) &
    (data['Prev_No_medal_3'] != 0) &
    (data['Prev_No_medal_4'] != 0) &
    (data['Prev_No_medal_5'] != 0) &
    (data['Prev_No_medal_6'] != 0) &
    (data['No medal'] == 0) &
    (data['Prev_Year_1'] < data['Year']) &
    (data['Prev_Year_2'] < data['Prev_Year_1']) &
    (data['Prev_Year_3'] < data['Prev_Year_2']) &
    (data['Prev_Year_4'] < data['Prev_Year_3']) &
    (data['Prev_Year_5'] < data['Prev_Year_4']) &
    (data['Prev_Year_6'] < data['Prev_Year_5'])
]

# 删除不需要的列，只保留原始列和辅助列
filtered_data = filtered_data[['Team', 'Year', 'Event', 'No medal',
                               'Prev_No_medal_1', 'Prev_No_medal_2', 'Prev_No_medal_3',
                               'Prev_No_medal_4', 'Prev_No_medal_5', 'Prev_No_medal_6']]

# 将结果保存为 Excel 文件
output_file = "bottleneck_with_history111.xlsx"
filtered_data.to_excel(output_file, index=False)

print(f"结果已成功保存到 {output_file}")