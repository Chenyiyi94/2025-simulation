import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 读取CSV文件
csv_file = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\connection_probability\Bouton_Density_Data\MouseToPlot.csv'  # 替换为你的CSV文件路径
# 指定要读取的列名
columns_to_read = ['s0', 's1', 's2','s3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']
df = pd.read_csv(csv_file, header=0,nrows=2000,usecols=columns_to_read)
#print(df.columns)
#print(df)

# 初始化图
G = nx.DiGraph()

# 添加根节点（假设第二行的s0列是root）
root = df.loc[0, 's0']  # 使用.loc[]来访问DataFrame的特定行和列
print(root)
G.add_node(root)

node_s1 = node_s2 = node_s3 = node_s4 = node_s5 = node_s6 = node_s7 = node_s8 = node_s9 = node_s10 = None

# 从第三行开始迭代（因为前两行是列名和根节点信息）
for index, row in df.iloc[1:].iterrows():
    # current_node = None  # 初始化当前节点为None
    print(f"运行到第{index+1}行了,数据是：{row.to_dict()}")

    for col in ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']:
        if col == 's1' and pd.notnull(row[col]):
            print(f"col值是{col}")
            G.add_edge(root, row[col])  # 如果是s1列，则连接到root
            node_s1 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s1}")

        if col == 's2' and pd.notnull(row[col]):
            G.add_edge(node_s1, row[col])  # 如果是s1列，则连接到root
            node_s2 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s2}")

        if col == 's3' and pd.notnull(row[col]):
            G.add_edge(node_s2, row[col])  # 如果是s1列，则连接到root
            node_s3 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s3}")
        
        if col == 's4' and pd.notnull(row[col]):
            G.add_edge(node_s3, row[col])  # 如果是s1列，则连接到root
            node_s4 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s4}")

        if col == 's5' and pd.notnull(row[col]):
            G.add_edge(node_s4, row[col])  # 如果是s1列，则连接到root
            node_s5 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s5}")

        if col == 's6' and pd.notnull(row[col]):
            G.add_edge(node_s5, row[col])  # 如果是s1列，则连接到root
            node_s6 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s6}")

        if col == 's7' and pd.notnull(row[col]):
            G.add_edge(node_s6, row[col])  # 如果是s1列，则连接到root
            node_s7 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s7}")

        if col == 's8' and pd.notnull(row[col]):
            G.add_edge(node_s7, row[col])  # 如果是s1列，则连接到root
            node_s8 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s8}")

        if col == 's9' and pd.notnull(row[col]):
            G.add_edge(node_s8, row[col])  # 如果是s1列，则连接到root
            node_s9 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s9}")

        if col == 's10' and pd.notnull(row[col]):
            G.add_edge(node_s9, row[col])  # 如果是s1列，则连接到root
            node_s10 = row[col]  # 更新当前节点为s1的值
            print(f"当前节点值是{node_s10}")



# 绘制图
# pos = nx.spring_layout(G)  # 使用spring布局算法来定位节点
# pos = nx.circular_layout(G)
# pos = nx.shell_layout(G)  # nlist 是节点分层的列表
# pos = nx.spiral_layout(G)
# pos = nx.kamada_kawai_layout(G)
#pos = nx.spectral_layout(G)
pos = nx.planar_layout(G)   # ok
#pos = nx.random_layout(G)

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=50, font_size=6, font_weight='light', arrows=True)
plt.title('CSV File Structure')
plt.show()