#数据读取，从data文件中读
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re   
import xarray as xr
# 读取数据文件
#参数header:哪一行是数据的名字
#参数delim:用什么符号作为分隔符，参数值是字符串，比如：';'分号   '\t'制表符
#skiprows.  skipfooter. 跳过头尾多少行，参数值是int
Lx = 20000
Ly = 1
J_set = 1

# 定义文件夹路径
folder_path = 'data/'
#正则表达式
filename_pattern = re.compile(r'k(\d+(\.\d+)?)L(\d+)T(\d+(\.\d+)?)\.csv')
#这是一个字典??或许不用字典更好
data_dir = {}
params_dir = {}
#这是文件名字列表？
listdir = os.listdir("data/")


# 读取数据，输入是数据文件地址，返回是参数与数据的字典
def read_data(listdir):
    ##遍历文件夹中的文件，读取数据，存储在params_dir中
    for file in listdir:
    # 使用正则表达式检查文件名是否匹配
        match = filename_pattern.match(file)
        if match:
            # 如果文件名匹配，则提取参数值并读取CSV文件
            file_path = os.path.join(folder_path, file)
            print(file)

            #data = pd.read_csv(file_path, delim_whitespace=True)
            data = pd.read_csv(file_path)
            #data_dir[file] = data


            TotalStep = data["step"].iloc[-1]
            k = float(match.group(1))  # k 可能是整数或浮点数
            Lx = int(match.group(3))  # L 是整数
            T = float(match.group(4))  # T 可能是整数或浮点数

            params_dir[(k, Lx, T, TotalStep, file)] = data
            print(k,Lx,T,TotalStep,file)
    return params_dir


##这个是用来画图的，输入参数与数据的字典，输出图片，保存在img文件夹中
def plot_for_each(params_dir):
    for params,data in params_dir.items():
        step = data["step"]
        lenth = len(step)
        half_len = int(lenth /2)
        Energy = data["Energy"]
        Magnet = data["Magnet"]
        acc = data["acc"]
        #h = data["h"]
        J = data["J"]
        ## 创建子图
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
        fig.tight_layout(pad=3.0)


        # 定义滑动窗口大小和阈值
        window_size = 1000
        threshold = 0.25
        # 数据平滑
        smoothed_magnet = sliding_window_average(Magnet, window_size)
        smoothed_enrgy = sliding_window_average(Energy, window_size)
        # 检测跳转点（稳定段之间的边界）
        jump_indices = jump_point(data, window_size, threshold)


        # 绘制各个图表
        #axes[0, 0].scatter(step, Energy)
        axes[0, 0].plot(step, Energy)
        axes[0, 0].plot(step, smoothed_enrgy)
        axes[0, 0].set_title('Energy')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Energy')
        for jump_index in jump_indices:
            axes[0, 0].axvline(x=step[jump_index], color='r', linestyle='--', label='Jump Point' if jump_index == jump_indices[0] else "")

        #axes[0, 1].scatter(step, Magnet)
        axes[0, 1].plot(step, Magnet)
        axes[0, 1].plot(step, smoothed_magnet)
        axes[0, 1].set_ylim(-1.1, 1.1)
        axes[0, 1].set_title('Magnet')
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Magnet')
        for jump_index in jump_indices:
            axes[0, 1].axvline(x=step[jump_index], color='r', linestyle='--', label='Jump Point' if jump_index == jump_indices[0] else "")


        axes[1, 0].plot(step, acc)
        axes[1, 0].set_title('acc,,T='+params[-1])
        axes[1, 0].set_xlabel('Step')
        axes[1, 0].set_ylabel('acc')
        for jump_index in jump_indices:
            axes[1, 0].axvline(x=step[jump_index], color='r', linestyle='--', label='Jump Point' if jump_index == jump_indices[0] else "")

        axes[1, 1].plot(step, J)
        axes[1, 1].set_title('J')
        axes[1, 1].set_ylim(min(J), max(J))
        #axes[1, 1].set_ylim(-0.1, 0.1)
        axes[1, 1].set_xlabel('Step')
        axes[1, 1].set_ylabel('J')
        for jump_index in jump_indices:
            axes[1, 1].axvline(x=step[jump_index], color='r', linestyle='--', label='Jump Point' if jump_index == jump_indices[0] else "")

        plt.savefig("img/"+params[-1]+".png")


def jump_point(data, window_size, threshold):

    Magnet = data["Magnet"]
    # 数据平滑
    smoothed_magnet = sliding_window_average(Magnet, window_size)
    #smoothed_enrgy = sliding_window_average(Energy, window_size)

    # 滑动窗口判断稳定性
    stable_indices = []
    for i in range(len(Magnet) - window_size + 1):
        window = smoothed_magnet[i:i + window_size]
        if is_stable(window, threshold):
            stable_indices.append(i + window_size - 1)  # 记录窗口末尾为稳定点
            
        # 检测跳转点（稳定段之间的边界）
    jump_indices = [stable_indices[i] for i in range(1, len(stable_indices)) if stable_indices[i] > stable_indices[i - 1] + 1]
    return jump_indices


def sliding_window_average(data, window_size):
    # 计算滑动平均
    smoothed = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    
    # 计算填充大小，使得填充后的数据与原始数据长度一致
    padding = (window_size - 1) // 2  # 前后填充的大小
    
    # 填充数据，确保长度与原始数据一致
    smoothed_padded = np.pad(smoothed, (padding, padding), mode='edge')
    
    # 如果原始数据长度更大，填充的边界也应该补充
    if len(smoothed_padded) < len(data):
        smoothed_padded = np.pad(smoothed_padded, (0, len(data) - len(smoothed_padded)), mode='edge')
    
    return smoothed_padded

# 定义一个函数判断稳定性
def is_stable(window, threshold):
    return (np.max(window) - np.min(window)) < threshold

def calculate_thermo(params_dir):
    # 定义滑动窗口大小和阈值
    window_size = 50
    threshold = 0.1
    # 用于存储数据
    thermos = []
    # 遍历每个参数组合的数据
    for params, data in params_dir.items():

        # 定义滑动窗口大小和阈值
        window_size = 1000
        threshold = 0.25
        # 检测跳转点（稳定段之间的边界）
        jump_indices = jump_point(data, window_size, threshold)

        # 将数据分段
        segments = np.split(data, jump_indices) # 按照跳转点分段

        segments_0 = [segment for segment in segments if np.abs(segment["Magnet"].mean()) < 0.1]
        segments_1 = [segment for segment in segments if np.abs(segment["Magnet"].mean()) >= 0.1]

        segment_0 = pd.concat(segments_0) if segments_0 else pd.DataFrame()
        segment_1 = pd.concat(segments_1) if segments_1 else pd.DataFrame()

        mean_E_0 = segment_0["Energy"].mean() if not segment_0.empty else np.nan
        mean_M_0 = segment_0["Magnet"].mean() if not segment_0.empty else np.nan
        std_E_0 = segment_0["Energy"].std() if not segment_0.empty else np.nan
        std_M_0 = segment_0["Magnet"].std() if not segment_0.empty else np.nan

        mean_E_1 = segment_1["Energy"].mean() if not segment_1.empty else np.nan
        mean_M_1 = segment_1["Magnet"].mean() if not segment_1.empty else np.nan
        std_E_1 = segment_1["Energy"].std() if not segment_1.empty else np.nan
        std_M_1 = segment_1["Magnet"].std() if not segment_1.empty else np.nan

        if not segment_0.empty:
            state_0 = [mean_E_0, mean_M_0, std_E_0, std_M_0]
            thermos.append([params[0], params[1], params[2], params[3], state_0])
        
        if not segment_1.empty:
            state_1 = [mean_E_1, abs(mean_M_1), std_E_1, std_M_1]
            thermos.append([params[0], params[1], params[2], params[3], state_1])
    
    print(thermos)
    print(len(thermos))
    # 将数据保存到CSV文件
    expanded_thermos = []
    for thermo in thermos:
        k, Lx, T, TotalStep, state = thermo
        mean_E, mean_M, std_E, std_M = state
        state_label = 0 if abs(mean_M) < 0.01 else 1
        expanded_thermos.append([k, Lx, T, TotalStep, mean_E, mean_M, std_E, std_M, state_label])
    thermo_df = pd.DataFrame(expanded_thermos, columns=['k', 'Lx', 'T', 'TotalStep', 'mean_E', 'mean_M', 'std_E', 'std_M', 'State'])
    thermo_df.to_csv('thermo_data.csv', index=False)
    return thermos

# 输入segment_ds，画出图像，保存在img文件夹中
def plot_thermos(thermos):
    # Group data by k
    grouped_thermos = {}
    for thermo in thermos:
        k, Lx, T, TotalStep, state = thermo
        if k not in grouped_thermos:
            grouped_thermos[k] = []
        grouped_thermos[k].append((T, state))

    # Plot mean_M and mean_E vs T for each k
    for k, data in grouped_thermos.items():
        data.sort()  # Sort by temperature T
        T_values = [item[0] for item in data]
        mean_E_values = [item[1][0] for item in data]
        std_E_values = [item[1][2] for item in data]
        mean_M_values = [item[1][1] for item in data]
        std_M_values = [item[1][3] for item in data]

        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 12))

        # Plotting Mean Energy vs Temperature with error bars and caps
        ax1.errorbar(T_values, mean_E_values, yerr=std_E_values, fmt='o', label=f'k={k}', capsize=5)
        ax1.set_xlabel('Temperature (T)')
        ax1.set_xlim(1.2, 1.4)
        ax1.set_ylabel('Mean Energy')
        ax1.set_title('Mean Energy vs Temperature')
        ax1.legend()

        # Plotting Mean Magnet vs Temperature with error bars and caps
        ax2.errorbar(T_values, mean_M_values, yerr=std_M_values, fmt='s', label=f'k={k}', capsize=5)
        ax2.set_xlabel('Temperature (T)')
        ax2.set_xlim(1.2, 1.4)
        ax2.set_ylabel('Mean Magnet')
        ax2.set_title('Mean Magnet vs Temperature')
        ax2.legend()

        # Add dashed lines between corresponding (k, T) pairs
        for i in range(1, len(T_values)):
            if T_values[i] == T_values[i-1]:  # Check if T values are the same
                ax1.plot(T_values[i-1:i+1], mean_E_values[i-1:i+1], 'k--', lw=1)
                ax2.plot(T_values[i-1:i+1], mean_M_values[i-1:i+1], 'k--', lw=1)

        fig.tight_layout()
        plt.savefig("img/thermo_mean_E_M_vs_T.png")
        plt.close(fig)



if __name__ == "__main__":
    params_dir = read_data(listdir)
    #plot_for_each(params_dir)
    thermos = calculate_thermo(params_dir)
    plot_thermos(thermos)


