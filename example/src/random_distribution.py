import numpy as np
from matplotlib import pyplot as plt

<seeds>
<config>

# from configs, we now have the vars w and noise
w = np.array(w)
x = np.arange(0, 100, 1)
y = w*x + np.random.normal(0, noise, 100)

plt.plot(x, y)
plt.savefig('plot.png')