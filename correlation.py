import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Parameters
Lx = 1000
Ly = 1
J_set = 1
BIN = 30

n_config = 1
cutoff = 100
# Initialize directories and lists
data_dir = {}
listdir = os.listdir("data/")
Heat_cap_list = []
Magnet_sus_list = []
T_list = []
T_conti = np.array([])  # Continuous T sequence for analytical curves
ave_ener_list = []
ave_mag_list = []


# 计算单个构型的关联函数
def correlation_function_single_config(config, r):
    N = len(config)
    spin_correlation = np.mean([config[i % N] * config[(i + r) % N] for i in range(N)])
    return spin_correlation
    
# 计算给定多个构型的平均关联函数
def average_correlation_function(configurations):
    N = len(configurations[0])  # 假设所有构型长度相同
    total_steps = len(configurations)
    print(N,total_steps)
    
    # 计算每个距离 r 的关联函数并取平均
    correlation_results = []
    for r in range(0, cutoff):  # r = 1 到 N-1
        correlation_sum = 0
        for config in configurations:
            correlation_sum += correlation_function_single_config(config, r) - np.mean(config)**2
        correlation_avg = correlation_sum / total_steps
        correlation_results.append(correlation_avg)
    
    return correlation_results



# Read and process each data file
for file in listdir:
    file_path = os.path.join("data/", file)
    print(file)
    T = float(file)
    data = pd.read_csv(file_path, delim_whitespace=True)
    data_dir[file] = data 
    
    
    step = data["step"]
    lenth = len(step)
    half_len = int(lenth / 2)
    Energy = data["Energy"]
    Magnet = data["Magnet"]
    acc = data["acc"]
    J = data["J"]
    
    Lx = len(data['config'][0])
    ###读取构型ss
    configurations = []
    for config in data['config'][-n_config:]:
        spins = [1 if spin == '+' else -1 for spin in config.strip()]
        configurations.append(spins)
    # 计算所有构型的平均关联函数
    correlation_results = average_correlation_function(configurations)
    r_values = range(0, len(correlation_results) )  # 距离 r 从 1 开始
    #r_values = range(1, 100)

        
    #J = data["J"][half_len:]

    # Create subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    fig.tight_layout(pad=3.0)

    # Plot histograms
    axes[0, 0].hist(Energy, bins=BIN)
    axes[0, 0].set_title('Energy')
    axes[0, 0].set_xlabel('Energy')
    axes[0, 0].set_ylabel('Frequency')

    axes[0, 1].hist(Magnet, bins=BIN)
    axes[0, 1].set_xlim(-1.1,1.1)
    axes[0, 1].set_title('Magnetization')
    axes[0, 1].set_xlabel('Magnetization')
    axes[0, 1].set_ylabel('Frequency')

    #axes[1, 0].plot(r_values, correlation_results, marker='o', linestyle='-')
    axes[1, 0].plot(r_values, correlation_results)
    axes[1, 0].set_xlim(0, len(correlation_results))
    axes[1, 0].set_title('Correlation Function')
    axes[1, 0].set_xlabel('Distance r')
    axes[1, 0].set_ylabel('C(r)')
    #axes[1, 0].grid(True)
    ######
    #axes[1, 0].hist(acc, bins=BIN)
    #axes[1, 0].set_title(f'Acceptance Rate, T={file}')
    #axes[1, 0].set_xlabel('Acceptance Rate')
    #axes[1, 0].set_ylabel('Frequency')
    ######
    
    
    axes[1, 1].hist(J, bins=BIN)
    axes[1, 1].set_xlim(1.0,1.3)
    axes[1, 1].set_title('J')
    axes[1, 1].set_xlabel('J')
    axes[1, 1].set_ylabel('Frequency')

    plt.savefig("distri/" + file + "_distri.png")
    #plt.close(fig)


