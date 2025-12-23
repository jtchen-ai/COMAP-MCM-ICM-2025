import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# 读取之前生成的 CSV 文件
processed_file = "processed_olympic_data.csv"  # 替换为生成的文件路径
df = pd.read_csv(processed_file)

# 提取从 Australia 开始的列
australia_start_cols = df.loc[:, "Australia":]

# 提取 SWA 列到 WRG 列
swa_to_wrg_cols = df.loc[:, "SWA":"WRG"]

# 初始化存储 Spearman 相关系数的结果
heatmap_data = pd.DataFrame(index=australia_start_cols.columns, columns=swa_to_wrg_cols.columns)

# 嵌套循环：从 Australia 开始的每一列与 SWA 到 WRG 的每一列计算 Spearman 相关系数
for australia_col in australia_start_cols.columns:
    for swa_col in swa_to_wrg_cols.columns:
        # 计算 Spearman 相关系数
        corr, _ = spearmanr(df[australia_col], df[swa_col])
        # 填充热力图数据
        heatmap_data.loc[australia_col, swa_col] = corr

# 将相关系数转换为浮点数（确保热力图正确显示）
heatmap_data = heatmap_data.astype(float)

# 替换 SWA 到 WRG 的列名为 feature_columns
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

# 确保替换列名的数量一致
heatmap_data.columns = feature_columns[:len(heatmap_data.columns)]

# 绘制热力图
plt.figure(figsize=(20, 12))  # 调整图形大小以显示更多标签
sns.heatmap(
    heatmap_data,
    annot=False,              # 设置为 False，不显示数字值，避免遮挡标签
    fmt=".2f",
    cmap="coolwarm",
    cbar_kws={'label': 'Spearman Correlation'}
)

# 添加标题和标签

plt.xlabel("Olympic Events", fontsize=12)
plt.ylabel("Countries", fontsize=12)

# 调整 x 轴标签的旋转角度以避免重叠
plt.xticks( fontsize=8)  # x轴标签字体调整为10
plt.yticks(fontsize=8)  # 缩小 y 轴标签字体

# 自动调整布局以避免标签被裁剪
plt.tight_layout()

# 显示图形
plt.show()