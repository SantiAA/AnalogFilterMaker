# python native modules

# third-party modules
from scipy import signal
import numpy as np

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class ChebyII(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Cheby II")
        self.application = [FilterTypes.HighPass, FilterTypes.LowPass, FilterTypes.BandPass, FilterTypes.BandReject]
        self.information = {}
        self.dict = {
            "N max": [(0, 20, False), None],
            "Q max": [(0, 10, False), None],
            "Fixed N": [(0, 20, True), None],
            "Denorm.": [(0, 100, False), None]
        }

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Cheby II is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)

        if filter_in_use.get_type() is FilterTypes.BandReject:
            self.__adjust_w__(False)
        elif filter_in_use.get_type() is FilterTypes.BandPass:
            self.__adjust_w__(True)

        self.__selectivity__(filter_in_use.get_type())

        return True

    def calculate(self, filter_in_use: Filter, **kwargs):
        super().calculate(filter_in_use, **kwargs)
        z = []
        p = []
        k = 0
        """ First I calculate the Normalized LowPass, to get the useful w """
        normalized_n, useful_w = signal.cheb2ord(1, self.selectivity, self.information[TemplateInfo.Ap],
                                                 self.information[TemplateInfo.Aa], analog=True)
        if self.fixed_n > 0:
            normalized_n = self.fixed_n
        elif normalized_n > self.n_max:
            normalized_n = self.n_max

        while True:
            z_norm, p_norm, k_norm = signal.cheby2(normalized_n, useful_w, analog=True, output='zpk')

            """ Now check the desnomalization cte """
            w, h = signal.freqs_zpk(z_norm, p_norm, k_norm)
            h = 20 * np.log10(abs(h))
            i = [abs(j + self.information[TemplateInfo.Aa]) for j in h]
            wa = w[i.index(min(i))]
            denorm_cte = (wa * (1 - self.denorm / 100) + self.denorm / (self.selectivity * 100))
            _z = z_norm * denorm_cte
            _p = p_norm * denorm_cte
            _k = k_norm * (denorm_cte ** (len(p_norm) - len(z_norm)))
            """" Next we transform the LowPass into the requested filter """

            if filter_in_use.get_type() is FilterTypes.LowPass:
                """ And transform the normalized low pass to the desire one """
                z, p, k = signal.lp2lp_zpk(_z, _p, _k, self.information[TemplateInfo.fp])
                filter_in_use.load_z_p_k(z, p, k)

            elif filter_in_use.get_type() is FilterTypes.HighPass:
                z, p, k = signal.lp2hp_zpk(_z, _p, _k, self.information[TemplateInfo.fp])
                filter_in_use.load_z_p_k(z, p, k)

            elif filter_in_use.get_type() is FilterTypes.BandPass:
                Awp = self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__]
                w0 = np.sqrt(self.information[TemplateInfo.fp_] * self.information[TemplateInfo.fp__])

                z, p, k = signal.lp2bp_zpk(_z, _p, _k, w0, Awp)  # Desnormalizado
                filter_in_use.load_z_p_k(z, p, k)

            elif filter_in_use.get_type() is FilterTypes.BandReject:
                Awp = self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__]
                w0 = np.sqrt(self.information[TemplateInfo.fp_] * self.information[TemplateInfo.fp__])

                z, p, k = signal.lp2bs_zpk(_z, _p, _k, w0, Awp)  # Desnormalizado
                filter_in_use.load_z_p_k(z, p, k)

            else:
                print("Chevy2.py: Invalid filter type passed to Inverse Chebyshev aproximation")
                return
            if self.q_max >= filter_in_use.get_max_q() or normalized_n == self.n_max or self.fixed_n > 0:
                break
            normalized_n = normalized_n + 1
        filter_in_use.load_normalized_z_p_k(z_norm, p_norm, k_norm)
        filter_in_use.load_z_p_k(z, p, k)