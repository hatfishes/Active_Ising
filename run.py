import os
import subprocess as sp 
import numpy as np
import re 


#扫描的范围
T_ = []
l1 = np.linspace(0.5,1.1,10)
l2 = np.linspace(0.5,1.5,10)
l3 = np.linspace(1.042,1.047,10)
l4 = np.linspace(0.95,1.05,10)
T_ = np.sort(np.concatenate((l1, l2)))

T_ = l1

print(T_)
#print(T_[10])
#创建命令队列
processes = []
for T in T_:
    p = sp.Popen(["./active_1D",str(T)])
    processes.append(p)
#并行执行命令
cout = 0
for p in processes:
    cout += 1
    print(cout)
    p.wait()


print("mission completed")


