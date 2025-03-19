import os,json,csv
import numpy as np

## 构建CCFv3结构
with open(r'..\Data\Other_Infomation\tree.json','r',encoding='utf_8_sig')as fp:
    json_data = json.load(fp)
    fp.close()
Celltype2Id={x['acronym']:x['id'] for x in json_data}
Id2Celltype={Celltype2Id[key]:key for key in Celltype2Id.keys()}
Id2Celltype[0]="no region"
Id2Celltype[-1]="outside"

# 提取bouton位置
path='.\File_Temp'

for root, dirs, files in os.walk(path):
    new_content=[]
    count=0
    for file in files:
        count+=1
        if count%100==0:
            print(count)
        name=file.split(".")[0]
        with open(os.path.join(path, file)) as file_object:
            contents = file_object.readlines()
            file_object.close()
        
        for lineid in range(0,len(contents)):
            if contents[lineid][0]=='#':# 跳过注释
                continue  
            x=contents[lineid]
            x=x.strip("\n")
            t1=x.split( )
            t2=list(map(float,t1))
            if t2[1]==5:
                temp=[name]+t2[2:8]+[int(t2[10])]+[Id2Celltype[t2[10]]]
                new_content.append(temp)
    with open('BoutonInfo.csv', 'w+',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["neuron id","x in row brain","y in row brain","z in row brain","x after registration","y after registration","z after registration","region id","region"])
        for x in new_content:
            writer.writerow(x)
        f.close()
        