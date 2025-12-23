import pandas as pd

# 导入CSV文件
file_path = "team_year_Event_medal_stats11111.csv"  # 替换为文件的实际路径
data = pd.read_csv(file_path)


data = data.sort_values(by=['Team', 'Event', 'Year'])

# 定义函数：筛选出当前年份的 No medal 为 0，且前两年不为 0 的记录，并返回前两年的数据
def find_bottleneck_breakthrough_with_history(group):
    """
    在每个 Team 和 Sport 分组内，筛选出满足以下条件的年份：
    1. 当前年份的 No medal 为 0；
    2. 前至少两个更早的年份（且 Sport 相同）的 No medal 不为 0；
    同时返回前两年的数据。
    """
    # 添加辅助列：shift 获取前两年的 No medal 值和年份
    group['Prev_No_medal_1'] = group['No medal'].shift(1)  # 前一年的 No medal
    group['Prev_No_medal_2'] = group['No medal'].shift(2)  # 前两年的 No medal
    group['Prev_Year_1'] = group['Year'].shift(1)  # 前一年的年份
    group['Prev_Year_2'] = group['Year'].shift(2)  # 前两年的年份

    # 筛选条件：
    # 1. 当前年的 `No medal` 为 0；
    # 2. 前两年的 `No medal` 均不为 0；
    # 3. 前两年必须存在。
    filtered = group[
        (group['No medal'] == 0) &
        (group['Prev_No_medal_1'] != 0) & (group['Prev_No_medal_2'] != 0) &
        (~group['Prev_Year_1'].isna()) & (~group['Prev_Year_2'].isna())
    ]

    # 如果找到符合条件的行，提取前两年的对应行
    result = []
    for _, row in filtered.iterrows():
        # 当前行
        current_row = row.to_dict()

        # 前一年数据
        prev_row_1 = group[(group['Year'] == row['Prev_Year_1'])].iloc[0].to_dict()

        # 前两年数据
        prev_row_2 = group[(group['Year'] == row['Prev_Year_2'])].iloc[0].to_dict()

        # 合并当前行和前两年的数据
        result.append({
            "Current_Year": current_row['Year'],
            "Current_No_medal": current_row['No medal'],
            "Prev_Year_1": prev_row_1['Year'],
            "Prev_No_medal_1": prev_row_1['No medal'],
            "Prev_Year_2": prev_row_2['Year'],
            "Prev_No_medal_2": prev_row_2['No medal'],
            "Team": current_row['Team'],
            "Sport": current_row['Event'],
        })

    return pd.DataFrame(result)

# 按 Team 和 Sport 分组，应用筛选函数
result = data.groupby(['Event', 'Event']).apply(find_bottleneck_breakthrough_with_history)

# 重置索引
result = result.reset_index(drop=True)

# 输出结果
print(result)

# 如果需要保存结果到文件
result.to_csv("bottleneck_with_history111.xlsx", index=False, encoding='utf-8-sig')