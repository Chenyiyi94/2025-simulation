
# 假设文件路径
file_path = R"C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\visualization code\v1_v1_edge_types.csv"

import pandas as pd


# 初始化空列表存储数据
data = []

# 打开文件并读取
with open(file_path, 'r') as file:
    # 读取第一行作为列名
    columns = file.readline().strip().split(' ')[:8]

    # 读取剩余行作为数据
    for line in file:
        # 去除行首尾的空白字符，并按空格分割
        row = line.strip().split(' ')[:8]
        # 将每一行的数据添加到 data 列表中
        data.append(row)

# 将数据转换为 pandas DataFrame
df = pd.DataFrame(data, columns=columns)

# 打印 DataFrame
print(df)