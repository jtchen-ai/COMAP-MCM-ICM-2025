from scipy.stats import spearmanr
import numpy as np
import torch
import seaborn as sns
import matplotlib.pyplot as plt

# 假设项目安排数量（Query）和国家积分数（Key）
projects = np.array([2, 8, 2, 35, 2, 5, 48, 0, 0, 0, 2, 0, 0, 13, 2, 0, 6, 0, 0, 2, 2, 2, 4, 12, 2,
                     2, 2, 0, 0, 12, 2, 0, 2, 2, 14, 2, 2, 2, 0, 0, 15, 0, 0, 0, 2, 0, 0, 0, 0, 14,
                     2, 0, 10, 15, 4, 4, 0, 2, 5, 0, 0, 3, 0, 2, 0, 0, 10, 12, 6])

countries = np.array([217, 401, 174, 123, 238, 161, 274, 136, 106, 382])

# 项目和国家标签
feature_columns = [
    "Artistic Swimming", "Diving", "Marathon Swimming", "Swimming", "Water Polo",
    "Archery", "Athletics", "Badminton", "Baseball", "Softball", "3x3", "Basketball",
    "Basque Pelota", "Boxing", "Breaking", "Sprint", "Slalom", "Cricket", "Croquet",
    "BMX Freestyle", "BMX Racing", "Mountain Bike", "Road", "Track", "Dressage",
    "Eventing", "Jumping", "Vaulting", "Driving", "Fencing", "Field hockey",
    "Flag football", "Football", "Golf", "Artistic", "Rhythmic", "Trampoline",
    "Indoor", "Field", "Jeu de Paume", "Judo", "Karate", "Sixes", "Field",
    "Modern Pentathlon", "Polo", "Rackets", "Roque", "Coastal", "Rowing", "Sevens",
    "Union", "Sailing", "Shooting", "Skateboarding", "Sport Climbing", "Squash",
    "Surfing", "Table Tennis", "Taekwondo", "Tennis", "Triathlon", "Tug of War",
    "Beach", "Indoor", "Water Motorsports", "Weightlifting", "Freestyle", "Greco-Roman"
]
country_columns = ['Australia', 'China', 'France', 'Germany', 'Great Britain', 'Italy', 'Japan',
                   'Netherlands', 'South Korea', 'United States']

# 初始化存储斯皮尔曼相关系数的矩阵
spearman_matrix = np.zeros((len(projects), len(countries)))

# 计算每个项目和每个国家之间的斯皮尔曼相关系数
for i, project_value in enumerate(projects):
    for j, country_value in enumerate(countries):


        # 计算 Spearman 相关系数
        corr, _ = spearmanr(project_value, country_value)  # 单点之间的相关性

        print(corr)
        spearman_matrix[i, j] = corr

# 创建热力图
print(spearman_matrix)


plt.figure(figsize=(15, 10))
sns.heatmap(spearman_matrix, xticklabels=country_columns, yticklabels=feature_columns,
            cmap="coolwarm", cbar_kws={'label': 'Spearman Correlation'})
plt.title("Spearman Correlation Heatmap: Projects vs. Countries", fontsize=16)
plt.xlabel("Countries")
plt.ylabel("Sports Projects")
plt.tight_layout()
plt.show()