# 计算数据集神经元投射到指定region/layer 的number of bouton 和 length of axon.

import os,csv,math,shutil
import numpy as np
import time
from multiprocessing import Pool

global need_regions
global region

region = "VISal"  #source region
layer = "L6"      #source layer

#ID_file = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\ID_data\VISpL23.csv'
'''
with open(ID_file) as f:
    temp=csv.reader(f)
    need_regions=[int(x[0]) for x in temp]
    f.close()
print(need_regions)
'''
need_regions=[601,649]

def FileCount(par):
    path, file, output_path = par[0],par[1],par[2]
    bouton_count = 0
    axon_length = 0
    with open(os.path.join(path,file)) as file_object:
        contents = file_object.readlines()
        #print(f"contents的长度是{len(contents)}")
        file_object.close()
    for LineID in range(0,len(contents)):
        x=contents[LineID]
        x=x.strip("\n")
        t1=x.split( )
        t1=list(map(float,t1))
        #print(f"t1{t1}")
        if t1[1] in need_regions:
        # if t1[1] !=0:
            if t1[0]==5:
                bouton_count = bouton_count+1
            elif t1[0]==2:
                axon_length = axon_length+t1[2]
    temp=str(bouton_count)+' '+str(axon_length)
    print(f"temp:{temp}")
    new_file=file.split('.')[0]+'.txt'           # 结果文件的命名！需要修改更合理
    f=open(os.path.join(output_path, new_file),'w+')
    f.writelines(temp)
    f.close()

def run__pool():  # main process
    cpu_worker_num = 2
    time_start = time.time()  # 记录开始时间
    neuron_info_table = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\TableS6_Full_morphometry_1222_layer.csv'
    path='./File_Info'
    output_path ='./Temp'

    # 清空输出文件夹
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    else:
        shutil.rmtree(output_path)
        os.mkdir(output_path)

    par_list=[]

    with open(neuron_info_table, 'r', newline='',encoding='utf-8-sig') as csvfile:
        t = csv.reader(csvfile)
        t = list(t)
        for i in range(0,len(t)):
            if 'pre_' in t[i][0]:
                t[i][0]=t[i][0].replace('pre_','')+'_pre'
            if 'a' in t[i][2]:
                t[i][2]=t[i][2].replace('a','')
            if 'b' in t[i][2]:
                t[i][2]=t[i][2].replace('b','')    
    new_soma_info={x[0]:(x[1],x[2]) for x in t}
    print(f"new soma info {new_soma_info}")
    
    for root, dirs, files in os.walk(path):
        for file in files:
            # if soma_info[file.split('.')[0]][0]==region or region=="All":
            if new_soma_info[file.split('.')[0]][0]==region and new_soma_info[file.split('.')[0]][1]==layer:
                par_list.append([path,file,output_path])
    print(len(par_list))
    with Pool(cpu_worker_num) as p:
        p.map(FileCount, par_list)
       
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print('File Count time: '+str(time_sum))  

if __name__ =='__main__':
    run__pool()
    
    for root, dirs, files in os.walk('./Temp'):
        data=[]
        for file in files:
            with open(os.path.join('./Temp',file)) as file_object:
                temp = file_object.readlines()
                file_object.close()
            t=temp[0].split( )
            t=list(map(float,t))
            if t[0]==0:
                continue
            data.append(t)
        data=np.array(data)
        print(np.sum(data,0))
        t=np.sum(data,0)
        print(t[0], t[1])
        #print(t[0],t[1],t[0]/t[1])