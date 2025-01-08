import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
# 读取数据文件
Lx = 10000
Ly = 1
J_set = 1
num_splits = 500


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
binder_list = []
binder_err_list = []


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
        N = len(step)
        half_len = int(lenth / 2)
        Energy = data["Energy"][half_len:]
        Magnet = data["Magnet"][half_len:]
        acc = data["acc"]
        J = data["J"]

        mean_E = np.mean(Energy)
        mean_E2 = np.mean(Energy**2)

        mean_M = np.mean(Magnet)
        mean_M2 = np.mean(Magnet**2)
        mean_M4 = np.mean(Magnet**4)

        std_E = np.std(Energy,ddof=1)
        std_E2 = np.std((Energy)**2,ddof=1)

        std_M = np.std(Magnet,ddof=1)
        std_M2 = np.std(Magnet**2,ddof=1)
        std_M4 = np.std(Magnet**4,ddof=1)
        
        sigma_mean_E = std_E / np.sqrt(N) 
        sigma_mean_E2 = std_E2 / np.sqrt(N) 
        
        
        sigma_mean_M = std_M / np.sqrt(N) 
        sigma_mean_M2 = std_M2 / np.sqrt(N) 
    #计算热容
        dC_d_mean_E = -(2/(T**2)) * mean_E
        dC_d_mean_E2 = 1/(T**2)
        #sigma_C = np.sqrt((dC_d_mean_E * sigma_mean_E)**2 *(dC_d_mean_E2 * sigma_mean_E2)**2) 
        Heat_cap = (1 / (T**2)) * (mean_E2 - mean_E**2) *Lx
        Heat_cap_err = np.sqrt((dC_d_mean_E * sigma_mean_E)**2 *(dC_d_mean_E2 * sigma_mean_E2)**2)*Lx
    

    #计算磁导率
        dchi_d_mean_M = -(2/(T**2)) * mean_M 
        dchi_d_mean_M2 = 1/ (T**2)
        Magnet_sus = (1/(T**2)) *(mean_M2 - mean_M**2) 
        Magnet_sus_err =np.sqrt((dchi_d_mean_M * sigma_mean_M) **2 + (dchi_d_mean_M2 * sigma_mean_M2)**2) 

    #计算binder cumulant
        U4 = mean_M4 / mean_M2**2
        sigma_U4 = np.sqrt((1/ mean_M2**2  * std_M4 )**2 + (-2* mean_M4 / mean_M2**3 * std_M2)**2  ) 


        #binder = np.mean(binder_splits)
        #binder_err = np.std(binder_splits, ddof=1)
        
        Heat_cap_list.append(Heat_cap)
        Heat_cap_err_list.append(Heat_cap_err)
        Magnet_sus_list.append(Magnet_sus)
        Magnet_sus_err_list.append(Magnet_sus_err)
        binder_list.append(U4)
        binder_err_list.append(sigma_U4)

        T_list.append(T)

        #ave_ener = np.mean(Energy)
        #ave_ener_err = np.std(Energy) / np.sqrt(len(Energy))
        ave_ener_list.append(mean_E)
        ave_ener_err_list.append(std_E)

        #ave_mag = np.mean(abs(Magnet))
        #ave_mag_err = np.std(abs(Magnet)) / np.sqrt(len(Magnet))
        ave_mag_list.append(mean_M)
        ave_mag_err_list.append(std_M)

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
#axes[0, 0].plot(T_list, Heat_cap_list)
axes[0, 0].set_title('Heat Capacity')
axes[0, 0].set_xlabel('temp')
axes[0, 0].set_ylabel('Heat Capacity')

axes[0, 1].errorbar(T_list, Magnet_sus_list, yerr=Magnet_sus_err_list, fmt='o', capsize=5)
#axes[0, 1].plot(T_conti, Magnet_sus_conti)
#axes[0, 0].plot(T_list,Magnet_sus_list)
axes[0, 1].set_title('Magnetic Susceptibility')
axes[0, 1].set_xlabel('temp')
axes[0, 1].set_ylabel('Magnetic Susceptibility')

axes[1, 0].errorbar(T_list, ave_ener_list, yerr=ave_ener_err_list, fmt='o', capsize=5)
axes[1, 0].plot(T_conti, ener_conti)
#axes[1, 0].plot(T_list,ave_ener_list )
axes[1, 0].set_title('Average Energy')
axes[1, 0].set_xlabel('temp')
axes[1, 0].set_ylabel('Average Energy')

axes[1, 1].errorbar(T_list, ave_mag_list, yerr=ave_mag_err_list, fmt='o', capsize=5)
axes[1, 1].set_title('Average Magnetization')
axes[1, 1].set_xlabel('temp')
axes[1, 1].set_ylabel('Average Magnetization')

#axes[0, 2].errorbar(T_list, binder_list, yerr=binder_err_list, fmt='o', capsize=5)
#axes[0, 2].set_title('Binder Cumulant')
#axes[0, 2].set_xlabel('temp')
#axes[0, 2].set_ylabel('Binder Cumulant')


picturename = "img/newplotk"+str(k) + "L" + str(Lx)   +".png"
plt.savefig(picturename)
plt.show()

print("T", "Heat_cap", "Heat_cap_err", "Magnet_sus", "Magnet_sus_err", "magnetization", "magnetization_err")
for i in range(len(T_list)):
    print(T_list[i], Heat_cap_list[i], Heat_cap_err_list[i], Magnet_sus_list[i], Magnet_sus_err_list[i], ave_mag_list[i], ave_mag_err_list[i])


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
        'Average Magnetization Error': ave_mag_err_list,
        'binder cumulant':binder_list,
        'binder cumulant error':binder_err_list
    })
    df.to_csv(filename, index=False)

# 保存数据
outputfilename = "Thermos/thermok" + str(k) + "L" + str(Lx) + ".csv"
save_data_to_csv(outputfilename, T_list, Heat_cap_list, Heat_cap_err_list, Magnet_sus_list, Magnet_sus_err_list, ave_ener_list, ave_ener_err_list, ave_mag_list, ave_mag_err_list)


