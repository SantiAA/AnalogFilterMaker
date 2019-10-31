from scipy.signal import ZerosPolesGain, TransferFunction

from numpy import pi, log10, conjugate
from BackEnd.Output.plots import GraphValues
from StagesManager import Zero, Pole


class Stage:
    def __init__(self, z: Zero, p: Pole, k):
        self.k = k
        self.z = z
        self.pole = p

    def get_tf_plot(self):
        z = complex(0, self.z.im) if self.z is not None else []
        k_correct = abs(self.pole.p)**2*self.k
        transfer_function = ZerosPolesGain(z, self.pole.p, k_correct)
        w, h = transfer_function.freqresp(n=3000)
        f = w/(2*pi)
        mag = 20*log10(h)
        return GraphValues(f, mag, False, False, True)

    def get_tf_tex(self):
        z = complex(0, self.z.im) if self.z is not None else []
        p = [self.pole.p, conjugate(self.pole.p)] if self.pole.q > 0 else self.pole.p
        zpk = ZerosPolesGain(z, p, self.k)
        transfer_function = zpk.to_tf()
        num = transfer_function.num
        den = transfer_function.den
        ret = "$H(s)=\\frac{"
        i=0
        for i in range(len(num)-1, 0-1, -1):
            if abs(num[i]) > 0:
                if i < len(num) - 1:
                    ret += '+'
                ret += f'{num[i]:.2}'
                if i > 0:
                    ret += f's'
                if i > 1:
                    ret += f'^{i}'
        ret += "}{"
        for i in range(len(den)-1, 0-1, -1):
            if abs(den[i]) > 0:
                if i < len(den) - 1:
                    ret += '+'
                ret += f'{den[i]:.2}'
                if i > 0:
                    ret += f's'
                if i > 1:
                    ret += f'^{i}'
        ret += "}$\n\n"
        ord = 2 if self.pole.q > 0 else 1
        ret += f'Q={self.pole.q:.2}    n={ord}'
        return ret

    def set_gain(self, k):
        self.k = k
