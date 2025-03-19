import pandas as pd

def standardize_csv(input_file,output_file):
    """
    将非标准的 CSV 文件处理为标准的 CSV 文件，并保存为 Python 可以轻松读取的格式。
    参数:
    - input_file: 输入文件路径（非标准 CSV 文件）
    - output_file: 输出文件路径（标准 CSV 文件）
    """
    df = None  # 初始化 df
    # 尝试不同的分隔符
    try:
        # 尝试用逗号分隔
        df = pd.read_csv(input_file, sep=',', encoding='utf-8')
        print("使用逗号分隔符读取成功！")
    except Exception as e:
        print("使用逗号分隔符读取失败，尝试其他分隔符。")
        try:
            # 尝试用制表符分隔
            df = pd.read_csv(input_file, sep='\t', encoding='utf-8-sig')
            print("使用制表符分隔符读取成功！")
        except Exception as e:
            print("使用制表符分隔符读取失败，尝试其他分隔符。")
            try:
                # 尝试用空格分隔
                df = pd.read_csv(input_file, sep=' ', encoding='utf-8-sig')
                print("使用空格分隔符读取成功！")
            except Exception as e:
                print("使用空格分隔符读取失败，尝试其他分隔符。")
                try:
                    # 尝试用分号分隔
                    df = pd.read_csv(input_file, sep=';', encoding='utf-8-sig')
                    print("使用分号分隔符读取成功！")
                except Exception as e:
                    print("无法确定分隔符，请手动检查文件。")
                    with open(input_file,'r',encoding='utf-8-sig') as f:
                        lines = f.readline()
                    header = lines[0].strip().split()  # 按空格或者制表符拆分列名
                    data = [line.strip().split() for line in lines[1:]]  # 按空格或者制表符拆分列名

                    # 将数据转换为 DataFrame
                    df = pd.DataFrame(data, columns=header)

    # 打印数据框的前几行
    print("文件内容预览：")
    print(df.head())
    print("文件列数:", len(df.columns))
    print("列名:", df.columns.tolist())
    # 保存为标准的 CSV 文件
    df.to_csv(output_file, index=False, encoding='utf-8-sig', sep=',')
    print(f"文件已保存为 {output_file}")

# 文件路径
file_path1 = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\visualization code\point_v1_v1_edge_types.csv'
output_path1 = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\visualization code\standard_point_v1_v1_edge_types.csv'
standardize_csv(file_path1, output_path1)

file_path2 = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\visualization code\v1_v1_edge_types.csv'
output_path2 = r'C:\Users\ChenYi\Desktop\network_simulation\Bouton Density\visualization code\standard_v1_v1_edge_types.csv'
standardize_csv(file_path2, output_path2)




