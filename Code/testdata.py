import pandas as pd

# 1. 导入两个 Excel 文件
file_path1 = "X1.xlsx"  # 第一个文件
file_path2 = "X2.xlsx"  # 第二个文件

# 读取两个 Excel 文件的 Sheet1 表
data1 = pd.read_excel(file_path1, sheet_name="Sheet1")
data2 = pd.read_excel(file_path2, sheet_name="Sheet1")

# 2. 将数据转换为数组形式
# 去掉第一列（"Index"），只保留每行的 40 个数据值
data1_array = data1.iloc[:, 1:].values.tolist()  # 转换为二维数组
data2_array = data2.iloc[:, 1:].values.tolist()  # 转换为二维数组

# 打印数组内容
print("data1 的第一行数据：", data1_array[0])
print("data2 的第一行数据：", data2_array[0])




