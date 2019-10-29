from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets
from FrontEnd.UIManager import UIManager
from enum import Enum

class hola(Enum):
    A = "A"
    B = "B"


my_dict = {hola.A: 1, hola.B: 2}
print(hola.A.value)

exit()


class A(object):
    def __init__(self):
        print("Hola soy A")
        self.a = 0

mi = A()
mi.a += 1
mi_2 = mi.__new__(type(mi))
mi_2.__init__()
print(mi)
print(mi_2)
exit()

N, Wn = signal.buttord( 1, 7, 2, 40, analog=True)
print("N = ", N, " Frecuencias: ", Wn)
#z, p, k = signal.buttap(N)
#my = signal.ZerosPolesGain(z, p, k)
#w, h, p = my.bode(1000)
z, p, k = signal.butter(N, Wn, 'low', analog=True, output='zpk')
my = signal.ZerosPolesGain(z, p, k)
w, h, p = my.bode(10000)

plt.semilogx(w, h)
plt.title('Butterworth frequency response (rs=40)')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(1, color='green')  # cutoff frequency
#plt.axvline(1000, color='green')  # cutoff frequency
plt.axhline(-2, color='green')  # rs
#plt.axvline(400, color='blue')  # cutoff frequency
plt.axvline(7, color='blue')  # cutoff frequency
plt.axhline(-40, color='blue')  # rs
plt.show()

