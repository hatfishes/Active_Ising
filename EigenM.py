import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
#系综矩阵

#M= np.array([[1,1,1],[1,1,1],[1,1,1]])
#matrix = np.ones((20, 10000))


def readfile(file_path):#读取文件，返回系综矩阵
    # 从文件中读取数据
    data = pd.read_csv(file_path , delim_whitespace=True)
    #data.columns = ['步骤', '能量', '磁矩', 'acc', 'J', 'config']

    # 去除不必要的字符并转换为整数
    data["config"] = data["config"].str.replace('[&]', '', regex=True)
    data["config"] = data["config"].apply(lambda x: [1 if spin == '+' else -1 for spin in x])


    # 提取"config"列作为整数列表
    config_list = data["config"].tolist()   
    mean_config = np.mean(config_list, axis=0)
    #sub_config = config_list - mean_config
    sub_config = config_list

    print("sub0",config_list[0])
    print("sub1",config_list[1])   

    print("mean value",mean_config)

    print("sub0",sub_config[0])
    print("sub1",sub_config[1])    

    Matrix = np.array(sub_config).T # 转置以使得行表示时间序列，列表示自旋方向
    num_rows, num_cols = Matrix.shape
    C0 = np.sqrt(num_rows* num_cols)
    A_ = Matrix /C0
    return A_  



def drawSpace(U):#这个函数用来画

    # 创建包含三个子图的图形
    fig, axs = plt.subplots(3, 1, figsize=(15, 10), sharey=True)

    UT = np.transpose(U)

    # 遍历每个子图，绘制
    for ax, y_data, title in zip(axs, [UT[0], UT[1], UT[2]], ['EM1', 'EM2', 'EM3']):

        ax.plot(y_data)
        ax.set_title(title)

    # 设置整体标题
    fig.suptitle('Largest Eigen Microstates')

    # 显示图形
    plt.savefig("Output/Space")


def drawEigen(S):#这个函数画生成本征值
    plt.scatter(range(len(S)),S *S)
    plt.plot(S *S)
    plt.savefig("Output/EigenValue")

def drawTime(Vt):    
    # 创建颜色映射
    cmap = plt.cm.viridis

    # 创建包含三个子图的图形
    fig, axs = plt.subplots(3, 1, figsize=(15, 10), sharey=True)

    # 遍历每个子图，绘制Vt
    for ax, y_data, title in zip(axs, [Vt[0], Vt[1], Vt[2]], ['EM1', 'EM2', 'EM3']):

        ax.plot(y_data)
        ax.set_title(title)

    # 设置整体标题
    fig.suptitle('Evolution of Largest Eigen Microstates')

    # 显示图形
    plt.savefig("Output/Evolution")

temp = sys.argv[1]
#file = "data/1.46552"
file = "data/"+temp
N = 400
N_sqr= np.sqrt(N)
A = readfile(file)
U, S, Vt = np.linalg.svd(A, full_matrices=False) #奇异值分解

U_ = U *N_sqr
S_ = S /np.sqrt( sum(S*S))
Vt_ = Vt * N_sqr
drawEigen(S_)

drawSpace(U_)

drawTime(Vt_)




print(sum(S*S))
print(S[0],S_[0])
print("分解完成:",file)