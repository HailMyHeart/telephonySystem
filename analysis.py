import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

def extract_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        capacity = None
        block_rate = None
        for line in file:
            if line.startswith('capacity'):
                capacity = float(line.split()[-1])
            elif line.startswith('block rate'):
                block_rate = float(line.split()[-1].strip('%'))
                if capacity is not None and block_rate is not None:
                    data.append((capacity, block_rate))
                    capacity = None
                    block_rate = None
    return data

def process_file(file_path):
    data = extract_data_from_file(file_path)
    data.sort(key=lambda x: x[0])  # 按照 capacity 排序
    
    capacities, block_rates = zip(*data)  # 解压数据
    capacities = [str(int(capacity)) for capacity in capacities]
    block_rates = list(block_rates)
    
    # 使用Seaborn风格生成柱状图
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 3))
    ax = sns.barplot(x=capacities, y=block_rates, color='blue', ci=None, width=0.4)  # 统一颜色为蓝色，调整柱子宽度
    plt.xlabel('Number of Channels per Direction')
    plt.ylabel('Call Blocking Rate (%)')
    plt.title('Blocking Rate vs. Number of Channels in the Uni-Directional System', pad=20)
    
    # 在每个柱形上标明 y 值
    for i, v in enumerate(block_rates):
        ax.text(i, v, f"{v:.2f}%", ha='center', va='bottom')  # 调整 y 值的位置
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bi-30.txt')
    process_file(file_path)