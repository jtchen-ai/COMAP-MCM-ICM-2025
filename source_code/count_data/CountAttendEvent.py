import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# 读取 Excel 数据
data = pd.read_excel("sports_present_every_year.xlsx")

# 定义国家列表
countries = ['Australia', 'China', 'France', 'Great Britain', 'Japan',
             'Netherlands', 'South Korea', 'United States', 'Italy', 'Germany']

# 筛选 Team 列中包含在目标国家列表中的数据
filtered_data = data[data['Team'].isin(countries)].copy()  # 显式创建副本，避免视图问题

# 定义奖牌权重
weights = {'Gold': 5, 'Silver': 3, 'Bronze': 1}

# 计算加权积分
filtered_data['Weighted_Score'] = (
    filtered_data['Gold'] * weights['Gold'] +
    filtered_data['Silver'] * weights['Silver'] +
    filtered_data['Bronze'] * weights['Bronze']
)

# 计算每个运动的总积分
total_scores_by_sport = filtered_data.groupby('Sport')['Weighted_Score'].sum()

# 创建一个 DataFrame，用于存储每个国家在每个运动中的加权积分
team_sport_scores = filtered_data.groupby(['Team', 'Sport'])['Weighted_Score'].sum().unstack(fill_value=0)

# 初始化 Spearman 相关系数矩阵
spearman_corr = pd.DataFrame(index=team_sport_scores.columns, columns=countries)

# 计算 Spearman 相关系数
for sport in team_sport_scores.columns:
    for country in countries:
        # 获取运动的总分
        if sport not in total_scores_by_sport.index:
            print(f"Skipping {sport} due to no data in total_scores_by_sport.")
            continue
        sport_scores = pd.Series(total_scores_by_sport[sport], index=team_sport_scores.index)

        # 获取国家的分数
        if country not in team_sport_scores.index:
            print(f"Skipping {country} due to no data in team_sport_scores.")
            continue
        country_scores = team_sport_scores.loc[country]

        # 确保两个 Series 长度一致
        valid_indices = country_scores.index.intersection(sport_scores.index)
        country_scores = country_scores.loc[valid_indices].dropna()
        sport_scores = sport_scores.loc[valid_indices].dropna()

        if len(country_scores) == 0 or len(sport_scores) == 0:  # 如果没有有效数据
            print(f"Skipping {sport} or {country} due to insufficient data.")
            continue

        # 计算 Spearman 相关系数
        if len(country_scores) > 1 and len(sport_scores) > 1:  # 至少需要两个数据点
            spearman_corr.loc[sport, country] = spearmanr(country_scores, sport_scores).correlation
        else:
            spearman_corr.loc[sport, country] = None  # 数据不足，无法计算

# 转换为数值类型（避免空值问题）
spearman_corr = spearman_corr.astype(float)

# 可视化热力图
plt.figure(figsize=(12, 8))
sns.heatmap(spearman_corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Spearman Correlation Between Sports and Teams")
plt.xlabel("Teams")
plt.ylabel("Sports")
plt.tight_layout()

# 保存热力图为图片
plt.savefig("spearman_correlation_heatmap.png")
plt.show()