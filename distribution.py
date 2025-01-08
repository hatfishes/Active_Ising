import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
# Parameters
Lx = 1000
Ly = 1
J_set = 1
BIN = 100
# Initialize directories and lists
data_dir = {}
listdir = os.listdir("data/")
Heat_cap_list = []
Magnet_sus_list = []
T_list = []
T_conti = np.array([])  # Continuous T sequence for analytical curves
ave_ener_list = []
ave_mag_list = []

# 定义文件夹路径
folder_path = 'data/'
filename_pattern = re.compile(r'k(\d+(\.\d+)?)L(\d+)T(\d+(\.\d+)?)\.csv')
for file in listdir:
# 使用正则表达式检查文件名是否匹配
    match = filename_pattern.match(file)
    if match:
        # 如果文件名匹配，则提取参数值并读取CSV文件
        # 如果文件名匹配，则提取参数值并读取CSV文件
        k = float(match.group(1))  # k 可能是整数或浮点数
        Lx = int(match.group(3))  # L 是整数
        T = float(match.group(4))  # T 可能是整数或浮点数
        file_path = os.path.join(folder_path, file)

        #file_path = os.path.join("data/", file)
        print(file)
        #T = float(file)
        #data = pd.read_csv(file_path, delim_whitespace=True)
        data = pd.read_csv(file_path)
        data_dir[file] = data

        step = data["step"]
        lenth = len(step)
        half_len = int(lenth / 2)
        Energy = data["Energy"]
        Magnet = data["Magnet"]
        acc = data["acc"]
        J = data["J"]
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

        axes[1, 0].hist(acc, bins=BIN)
        axes[1, 0].set_title(f'Acceptance Rate, T={file}')
        axes[1, 0].set_xlabel('Acceptance Rate')
        axes[1, 0].set_ylabel('Frequency')

        axes[1, 1].hist(J, bins=BIN)
        axes[1, 1].set_xlim(1.0,1.3)
        axes[1, 1].set_title('J')
        axes[1, 1].set_xlabel('J')
        axes[1, 1].set_ylabel('Frequency')

        plt.savefig("distri/" + file + "_distri.png")
        #plt.close(fig)


