import pandas as pd
import numpy as np

# 文件路径
input_csv = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Code\v1_v1_edge_models.csv'
output_csv = "new_cy_v1_v1_edge_models.csv"


df = pd.read_csv(input_csv, on_bad_lines='skip',sep=r'\s+', engine='python')
print("列名：", df.columns)

# 检查“weight max”列是否存在
if "weight_max" not in df.columns:
    raise ValueError("CSV文件中没有找到'weight_max'列！")

# 统计最大值和最小值
max_value = df["weight_max"].max()
min_value = df["weight_max"].min()
length_weight_max = len(df["weight_max"])
print(f"当前'weight_max'列的最大值: {max_value}")
print(f"当前'weight_max'列的最小值: {min_value}")
print(f"当前'weight_max'列的长度是: {length_weight_max}")

'''
# 假设你的新数据是一个列表，长度与原数据行数一致
new_data = [0.025, 0.015, 0.010, 0.020, 0.005]  # 替换为你的实际数据
if len(new_data) != len(df):
    raise ValueError("新数据的长度与CSV文件的行数不一致！")


df["weight max"] = new_data

# 保存修改后的CSV文件
df.to_csv(output_csv, index=False)

'''

def data_normalization(data,target_min=0,target_max=2):
    """将data归一化到指定范围[target_min,target_max],返回归一化后的数据normalized_data。"""
    # 确保输入数据是 NumPy 数组或 Pandas Series
    if isinstance(data, list):
        data = np.array(data)

    # 计算原始数据的最小值和最大值
    data_min_value = np.min(data)
    data_max_value = np.max(data)

    # 检查是否所有值都相同（避免分母为零）
    if data_min_value == data_max_value:
        return np.full_like(data, (target_min + target_max) / 2)

    # 应用线性映射公式
    normalized_data = target_min + (data - data_min_value) / (data_max_value - data_min_value) * (target_max - target_min)

    return normalized_data

data_list = [292.697, 210.606, 38.0, 293.071, 61.75, 50.679, 1.878, 45.076, 773.316, 655.184, 124.543, 289.029, 311.333, 340.333, 155.3, 415.633]
print(len(data_list))
new_weight_value = data_normalization(data=data_list)
print(f"归一化后的数据是：{new_weight_value}")



def replace_column_with_new_weights(csv_file_path: str,
                                       output_file_path: str,
                                       column_name:str,
                                       fixed_numbers: list):
    """
    用一组固定的数字随机替换CSV文件中指定列的数据。

    参数:
        csv_file_path (str): 输入 CSV 文件的路径。
        output_file_path (str): 输出 CSV 文件的路径。
        column_name (str): 要替换的列名。
        fixed_numbers (list): 用于随机替换的固定数字列表。
    """
    # 1. 读取 CSV 文件
    try:
        df1 = pd.read_csv(csv_file_path, on_bad_lines='skip',sep=r'\s+', engine='python')
    except FileNotFoundError:
        raise FileNotFoundError(f"文件未找到，请检查路径：{csv_file_path}")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("CSV 文件为空或格式不正确。")

    # 2. 检查指定列是否存在
    if column_name not in df1.columns:
        raise ValueError(f"CSV 文件中没有找到列：{column_name}！")

    # 3. 随机替换指定列的数据
    df[column_name] = np.random.choice(fixed_numbers, size=len(df1))

    # 4. 保存修改后的 CSV 文件
    df.to_csv(output_file_path, index=False)

    print(f"已将 '{column_name}' 列的数据替换为新值，并保存到文件：{output_file_path}")



csv_file_path = input_csv
output_file_path = output_csv
column_name = "weight_max"
fixed_numbers = new_weight_value

replace_column_with_new_weights(csv_file_path, output_file_path, column_name, fixed_numbers)