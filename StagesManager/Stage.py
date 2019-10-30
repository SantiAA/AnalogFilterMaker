from scipy.signal import ZerosPolesGain, TransferFunction

from numpy import pi, log10
from BackEnd.Output.plots import GraphValues
from StagesManager import Zero, Pole


class Stage:
    def __init__(self, z: Zero, p: Pole):
        self.k = 1
        self.z = z
        self.pole = p

    def get_tf_plot(self):
        transfer_function = ZerosPolesGain(complex(0, self.z.im), self.pole.p, self.k)
        w, h = transfer_function.freqresp(n=3000)
        f = w/(2*pi)
        mag = 20*log10(h)
        return GraphValues(f, mag, False, False, True)

    def get_tf_tex(self):
        zpk = ZerosPolesGain(complex(0, self.z.im), self.pole.p, self.k)
        transfer_function = zpk.to_tf()
        num = transfer_function.num
        den = transfer_function.den
        ret = "H(s)=\\frac{"
        i=0
        for i in range(len(num), 0):
            ret += "{0.2f}".format(num[i]) + "s^" + str(i)
        ret += "}{"
        for i in range(len(den), 0):
            ret += "{0.2f}".format(den[i]) + "s^" + str(i)
        ret += "}"
        return ret

    def get_dr(self, vi_min, vi_max):

        pass