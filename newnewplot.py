import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 读取数据文件
Lx = 20000
Ly = 1
J_set = 1
data_dir = {}
listdir = os.listdir("data/")
Heat_cap_list = []
Magnet_sus_list = []
Heat_cap_err_list = []
Magnet_sus_err_list = []
T_list = []
T_conti = np.array([])  # 连续的T序列，用于解析绘制曲线
ave_ener_list = []
ave_ener_err_list = []
ave_mag_list = []
ave_mag_err_list = []

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

    # 将数据分成10份
    num_splits = 10
    split_size = (lenth - half_len) // num_splits
    Heat_cap_splits = []
    Magnet_sus_splits = []

    for i in range(num_splits):
        start_idx = half_len + i * split_size
        end_idx = start_idx + split_size

        Energy_split = Energy[start_idx:end_idx]
        Magnet_split = Magnet[start_idx:end_idx]

        ave_ener_split = np.mean(Energy_split)
        ave_ener_2_split = np.mean(Energy_split**2)
        Heat_cap_split = (ave_ener_2_split - ave_ener_split**2) / (T**2) * Lx

        ave_mag_split = np.mean(Magnet_split)
        ave_mag_2_split = np.mean(Magnet_split**2)
        Magnet_sus_split = (ave_mag_2_split - ave_mag_split**2) / T * Lx

        Heat_cap_splits.append(Heat_cap_split)
        Magnet_sus_splits.append(Magnet_sus_split)

    Heat_cap = np.mean(Heat_cap_splits)
    Heat_cap_err = np.std(Heat_cap_splits, ddof=1)

    Magnet_sus = np.mean(Magnet_sus_splits)
    Magnet_sus_err = np.std(Magnet_sus_splits, ddof=1)

    Heat_cap_list.append(Heat_cap)
    Heat_cap_err_list.append(Heat_cap_err)
    Magnet_sus_list.append(Magnet_sus)
    Magnet_sus_err_list.append(Magnet_sus_err)
    T_list.append(T)

    ave_ener = np.mean(Energy[half_len:])
    ave_ener_err = np.std(Energy[half_len:]) / np.sqrt(len(Energy[half_len:]))
    ave_ener_list.append(ave_ener)
    ave_ener_err_list.append(ave_ener_err)

    ave_mag = np.mean(abs(Magnet[half_len:]))
    ave_mag_err = np.std(abs(Magnet[half_len:])) / np.sqrt(len(Magnet[half_len:]))
    ave_mag_list.append(ave_mag)
    ave_mag_err_list.append(ave_mag_err)

# 定义各个热力学函数的解析式
def Magnet_sus(T):
    return (1 / T) * np.exp(2 * J_set / T)

def Heat_cap(T):
    numerator = 4 * J_set**2 * np.exp(-2 * J_set / T)
    denominator = T**2 * (1 + np.exp(-2 * J_set / T))**2
    return numerator / denominator

def ener(T):
    return -J_set * ((1 - np.exp(-2 * J_set / T)) / (1 + np.exp(-2 * J_set / T)))

T_conti = np.linspace(min(T_list), max(T_list), 1000)
Magnet_sus_conti = Magnet_sus(T_conti)
Heat_cap_conti = Heat_cap(T_conti)
ener_conti = ener(T_conti)

# 创建子图
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
fig.tight_layout(pad=3.0)

# 绘制各个图表
axes[0, 0].errorbar(T_list, Heat_cap_list, yerr=Heat_cap_err_list, fmt='o', capsize=5)
axes[0, 0].plot(T_conti, Heat_cap_conti)
axes[0, 0].set_title('Heat Capacity')
axes[0, 0].set_xlabel('temp')
axes[0, 0].set_ylabel('Heat Capacity')

axes[0, 1].errorbar(T_list, Magnet_sus_list, yerr=Magnet_sus_err_list, fmt='o', capsize=5)
#axes[0, 1].plot(T_conti, Magnet_sus_conti)
axes[0, 1].set_title('Magnetic Susceptibility')
axes[0, 1].set_xlabel('temp')
axes[0, 1].set_ylabel('Magnetic Susceptibility')

axes[1, 0].errorbar(T_list, ave_ener_list, yerr=ave_ener_err_list, fmt='o', capsize=5)
axes[1, 0].plot(T_conti, ener_conti)
axes[1, 0].set_title('Average Energy')
axes[1, 0].set_xlabel('temp')
axes[1, 0].set_ylabel('Average Energy')

axes[1, 1].errorbar(T_list, ave_mag_list, yerr=ave_mag_err_list, fmt='o', capsize=5)
axes[1, 1].set_title('Average Magnetization')
axes[1, 1].set_xlabel('temp')
axes[1, 1].set_ylabel('Average Magnetization')


def save_data_to_csv(filename, T_list, Heat_cap_list, Heat_cap_err_list, Magnet_sus_list, Magnet_sus_err_list, ave_ener_list, ave_ener_err_list, ave_mag_list, ave_mag_err_list):
    df = pd.DataFrame({
        'Temperature': T_list,
        'Heat Capacity': Heat_cap_list,
        'Heat Capacity Error': Heat_cap_err_list,
        'Magnetic Susceptibility': Magnet_sus_list,
        'Magnetic Susceptibility Error': Magnet_sus_err_list,
        'Average Energy': ave_ener_list,
        'Average Energy Error': ave_ener_err_list,
        'Average Magnetization': ave_mag_list,
        'Average Magnetization Error': ave_mag_err_list
    })
    df.to_csv(filename, index=False)

# 保存数据
save_data_to_csv("thermodynamic_data.csv", T_list, Heat_cap_list, Heat_cap_err_list, Magnet_sus_list, Magnet_sus_err_list, ave_ener_list, ave_ener_err_list, ave_mag_list, ave_mag_err_list)



plt.savefig("img/newplot.png")
plt.show()

print("T", "Heat_cap", "Heat_cap_err", "Magnet_sus", "Magnet_sus_err", "magnetization", "magnetization_err")
for i in range(len(T_list)):
    print(T_list[i], Heat_cap_list[i], Heat_cap_err_list[i], Magnet_sus_list[i], Magnet_sus_err_list[i], ave_mag_list[i], ave_mag_err_list[i])

