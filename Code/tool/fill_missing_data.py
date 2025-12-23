import pandas as pd

# 读取Excel文件
df = pd.read_excel('isHost.xlsx', sheet_name='Sheet1')

# 将缺失值（NaN）替换为0
df.fillna(0, inplace=True)

# 保存修改后的数据到新的Excel文件
df.to_excel('isHost.xlsx', index=False)

print("缺失值已补0，结果保存为 'isHost.xlsx'")