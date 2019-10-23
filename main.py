from PyQt5 import QtWidgets


from FrontEnd.UIManager import UIManager

"""
dictionary = {"A": 0, "B": 1, "C": 2}
for key in dictionary:
    print(key, " : ", dictionary[key])

N, Wn = signal.cheb2ord(1, 10, 3, 40, analog=True)
b, a = signal.cheby2(2, 40, Wn, 'low', analog=True)
w, h = signal.freqs(b, a)
print("Normalizado: Numerador ", b, " denominador ", a)
N, Wn = signal.cheb2ord(10, 100, 3, 40, analog=True)
b, a = signal.cheby2(2, 40, Wn, 'low', analog=True)
w, h = signal.freqs(b, a)
print("Desnormalizado: Numerador ", b, " denominador ", a)
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title('Chebyshev Type II frequency response (rs=40)')
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

"""

def start():
    app = QtWidgets.QApplication([])
    uiMan = UIManager()
    uiMan.begin()
    app.exec()


if __name__ == "__main__":
    start()