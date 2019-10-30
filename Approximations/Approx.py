"""
Approximation base class
"""

# python native modules
from math import *

# third-party modules
from scipy.signal import *

# AFM project modules
from Filters.Filters import Filter
from Filters.Filters import TemplateInfo
from Filters.Filters import FilterTypes


class Approximation(object):

    def __init__(self, name):
        """ Useful to add in the GUI """
        self.name = name  # The name of the approximation
        self.dict = {
            "Q max": [(0, 100, False, float()), 10],
            "Fixed N": [(0, 20, True, int()), 10],
        }
        self.extra_combos = []  # To change to 2 in 'Transicionales'
        self.application = []  # Approximation's filter type application

        """ Useful for internal working """
        self.poles = []
        self.zeros = []
        self.information = {}
        self.selectivity = None
        self.n_max = 20
        self.q_max = -1  # aca ira el q maximo pedido por el usuario
        self.denorm = 0
        self.fixed_n = -1

    def is_available(self, filter_: FilterTypes):
        if filter_ in self.application:
            return True
        else:
            return False

    def validate_input(self):
        """
        Check if the information loaded was ok
        """
        pass

    def get_filter(self):
        """
        return: signal.lti object
        """
        pass

    def load_information(self, filter_in_use: Filter):
        pass

    def calculate(self, filter_in_use: Filter, kwargs):
        self.n_max = 20
        self.denorm = 0
        self.q_max = -1
        self.fixed_n = -1
        switcher = {
            # "n_max": self._set_n_max,
            "Denorm.": self._set_denorm,
            "Q max": self._set_q_max,
            "Fixed N": self._set_fixed_n
        }
        for key, value in kwargs.items():
            fun = switcher.get(key, lambda: "Invalid argument")
            lam = lambda: 0
            if type(fun) != type(lam):
                fun(value)
            else:
                print(key + "is an invalid argument for calculate()")

    # def _set_n_max(self, n_max):
    #     if type(n_max) is int:
    #        if n_max <= 20:
    #            self.n_max = n_max
    #    else:
    #        print("Approx.py: Invalid n_max argument, it must be float")

    def _set_denorm(self, denorm):
        if type(denorm) is float or type(denorm) is int:
            if 0 <= denorm <= 100:
                self.denorm = denorm
        else:
            print("Approx.py: Invalid denorm argument, it must be float")

    def _set_q_max(self, q_max):
        if type(q_max) is float or type(q_max) is int:
            if q_max > 0:
                self.q_max = q_max
        else:
            print("Approx.py: Invalid q_max argument, it must be float")

    def _set_fixed_n(self, fixed_n):
        if type(fixed_n) is int and fixed_n > 0:
            self.fixed_n = fixed_n
        else:
            print("Approx.py: Invalid fixed_q argument, it mus be int")

    """ Search more useful functions to add """

    def __adjust_w__(self, band_or_stop: bool):
        f01 = sqrt(self.information[TemplateInfo.fa_.value]*self.information[TemplateInfo.fa__.value])
        f02 = sqrt(self.information[TemplateInfo.fp_.value]*self.information[TemplateInfo.fp__.value])
        if f01 is f02:
            return  # Is symmetric
        wp__ = f01**2/self.information[TemplateInfo.fp_.value]
        wp_ = f01 ** 2 / self.information[TemplateInfo.fp__.value]
        wa__ = f01**2/self.information[TemplateInfo.fa_.value]
        wa_ = f01 ** 2 / self.information[TemplateInfo.fa__.value]
        k1 = (self.information[TemplateInfo.fa_.value]-self.information[TemplateInfo.fa__.value]) / \
             (wp_-self.information[TemplateInfo.fp__.value])
        k2 = (self.information[TemplateInfo.fa_.value] - self.information[TemplateInfo.fa__.value]) / \
             (self.information[TemplateInfo.fp_.value] - wp__)
        k3 = (wa_ - self.information[TemplateInfo.fa__.value]) / \
             (self.information[TemplateInfo.fp_.value] - self.information[TemplateInfo.fp__.value])
        k4 = (self.information[TemplateInfo.fa_.value] - wa__) / \
             (self.information[TemplateInfo.fp_.value] - self.information[TemplateInfo.fp__.value])
        if band_or_stop:  # True bandPass, False bandReject
            n1, _ = buttord(1, k1, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])
            n2, _ = buttord(1, k2, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])
            n3, _ = buttord(1, k3, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])
            n4, _ = buttord(1, k4, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])
        else:
            n1, _ = buttord(1, 1/k1, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])
            n2, _ = buttord(1, 1/k2, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])
            n3, _ = buttord(1, 1/k3, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])
            n4, _ = buttord(1, 1/k4, self.information[TemplateInfo.Ap.value], self.information[TemplateInfo.Aa.value])

        if n1 <= n2 and n1 <= n3 and n1 <= n4:
            self.information[TemplateInfo.fp_.value] = wp_
        elif n2 <= n1 and n2 <= n3 and n2 <= n4:
            self.information[TemplateInfo.fp__.value] = wp__
        elif n3 <= n1 and n3 <= n2 and n3 <= n4:
            self.information[TemplateInfo.fa_.value] = wa_
        elif n4 <= n1 and n4 <= n2 and n4 <= n2:
            self.information[TemplateInfo.fa__.value] = wa__


