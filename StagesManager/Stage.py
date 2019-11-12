from scipy.signal import ZerosPolesGain, TransferFunction

from numpy import pi, log10, conjugate, imag, amax
from BackEnd.Output.plots import GraphValues
from StagesManager import Zero, Pole


class Stage:
    def __init__(self, z: Zero, p: Pole, k):
        self.z = z
        self.pole = p
        if self.z is not None:
            if self.z.im:
                k_correct = abs(self.pole.p) ** 2 * k/(abs(self.z.im)**self.z.n) if self.pole.q > 0 else abs(self.pole.p) * k/(abs(self.z.im)**self.z.n)
            else:
                k_correct = k
        else:
            k_correct = abs(self.pole.p) ** 2 * k if self.pole.q > 0 else abs(self.pole.p) * k
        self.gain = k_correct
        self.k = k
        if self.z is not None:
            z = [complex(0, self.z.im), complex(0, -self.z.im)] if self.z.n == 2 else [complex(0, 0)]
        else:
            z = []
        p = [self.pole.p, conjugate(self.pole.p)] if self.pole.q > 0 else [self.pole.p]
        transfer_function = ZerosPolesGain(z, p, self.gain)
        w, h = transfer_function.freqresp(n=3000)
        mag = abs(h)
        self.max = amax(mag)

    def get_tf_plot(self, i):
        if self.z is not None:
            z = [complex(0, self.z.im), complex(0, -self.z.im)] if self.z.n == 2 else [complex(0, 0)]
        else:
            z = []
        # if self.z is not None:
        #     if self.z.im:
        #         k_correct = abs(self.pole.p) ** 2 * self.k/(abs(self.z.im)**self.z.n) if self.pole.q > 0 else abs(self.pole.p) * self.k/(abs(self.z.im)**self.z.n)
        #     else:
        #         k_correct = self.k
        # else:
        #     k_correct = abs(self.pole.p) ** 2 * self.k if self.pole.q > 0 else abs(self.pole.p) * self.k
        p = [self.pole.p, conjugate(self.pole.p)] if self.pole.q > 0 else [self.pole.p]
        #transfer_function = ZerosPolesGain(z, p, k_correct)
        transfer_function = ZerosPolesGain(z, p, self.gain)
        w, h = transfer_function.freqresp(n=3000)
        f = w/(2*pi)
        mag = 20*log10(h)
        return GraphValues(f, mag, False, False, True, f'Stage {i + 1}')

    def get_tf_tex(self):
        if self.z is not None:
            z = [complex(0, self.z.im), complex(0, -self.z.im)] if self.z.n == 2 else [complex(0, 0)]
        else:
            z = []
        p = [self.pole.p, conjugate(self.pole.p)] if self.pole.q > 0 else self.pole.p
        # if self.z is not None:
        #     if self.z.im:
        #         k_correct = abs(self.pole.p) ** 2 * self.k/(abs(self.z.im)**self.z.n) if self.pole.q > 0 else abs(self.pole.p) * self.k/(abs(self.z.im)**self.z.n)
        #     else:
        #         k_correct = self.k
        # else:
        #     k_correct = abs(self.pole.p) ** 2 * self.k if self.pole.q > 0 else abs(self.pole.p) * self.k
        #zpk = ZerosPolesGain(z, p, k_correct)
        zpk = ZerosPolesGain(z, p, self.gain)
        transfer_function = zpk.to_tf()
        num = transfer_function.num
        den = transfer_function.den
        ret = "$H(s)=\\frac{"
        i=0
        for i in range(len(num)):
            if abs(num[i]) > 0:
                ret += f'{num[i]:.1f}'
                if i < len(num) - 1:
                    ret += f's'
                if i < len(num) - 2:
                    ret += f'^{len(num)-i-1}'
                if i < len(num)-1:
                    ret += '+'
        ret += "}{"
        for i in range(len(den)):
            if abs(den[i]) > 0:
                ret += f'{den[i]:.1f}'
                if i < len(den) - 1:
                    ret += f's'
                if i < len(den) - 2:
                    ret += f'^{len(den)-i-1}'
                if i < len(den)-1:
                    ret += '+'
        ret += "}$\n\n"
        ord = 2 if self.pole.q > 0 else 1
        ret += f'Q={self.pole.q:.2}    n={ord}' if ord == 2 else f'n={ord}'
        return ret

    def set_gain(self, k):
        if self.z is not None:
            if self.z.im:
                k_correct = abs(self.pole.p) ** 2 * k / (abs(self.z.im) ** self.z.n) if self.pole.q > 0 else abs(
                    self.pole.p) * k / (abs(self.z.im) ** self.z.n)
            else:
                k_correct = k
        else:
            k_correct = abs(self.pole.p) ** 2 * k if self.pole.q > 0 else abs(self.pole.p) * k
        self.gain = k_correct
        self.k = k
        if self.z is not None:
            z = [complex(0, self.z.im), complex(0, -self.z.im)] if self.z.n == 2 else [complex(0, 0)]
        else:
            z = []
        p = [self.pole.p, conjugate(self.pole.p)] if self.pole.q > 0 else [self.pole.p]
        transfer_function = ZerosPolesGain(z, p, self.gain)
        w, h = transfer_function.freqresp(n=3000)
        mag = abs(h)
        self.max = amax(mag)
