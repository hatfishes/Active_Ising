import numpy as np
import matplotlib.pyplot as plt


T = np.linspace(0,10,100)
y = T * T 

plt.plot(T,y)
plt.savefig("plot.png")
plt.show()