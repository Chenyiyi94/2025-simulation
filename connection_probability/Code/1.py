import numpy as np
import pandas as pd

def find_ids_by_acronym(csv_file_path, acronym_list):
    df = pd.read_csv(csv_file_path, usecols=['ID', 'Acronym'])       # 读取CSV文件的特定列
    matching_rows = df[df['Acronym'].isin(acronym_list)]       # 查找匹配的ID
    id_list = matching_rows['ID'].tolist()          # 提取ID并返回
    return id_list


# 示例调用
csv_file_path = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\MouseToPlot.csv'  # 替换为你的CSV文件路径
acronym_list = ['MO', 'MO1','MO2/3']  # 替换为你想要查找的acronym列表

ids = find_ids_by_acronym(csv_file_path, acronym_list)
print(ids)