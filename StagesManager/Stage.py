from scipy.signal import ZerosPolesGain

from BackEnd.Output.plots import GraphValues
from StagesManager import Zero, Pole


class Stage:
    def __init__(self, i, z: Zero, p: Pole):
        self.k = 1
        self.z = z
        self.p = p
        self.transfer_function = ZerosPolesGain(complex(0, z.im))

    def get_tf_plot(self):
        w, h = transfer_function
        graphs[GraphTypes.Module.value] = [[GraphValues(f, mag, False, False, True)],
                                           ["Frequency [Hz]", "Amplitude [dB]"]]
        return GraphValues([    ])


    def get_tf_tex(self):
        pass

    def get_dr(self, vi_min, vi_max):
        pass