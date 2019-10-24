from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

"""
dictionary = {"A": 0, "B": 1, "C": 2}
for key in dictionary:
    print(key, " : ", dictionary[key])
"""
N, Wn = signal.buttord(10, 100, 3, 40, analog=True)
z, p, k = signal.butter(N, Wn, 'low', analog=True, output='zpk')
w, h = signal.freqs_zpk(z, p, k)
h = 20 * np.log10(abs(h))

i = [abs(j+40) for j in h]
wa = w[i.index(min(i))]

plt.semilogx(w, h)
denorm = (wa*(1-0.5)+100*0.5)/wa
z = z * denorm
p = p*denorm
k = k*((denorm)**(len(p)-len(z)))
w, h = signal.freqs_zpk(z, p, k)
h = 20 * np.log10(abs(h))
plt.semilogx(w, h)

plt.title('Butterworth frequency response (rs=40)')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(100, color='green')  # cutoff frequency
plt.axhline(-40, color='green')  # rs
plt.axvline(10, color='blue')  # cutoff frequency
plt.axhline(-3, color='blue')  # rs
plt.axis([1, 500, -80, 3])
plt.show()

z, p, k = signal.buttap(N)
w, h = signal.freqs_zpk(z, p, k)

plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title('Butterworth frequency response (rs=40)')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(10, color='green')  # cutoff frequency
plt.axhline(-40, color='green')  # rs
plt.axvline(1, color='blue')  # cutoff frequency
plt.axhline(-3, color='blue')  # rs
plt.show()
