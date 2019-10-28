# python native modules

# third-party modules
from scipy import signal
import numpy as np

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class Bessel(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Bessel")
        self.application = [FilterTypes.GroupDelay]

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Bessel is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)

        self.__selectivity__(filter_in_use.get_type())
        return True

    def calculate(self, filter_in_use: Filter, **kwargs):
        super().calculate(filter_in_use, **kwargs)
        z = []
        p = []
        k = 0
        """ First I calculate the Normalized LowPass, to get the useful w """
        normalized_n, useful_w = self._bessord(self.information[TemplateInfo.ft], self.information[TemplateInfo.tol],
                                               self.information[TemplateInfo.gd], self.n_max)
        if self.fixed_n > 0:
            normalized_n = self.fixed_n
        elif normalized_n > self.n_max:
            normalized_n = self.n_max

        while True:
            """ First search the order and the normalizer 'cut' frequency """
            z_norm, p_norm, k_norm = signal.bessel(normalized_n, useful_w, analog=True, output='zpk')
            if filter_in_use.get_type() is FilterTypes.GroupDelay:
                z, p, k = signal.bessel(normalized_n, useful_w/self.information[TemplateInfo.gd], 'low', True, 'zpk')
            else:
                print("Bessel.py: Invalid filter type passed to Bessel aproximation")
                return
            if self.q_max >= filter_in_use.get_max_q() or normalized_n == self.n_max or self.fixed_n > 0:
                break
            normalized_n = normalized_n + 1
        filter_in_use.load_normalized_z_p_k(z_norm, p_norm, k_norm)
        filter_in_use.load_z_p_k(z, p, k)

    def _bessord(self, frg, tol, tau, max_order):
        wrgn = 2*np.pi*frg*tau
        n = 0
        while True:  # do{}while() statement python style
            n = n+1
            z_n, p_n, k_n = signal.bessel(n, wrgn, 'low', True, 'zpk')
            w, h = signal.freqs_zpk(z_n, p_n, k_n)
            g_delay = -np.diff(np.unwrap(np.angle(h)))/np.diff(w)
            if g_delay >= (1-tol) or n is max_order:
                break
        return n, wrgn
