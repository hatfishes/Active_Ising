import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re   

# 读取数据文件
#参数header:哪一行是数据的名字
#参数delim:用什么符号作为分隔符，参数值是字符串，比如：';'分号   '\t'制表符
#skiprows.  skipfooter. 跳过头尾多少行，参数值是int


Lx = 20000
Ly = 1
J_set = 1
#这是一个字典
data_dir = {}
#这是文件名字列表？
listdir = os.listdir("data/")
Heat_cap_list =[]
Magnet_sus_list = []
T_list = []
T_conti = np.array([]) #连续的T序列，用于解析绘制曲线
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
        half_len = int(lenth /2)
        Energy = data["Energy"]
        Magnet = data["Magnet"]
        acc = data["acc"]
        #h = data["h"]
        J = data["J"]
        ## 创建子图
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
        fig.tight_layout(pad=3.0)



        # 绘制各个图表
        #axes[0, 0].scatter(step, Energy)
        axes[0, 0].plot(step, Energy)
        axes[0, 0].set_title('Energy')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Energy')

        #axes[0, 1].scatter(step, Magnet)
        axes[0, 1].plot(step, Magnet)
        axes[0, 1].set_ylim(-1.1, 1.1)
        axes[0, 1].set_title('Magnet')
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Magnet')
        # 创建第二个y轴
        #ax2 = axes[0, 1].twinx()
        #ax2.plot(step, J, label='J', color='orange')
        #ax2.set_ylim(min(J), max(J))

        axes[1, 0].plot(step, acc)
        axes[1, 0].set_title('acc,,T='+file)
        axes[1, 0].set_xlabel('Step')
        axes[1, 0].set_ylabel('acc')

        axes[1, 1].plot(step, J)
        axes[1, 1].set_title('J')
        axes[1, 1].set_ylim(min(J), max(J))
        #axes[1, 1].set_ylim(-0.1, 0.1)
        axes[1, 1].set_xlabel('Step')
        axes[1, 1].set_ylabel('J')

        plt.savefig("img/"+file+".png")

        ########################在循环中要计算每一个file算出来的热容和磁化率
        ave_ener = np.mean(Energy[half_len:])
        #ave_mag = abs(np.mean(Magnet[5000:])) /Ly / Lx
        ave_mag = np.mean(Magnet[half_len:])

        ave_ener_2 = np.mean(Energy[half_len:]**2)
        #ave_mag_2 = np.mean(Magnet[5000:]**2)/Ly / Lx /Ly / Lx
        ave_mag_2 = np.mean(Magnet[half_len:]**2)

        Heat_cap = (ave_ener_2 - ave_ener **2  )/(T**2) * Lx
        Magnet_sus = (ave_mag_2 - ave_mag **2 )/T *Lx
        Heat_cap_list.append(Heat_cap)
        Magnet_sus_list.append(Magnet_sus)
        T_list.append(T)
        ave_ener_list.append(ave_ener)
        ave_mag_list.append(ave_mag)

#定义各个热力学函数的解析式
def Magnet_sus(T):
    return (1 / T) * np.exp(2 * J_set / T)

def Heat_cap(T):
    numerator = 4 * J_set**2 * np.exp(-2 * J_set / T)
    denominator = T**2 * (1 + np.exp(-2 * J_set / T))**2
    return numerator / denominator

def ener(T):
    return -J_set * ((1 - np.exp(-2 * J_set / T)) / (1 + np.exp(-2 * J_set / T)))

T_conti = np.linspace(min(T_list),max(T_list),1000)
Magnet_sus_conti = Magnet_sus(T_conti)
Heat_cap_conti = Heat_cap(T_conti)
ener_conti = ener(T_conti)
#
#
## 创建子图
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
fig.tight_layout(pad=3.0)
#
# 绘制各个图表
axes[0, 0].scatter(T_list, Heat_cap_list)
axes[0, 0].plot(T_conti, Heat_cap_conti)
axes[0, 0].set_title('Heat Capacity')
axes[0, 0].set_xlabel('temp')
axes[0, 0].set_ylabel('Heat Capacity')

axes[0, 1].scatter(T_list, Magnet_sus_list)
#axes[0, 1].plot(T_conti, Magnet_sus_conti)
axes[0, 1].set_title('Magnetic Susceptibility')
axes[0, 1].set_xlabel('temp')
axes[0, 1].set_ylabel('Magnetic Susceptibility')

axes[1, 0].scatter(T_list, ave_ener_list)
axes[1, 0].plot(T_conti, ener_conti)
axes[1, 0].set_title('Average Energy')
axes[1, 0].set_xlabel('temp')
axes[1, 0].set_ylabel('Average Energy')


axes[1, 1].scatter(T_list, ave_mag_list)
axes[1, 1].set_title('Average Magnetization')
axes[1, 1].set_xlabel('temp')
axes[1, 1].set_ylabel('Average Magnetization')


##画散点图还是有连线的图
# plt.scatter(dataA, dataB , marker='o', color='b', label='Data Points')

#贴上标签
#plt.legend()

plt.savefig("img/figuretest.png")
plt.show()

print("T","Heat_cap","Magnet_sus","magnetization")
for i in range(len(T_list)):
    print(T_list[i], Heat_cap_list[i] , Magnet_sus_list[i],ave_mag_list[i])

