import pandas as pd

# 读取 CSV 文件
data = pd.read_csv("filtered_summerOly_athletes_sorted.csv")

# 按 Team 分组，统计每组 Year 和 Event 列中不同值的数量
result = (
    data.groupby("Team")
    .agg(
        Year=("Year", "nunique"),  # 统计 Year 列的不同值数量
        Event=("Event", "nunique")  # 统计 Event 列的不同值数量
    )
    .reset_index()  # 重置索引
)

# 将结果保存到新的 Excel 文件中
result.to_excel("team_year_event_summary.xlsx", index=False)

print("处理完成，结果已保存到 team_year_event_summary.xlsx 文件中。")