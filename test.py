from sympy import symbols, Eq, solve 
from math import pi

import numpy as np
from matplotlib import pyplot as plt


m = float(input())
R = float(input())
p = 1.3
C = 0.47
A = (2*pi)*(R**2)
g = 9.8

v = (2*m*g/(p*C*A))**(1/2)

x = np.linspace(0,2,2000)

y = v*np.tanh(g*x/v)

print("종단속도는 ")
print(v)
print("입니다")

plt.plot(x, y, 'r-')

plt.xlabel('t')

plt.ylabel('V')

plt.grid('alpha = 200')

plt.title('Motion Of Falling Body With Air Resistance')

plt.show()