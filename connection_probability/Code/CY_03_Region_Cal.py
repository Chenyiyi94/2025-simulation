# 计算数据集神经元投射到指定region/layer 的number of bouton 和 length of axon.

import os
import csv
import shutil
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool




# 数据集neuron参数
region = "VISl"   # source region
Layers = ['L2/3', 'L4', 'L5', 'L6']  # 数据集里没有L1的数据
# Layers = ['L6']  # source layer

#acronym_list = ['VISl6a','VISl6b']  # goal region and layer
acronym_list = ['VISl1']
# csv文件路径
csv_file_path = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\MouseToPlot.csv'  # 替换为你的CSV文件路径
neuron_info_table = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\TableS6_Full_morphometry_1222_layer.csv'

input_path = './File_Info'
output_path = './Temp'

def find_ids_by_acronym(csv_file_path, acronym_list):
    df = pd.read_csv(csv_file_path, usecols=['ID', 'Acronym'])       # 读取CSV文件的特定列
    matching_rows = df[df['Acronym'].isin(acronym_list)]       # 查找匹配的ID
    id_list = matching_rows['ID'].tolist()          # 提取ID并返回
    print(id_list)
    return id_list


# 计算投射区域的bouton number and axon length
def process_file(file_info):
    path, file_name, output_dir = file_info  #将file_info变量中的值分别赋给path、file_name和output_dir
    file_path = os.path.join(path,file_name) #将path和file_name组合file_path
    bouton_num = 0
    axon_length = 0.0
    with open(file_path,'r') as file:
        for line in file:
            parts = line.strip().split()
            parts = list(map(float,parts))
            region_id = int(parts[1])
            if region_id in goal_regions_ids:
                if parts[0] == 5:
                    bouton_num = bouton_num + 1
                elif parts[0] == 2:
                    axon_length = axon_length + parts[2]
    result = [bouton_num,axon_length]

    #print(type(result))
    #print(result[0])
    #print(result[1])
    #print(f"计算结果是{result}")
    #print(f"bouton_num ={bouton_num},and axon_length ={axon_length}")


    #with open(output_file_path,'x',newline='') as csvfile:
    with open('output.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result)

global goal_regions_ids
goal_regions_ids = find_ids_by_acronym(csv_file_path, acronym_list)

def main_process(layer=None):
    # 清空输出文件output.csv的内容
    with open('output.csv', 'w', newline='') as csvfile:
        pass  # 不写入任何内容，只是打开并清空文件

    # 若输出文件夹存在，则清空，不存在，则创建
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    else:
        os.mkdir(output_path)

    # 读取neuron information table，获取neuron所属region和layer
    neuron_info = {}
    with open(neuron_info_table, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if 'pre_' in row[0]:
                row[0] = row[0].replace('pre_', '') + '_pre'
            if 'a' in row[2]:
                row[2] = row[2].replace('a', '')   #若第三列有a或者b，则用空字符串代替---兼容6a,6b的情况
            if 'b' in row[2]:
                row[2] = row[2].replace('b', '')
            neuron_info[row[0]] = (row[1],row[2])    # neuron是键，region和layer是值


    #准备并行处理的任务列表
    tasks = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            file_info =(root,file,output_path)
            if neuron_info[file.split('.')[0]][0] == region: #to be changed to get all neurons in set of regions
                if layer is None or neuron_info[file.split('.')[0]][1] == layer:
                    tasks.append(file_info)

    # 并行处理文件
    with Pool(2) as p:   #使用2个CPU
        p.map(process_file,tasks)


    #汇总结果
    total_bouton_num = 0
    total_axon_length = 0.0
    neuron_num = 0
    with open('output.csv',mode='r',newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            neuron_num = neuron_num + 1
            total_bouton_num = total_bouton_num + int(row[0])      # 不剔除bouton_num = 0时的neuron
            total_axon_length = total_axon_length + float(row[1])
    total_axon_length = round(total_axon_length, 3)    #四舍五入保留3位小数
    print(f"neuron_num={neuron_num},and total_bouton_num={total_bouton_num},and total_axon_length={total_axon_length}")
    return neuron_num,total_bouton_num,total_axon_length

if __name__ == '__main__':
    for layer in Layers:
        print(layer)
        time_start = time.time()  # 开始时间
        result = main_process(layer=layer)  # 捕获返回值
        print(f"For {layer},the result is neuron_num,bouton_num, total_axon_length: {result}")
        print("--------------------------------")
        time_end = time.time()
        time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
        #print('File Count time: ' + str(time_sum))


# 绘图部分


