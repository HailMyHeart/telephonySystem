import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

def extract_counts_from_file(file_path):
    failure_rates = []
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            success_matches = re.findall(r"Success Total\s+(\d+)", content)
            blocked_matches = re.findall(r"Blocked Total\s+(\d+)", content)

            if len(success_matches) == len(blocked_matches):
                for success, blocked in zip(success_matches, blocked_matches):
                    success_count = int(success)
                    blocked_count = int(blocked)
                    failure_rate = calculate_failure_rate(success_count, blocked_count)
                    failure_rates.append(failure_rate)
            else:
                print(f"Mismatch in counts between Success Total and Blocked Total in file {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    
    return failure_rates

def calculate_failure_rate(success_count, blocked_count):
    total_count = success_count + blocked_count
    if (total_count == 0):
        return 0  # Avoid division by zero
    return blocked_count / total_count

def process_files(directory_path):
    results = {}
    pattern = re.compile(r"dual_(\d+)\.txt$")
    
    for filename in os.listdir(directory_path):
        match = pattern.match(filename)
        if match:
            file_path = os.path.join(directory_path, filename)
            failure_rates = extract_counts_from_file(file_path)
            
            if failure_rates:
                avg_failure_rate = sum(failure_rates) / len(failure_rates)
                results[filename] = avg_failure_rate * 100  # Convert to percentage
            else:
                results[filename] = None
    
    filenames = []
    failure_rates = []
    labels = []
    
    for filename, failure_rate in results.items():
        if failure_rate is not None:
            filenames.append(filename)
            failure_rates.append(failure_rate)
            total_channels = re.findall(r'\d+', filename)[0]
            labels.append(total_channels)
            print(f"{filename}: {failure_rate:.2f}%")
        else:
            print(f"{filename}: No valid data found")
    
    # 使用Seaborn风格生成柱状图
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 4))
    ax = sns.barplot(x=labels, y=failure_rates, color='blue')  # 统一颜色为蓝色
    plt.xlabel('Total Number of Channels')
    plt.ylabel('Call Blocking Rate (%)')
    plt.title('Finding the Optimal Channel Capacity to Ensure QoS ≤ 5% Blocking')
    
    # 在每个柱形上标明 y 值
    for i, v in enumerate(failure_rates):
        ax.text(i, v + 0.1, f"{v:.2f}%", ha='center', va='bottom')  # 调整 y 值的位置
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    directory_path = os.path.dirname(os.path.abspath(__file__))  # Use the script's directory
    process_files(directory_path)
