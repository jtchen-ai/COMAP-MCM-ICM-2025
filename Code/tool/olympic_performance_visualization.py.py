import matplotlib.pyplot as plt
import numpy as np

# 国家名称
countries = ["USA", "Australia", "China", "South Korea", "UK", "Germany", "France", "Japan", "Italy", "Netherlands"]

# 调整后的奖牌数据
gold = [45, 39, 36, 31, 16, 15, 10, 20, 9, 10]
silver = [42, 36, 24, 21, 15, 15, 15, 15, 10, 6]
bronze = [39, 36, 21, 29, 19, 14, 13, 17, 13, 9]
total = [126, 121, 84, 83, 50, 44, 41, 52, 32, 29]

# 创建条形图
x = np.arange(len(countries))
width = 0.25

fig, ax = plt.subplots(figsize=(12, 6))
bars_gold = ax.bar(x - width, gold, width, label='Gold', color='gold')
bars_silver = ax.bar(x, silver, width, label='Silver', color='silver')
bars_bronze = ax.bar(x + width, bronze, width, label='Bronze', color='brown')

# 添加标题和标签
ax.set_xlabel("Country")
ax.set_ylabel("Number of Medals")
ax.set_xticks(x)
ax.set_xticklabels(countries)
ax.legend()

# 在条形图上显示数字
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{int(height)}',
                ha='center', va='bottom', fontsize=10)

add_labels(bars_gold)
add_labels(bars_silver)
add_labels(bars_bronze)

# 调整布局并显示
plt.tight_layout()
plt.show()