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

        self.__selectivity__()
        return True

    def calculate(self, filter_in_use: Filter, n_max=20, denorm=0):
        """ Be careful this function doesn't care of Q !!! """
        """ Fist I calculate the Normalized LowPass """
        normalized_n, useful_w = signal.buttord(1, self.selectivity, self.information[TemplateInfo.Ap],
                                                self.information[TemplateInfo.Aa], analog=True)
        if normalized_n > n_max:
            normalized_n = n_max
        z_norm, p_norm, k_norm = signal.butter(normalized_n, useful_w, analog=True, output='zpk')
        """ Now check the desnomalization cte """
        w, h = signal.freqs_zpk(z_norm, p_norm, k_norm)
        h = 20*np.log10(abs(h))
        i = [abs(j + self.information[TemplateInfo.Aa]) for j in h]
        wa = w[i.index(min(i))]
        denorm_cte = (wa*(1-denorm/100)+denorm/(self.selectivity*100))
        #Aca falta terminar
        filter_in_use.load_normalized_z_p_k(z_norm, p_norm, k_norm)
        """ Next we transform the LowPass into the requested filter """

        if filter_in_use.get_type() is FilterTypes.LowPass:
            """ If the approximation support the filter I continue """
            """ Then using buttlord I get the order and the frequency for the -3dB point"""
            n, w = signal.buttord(self.information[TemplateInfo.fp], self.information[TemplateInfo.fa],
                                  self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)
            """ Now we limit the order of the filter """
            if n > n_max:
                n = n_max
            """ After getting the order I get the zeros, poles and gain of the filter """
            z, p, k = signal.butter(n, w, analog=True, output='zpk')  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
            filter_in_use.load_order(n)

        elif filter_in_use.get_type() is FilterTypes.HighPass:
            n, w = signal.buttord(self.information[TemplateInfo.fp], self.information[TemplateInfo.fa],
                                  self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

            z, p, k = signal.butter(n, w, analog=True, output='zpk')  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
            filter_in_use.load_order(n)

        elif filter_in_use.get_type() is FilterTypes.BandPass:
            wp = [self.information[TemplateInfo.fp__], self.information[TemplateInfo.fp_]]
            wa = [self.information[TemplateInfo.fa__], self.information[TemplateInfo.fa_]]
            n, w = signal.buttord(wp, wa, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

            z, p, k = signal.butter(n, w, analog=True, output='zpk', btype="band")  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
            filter_in_use.load_order(n)

        elif filter_in_use.get_type() is FilterTypes.BandReject:
            wp = [self.information[TemplateInfo.fp__], self.information[TemplateInfo.fp_]]
            wa = [self.information[TemplateInfo.fa__], self.information[TemplateInfo.fa_]]
            n, w = signal.buttord(wp, wa, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

            z, p, k = signal.butter(n, w, analog=True, output='zpk', btype="stop")  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
            filter_in_use.load_order(n)

