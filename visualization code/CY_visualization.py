''' Basic statistical analysis and visualization of spikes files of V1 point model.  2025-03-17  Author:Chen Yi '''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import correlate

# 加载spike文件
spike_data = pd.read_csv('point_spikes.csv', delim_whitespace=True, header=0)
print(spike_data.head())

node_type_data = pd.read_csv('v1_nodes.csv', delim_whitespace=True, header=0)

# 根据 id 和 node_ids 进行匹配，将 ei 列添加到 spike_data_ei里
spike_data_ei = pd.merge(
    spike_data,  # 左表
    node_type_data[['id', 'ei']],  # 右表，只选择 id 和 ei 列
    left_on='node_ids',  # 左表的匹配列
    right_on='id',  # 右表的匹配列
    how='left'  # 左连接，保留 spike_data 的所有行
)
# 打印前 100 行
print(spike_data_ei.head(100))

# 保存新的 spike_data 文件
spike_data_ei.to_csv('spike_data_ei.csv', index=False, sep=' ')

# 根据 ei 列的值设置颜色
color_map = {'e': 'red', 'i': 'blue'}  # 定义颜色映射
colors = spike_data_ei['ei'].map(color_map)  # 将 ei 列的值映射为颜色

# 绘制散点图
plt.figure(figsize=(10, 10))  # 设置画布大小
plt.scatter(x=spike_data_ei['timestamps'], y=spike_data_ei['node_ids'], c=colors, s=2, alpha=0.3,edgecolors='none')

plt.title('Spike Timestamps vs Node IDs', fontsize=14)
plt.xlabel('Timestamps (ms)', fontsize=12)
plt.ylabel('Node IDs', fontsize=12)
plt.show()


# 单独计算每个神经元的平均发放频率
spike_counts = spike_data['node_ids'].value_counts()   # value_counts用于统计每个node id在列中出现的次数
total_time = spike_data['timestamps'].max() - spike_data['timestamps'].min()  # time stamps的单位是ms
total_time = total_time / 1000    # ms -> s
average_firing_rates = spike_counts / total_time   # Hz 每秒发放次数

print("Spike counts per neuron:\n", spike_counts)
print("Total time in seconds:", total_time)
print("Average firing rates per neuron (Hz):\n", average_firing_rates)


# 计算平均每个神经元的放电次数
total_spikes = len(spike_data)
num_neurons = spike_data['node_ids'].nunique()
average_spikes_per_neuron = total_spikes / num_neurons

print("Total number of spikes:", total_spikes)
print("Number of unique neurons:", num_neurons)
print("Average spikes per neuron:", average_spikes_per_neuron)


# 发放时间直方图
plt.figure(figsize=(10, 6))
sns.histplot(spike_data['timestamps'], bins=50, kde=True)
plt.title('Spike Timestamps Distribution')
plt.xlabel('Time (ms)')
plt.ylabel('Frequency')
plt.show()

# 发放频率图

plt.figure(figsize=(10, 6))
plt.scatter(average_firing_rates.index,average_firing_rates.values,alpha=0.5)
print(type(average_firing_rates.index))
print(type(average_firing_rates.values))
plt.title('Average Firing Rates per Neuron')
plt.xlabel('Neuron/Node ID')
plt.ylabel('Firing Rate (Hz)')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(y=average_firing_rates)
plt.title('Distribution of Firing Rates')
plt.ylabel('Firing Rate (Hz)')
plt.show()

'''
# 发放模式图（选择一个神经元）
neuron_id = 125771  # 选择一个神经元ID
neuron_spikes = spike_data[spike_data['node_ids'] == neuron_id]['timestamps']
plt.figure(figsize=(10, 6))
plt.eventplot(neuron_spikes, orientation='horizontal', colors='b')
plt.title(f'Spike Train for Neuron {neuron_id}')
plt.xlabel('Time (ms)')
plt.ylabel('Spikes')
plt.show()



# 交叉相关分析（选择两个神经元）
neuron1_spikes = spike_data[spike_data['node_ids'] == 125771]['timestamps']
neuron2_spikes = spike_data[spike_data['node_ids'] == 120162]['timestamps']
cross_corr = correlate(neuron1_spikes, neuron2_spikes, mode='full')
plt.figure(figsize=(10, 6))
plt.plot(cross_corr)
plt.title('Cross-Correlation between Neuron 125771 and Neuron 120162')
plt.xlabel('Lag')
plt.ylabel('Correlation')
plt.show()
'''

# 保存发放频率数据
average_firing_rates.to_csv('average_firing_rates.csv')

# 保存发放时间直方图
plt.savefig('spike_timestamps_distribution.png')