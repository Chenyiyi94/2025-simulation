# the region and layer statistical information in the original neuron's morphometry table.
import csv



# 指定CSV文件路径
csv_file_path = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\TableS6_Full_morphometry_1222_layer.csv'

# 创建一个空集合来存储第二列的唯一值
unique_region_values = set()
unique_layer_values = set()

# 打开CSV文件进行读取
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    # 遍历CSV文件中的每一行（假设第一行是标题行，我们将其跳过）
    for row in csv_reader:
        region_value = row[1]
        layer_value = row[2]
        # 将第2,3列的值添加到集合中（集合会自动去除重复的值）
        unique_region_values.add(region_value)
        unique_layer_values.add(layer_value)

unique_region_values = sorted(list(unique_region_values))
print(f"region values: {unique_region_values}")
print(f"total region number: {len(unique_region_values)}")
print(f"layer values:{unique_layer_values}")


value_to_check = 'PFC'
# 检查值是否在集合中
if value_to_check in unique_region_values:
    print(f"{value_to_check} is in the set.")
else:
    print(f"{value_to_check} is not in the set.")
