# 计算数据集神经元投射到指定region/layer 的number of bouton 和 length of axon.
# 按大区域计算，如VIS，SS等
import os
import csv
import shutil
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool
from datetime import datetime




# 数据集neuron参数
# VIS_region = ['VISa', 'VISal', 'VISam', 'VISl', 'VISli', 'VISp', 'VISpm', 'VISpor', 'VISrl']  # From source neuron dataset, all regions which include "VI". And I removed "VISC".
# SS_region = ['SSp', 'SSp-bfd', 'SSp-ll', 'SSp-m', 'SSp-n', 'SSp-tr', 'SSp-ul', 'SSp-un', 'SSs']  # From source neuron dataset
#EFC_region = ['AId', 'AIp', 'AIv', 'MOp', 'MOs', 'ORB','ORBl', 'ORBm', 'ORBvl', 'PL']  # Executive Function cortical areas: AId AIp AIv MOp MOs ORB(ORBl, ORBm, ORBvl),PL. And PL is not in the source neuron datatset.
MC_region = ['PERI', 'RSP', 'RSPagl', 'RSPd', 'RSPv','TEa'] # Memory cortical areas: PERI,RSP(RSPagl,RSPd,RSPv),TEa
region = MC_region  # source region
Layers = ['L1','L2/3', 'L4', 'L5', 'L6']  # source数据集里没有L1的数据,但是映射时需要考虑layer1.
# Layers = ['L6']  # source layer

#acronym_list = ['VISl6a','VISl6b']  # goal region and layer
# projection_region_VIS = ['VIS','VIS1','VIS2/3','VIS4','VIS5','VIS6a','VIS6b','VISalVISal1','VISal2/3','VISal4','VISal5','VISal6a','VISal6b',
#                          'VISam','VISam1','VISam2/3','VISam4','VISam5','VISam6a','VISam6b',
#                          'VISl','VISl1','VISl2/3','VISl4','VISl5','VISl6a','VISl6b',
#                          'VISp','VISp1','VISp2/3','VISp4','VISp5','VISp6a','VISp6b',
#                          'VISpl','VISpl1','VISpl2/3','VISpl4','VISpl5','VISpl6a','VISpl6b',
#                          'VISpm','VISpm1','VISpm2/3','VISpm4','VISpm5','VISpm6a','VISpm6b']
#VIS_layer1 = ['VIS','VIS1','VISalVISal1','VISam','VISam1','VISl','VISl1','VISp','VISp1','VISpl','VISpl1','VISpm','VISpm1']
# VIS_layer2_3 = ['VIS','VIS2/3','VISal2/3','VISam','VISam2/3','VISl2/3','VISp','VISp2/3','VISpl','VISpl2/3','VISpm', 'VISpm2/3']
# VIS_layer5 = ['VIS','VIS5','VISal5','VISam5','VISl5','VISp5','VISpl5','VISpm5']
#projection_region_SS = ['SS1','SS4','SS6a','SS6b','SSp1','SSp4','SSp6a','SSp6b','SSp-n1','SSp-n4','SSp-n6a','SSp-n6b','SSp-bfd1','SSp-bfd4','SSp-bfd6a','SSp-bfd6b']
# SS_layer2_3 = ['SS2/3','SSp2/3','SSp-n2/3','SSp-bfd2/3','SSp-bfd','SSp-n','SSp','SS']
# SS_layer5 = ['SS5','SSp5','SSp-n5','SSp-bfd5','SSp-bfd','SSp-n','SSp','SS']
# projection_region_EFC = ['AId1','AId6a','AId6b','AIp1','AIp6a','AIp6b',
#                          'AIv1','AIv6a','AIv6b',
#                          'MOp1','MOp6a','MOp6b','MOs','MOs1','MOs6a','MOs6b',
#                          'ORB','ORB1','ORB6a','ORB6b','ORBl','ORBl1','ORBl6a','ORBl6b',
#                          'ORBm','ORBm1','ORBm2','ORBm6a','ORBm6b','ORBv','ORBvl','ORBvl1','ORBvl6a','ORBvl6b',
#                          'PL','PL1','PL2','PL6a','PL6b']
# EFC_layer2_3 = ['AId2/3','AIp2/3','AIv2/3','MOp2/3','MOs2/3','ORB2/3','ORBl2/3','ORBm2/3','ORBvl2/3','PL2/3']
# EFC_layer5 = ['AId5','AIp5','AIv5','MOp5','MOs5','ORB5','ORBl5','ORBm5','ORBvl5','PL5']
projection_region_MC = ['PERI','PERI6a','PERI6b','PERI1',
                        'RSPd','RSPd1','RSPd4','RSPd6a','RSPd6b','RSPv','RSPv1','RSPv2','RSPv6a','RSPv6b',
                        'RSP','RSPagl','RSPagl1','RSPagl6a','RSPagl6b',
                        'TEa','TEa1','TEa4','TEa6a','TEa6b']
MC_layer2_3 = ['PERI2/3','RSPd2/3','RSPv2/3','RSPagl2/3','TEa2/3']
MC_layer5 = ['PERI5','RSPd5','RSPv5','RSPagl5','TEa5']
acronym_list = MC_layer5
# csv文件路径
csv_file_path = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\MouseToPlot.csv'  # 替换为你的CSV文件路径
neuron_info_table = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\TableS6_Full_morphometry_1222_layer.csv'

input_path = './File_Info'
output_path = './Temp/result'

def find_ids_by_acronym(csv_file_path, acronym_list):
    df = pd.read_csv(csv_file_path, usecols=['ID', 'Acronym'])       # 读取CSV文件的特定列
    matching_rows = df[df['Acronym'].isin(acronym_list)]       # 查找匹配的ID
    id_list = matching_rows['ID'].tolist()          # 提取ID并返回
    #print(id_list)
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

    with open('output.csv', 'a', newline='') as csvfile:
        # 获取当前时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result_with_timestamp = result + [timestamp]
        writer = csv.writer(csvfile)
        #writer.writerow(result)
        writer.writerow(result_with_timestamp)

global goal_regions_ids
goal_regions_ids = find_ids_by_acronym(csv_file_path, acronym_list)


def main_process(layer=None):
    with open('output.csv', 'w', newline='') as csvfile:
        pass  # 清空输出文件
    # 检查输出文件夹是否存在
    if os.path.exists(output_path):
        print("输出文件夹存在")
    else:
        os.mkdir(output_path)
        print("输出文件夹不存在，已创建。")

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
            if neuron_info[file.split('.')[0]][0] in region:
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
    # 创建或追加写入 CSV 文件
    csv_file_path = 'MC_MC.csv'
    fieldnames = ['source_Layer', 'Neuron_Num', 'Total_Bouton_Num', 'Total_Axon_Length','Projection_region']

    # 以追加模式打开文件，如果文件不存在则创建它
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csvfile: # 清空是w，添加是a
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 如果文件是空的（即第一次写入），写入表头
        if csvfile.tell() == 0:
            writer.writeheader()

        for layer in Layers:
            print(layer)
            time_start = time.time()  # 开始时间
            result = main_process(layer=layer)  # 捕获返回值
            print(f"For {layer},the result is neuron_num,total_bouton_num, total_axon_length: {result}")
            print("--------------------------------")
            time_end = time.time()
            time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s

            # 将结果转换为字典格式，以便写入 CSV 文件
            row_data = {
                'source_Layer': layer,
                'Neuron_Num': result[0],
                'Total_Bouton_Num': result[1],
                'Total_Axon_Length': result[2],
                'Projection_region': str("MC_layer5")
            }
            # 写入数据行
            writer.writerow(row_data)




