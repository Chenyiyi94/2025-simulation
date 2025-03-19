import h5py

# 指定.h5文件的路径
file_path = r'C:\Users\ChenYi\Desktop\Data\lyuyinCluster\v1_nodes.h5'

# 以只读模式打开.h5文件
with h5py.File(file_path, 'r') as f:
    # 打印文件中包含的所有对象（组和数据集）
    print("Objects in the HDF5 file:")
    for name in f:
        print(name)

    # 示例：访问并打印特定数据集的内容
    dataset_name = 'nodes'  # 替换为实际的数据集名称
    dataset = f[dataset_name]
    print(dataset.name)
