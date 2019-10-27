# python native modules

# third-party modules
from scipy import signal
import numpy as np

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class Butterwoth(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Butterwoth")
        self.application = [FilterTypes.HighPass, FilterTypes.LowPass, FilterTypes.BandPass, FilterTypes.BandReject]

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Butterworth is not valid for ", filter_in_use.get_type())
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

    def calculate(self, filter_in_use: Filter, n_max=20, denorm=0):
        """ Be careful this function doesn't care of Q !!! """
        """ Fist I calculate the Normalized LowPass """
        normalized_n, useful_w = signal.buttord(1, self.selectivity, self.information[TemplateInfo.Ap],
                                                self.information[TemplateInfo.Aa], analog=True)
        if normalized_n > n_max:
            normalized_n = n_max
        z_norm, p_norm, k_norm = signal.butter(normalized_n, useful_w, analog=True, output='zpk')
        filter_in_use.load_normalized_z_p_k(z_norm, p_norm, k_norm)
        """ Now check the desnomalization cte """
        w, h = signal.freqs_zpk(z_norm, p_norm, k_norm)
        h = 20*np.log10(abs(h))
        i = [abs(j + self.information[TemplateInfo.Aa]) for j in h]
        wa = w[i.index(min(i))]
        denorm_cte = (wa*(1-denorm/100)+denorm/(self.selectivity*100))
        z_norm = z_norm*denorm_cte
        p_norm = p_norm*denorm_cte
        k_norm = k_norm*(denorm_cte**(len(p_norm)-len(z_norm)))
        """" Next we transform the LowPass into the requested filter """

        if filter_in_use.get_type() is FilterTypes.LowPass:
            """ If the approximation support the filter I continue """
            """ And transform the normalized low pass to the desire one """
            z, p, k = signal.lp2lp_zpk(z_norm, p_norm, k_norm, self.information[TemplateInfo.fp])
            filter_in_use.load_z_p_k(z, p, k)

        elif filter_in_use.get_type() is FilterTypes.HighPass:
            z, p, k = signal.lp2hp_zpk(z_norm, p_norm, k_norm, self.information[TemplateInfo.fp])
            filter_in_use.load_z_p_k(z, p, k)

        elif filter_in_use.get_type() is FilterTypes.BandPass:
            Awp = self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__]
            w0 = np.sqrt(self.information[TemplateInfo.fp_] * self.information[TemplateInfo.fp__] )

            z, p, k = signal.lp2bp_zpk(z_norm, p_norm, k_norm, w0, Awp)  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)

        elif filter_in_use.get_type() is FilterTypes.BandReject:
            Awp = self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__]
            w0 = np.sqrt(self.information[TemplateInfo.fp_] * self.information[TemplateInfo.fp__])

            z, p, k = signal.lp2bs_zpk(z_norm, p_norm, k_norm, w0, Awp)  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)

