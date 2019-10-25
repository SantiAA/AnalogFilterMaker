from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets
from FrontEnd.UIManager import UIManager



N, Wn = signal.buttord( [100, 5000], [500, 1000], 3, 40, analog=True)
print("N = ", N, " Frecuencias: ", Wn)
z, p, k = signal.butter(N, Wn, 'stop', analog=True, output='zpk')

#w, h = signal.lti(z, p, k).bode()
my = signal.ZerosPolesGain(z, p, k)
scnd_order = signal.zpk2sos(z, p, k)
print(z, p, k)
print("***********")
print(scnd_order)
w, h, p = my.bode(n=100000)

plt.semilogx(w, h)

plt.title('Butterworth frequency response (rs=40)')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(500, color='green')  # cutoff frequency
plt.axvline(1000, color='green')  # cutoff frequency
plt.axhline(-3, color='green')  # rs
plt.axvline(400, color='blue')  # cutoff frequency
plt.axvline(2000, color='blue')  # cutoff frequency
plt.axhline(-40, color='blue')  # rs
plt.show()

"""


def start():
    app = QtWidgets.QApplication([])
    uiMan = UIManager()
    uiMan.begin()
    app.exec()


if __name__ == "__main__":
    start()

"""