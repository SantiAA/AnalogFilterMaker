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
        self.application = []  # Approximation's filter type application

        """ Useful for internal working """
        self.poles = []
        self.zeros = []
        self.information = {}
        self.selectivity = None

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

    def calculate(self, filter_in_use: Filter, n_max=20, denorm=0):
        pass
    """ Search more useful functions to add """

    def __adjust_w__(self, band_or_stop: bool):
        f01 = sqrt(self.information[TemplateInfo.fa_]*self.information[TemplateInfo.fa__])
        f02 = sqrt(self.information[TemplateInfo.fp_]*self.information[TemplateInfo.fp__])
        if f01 is f02:
            return  # Is symmetric
        wp__ = f01**2/self.information[TemplateInfo.fp_]
        wp_ = f01 ** 2 / self.information[TemplateInfo.fp__]
        wa__ = f01**2/self.information[TemplateInfo.fa_]
        wa_ = f01 ** 2 / self.information[TemplateInfo.fa__]
        k1 = (self.information[TemplateInfo.fa_]-self.information[TemplateInfo.fa__]) / \
             (wp_-self.information[TemplateInfo.fp__])
        k2 = (self.information[TemplateInfo.fa_] - self.information[TemplateInfo.fa__]) / \
             (self.information[TemplateInfo.fp_] - wp__)
        k3 = (wa_ - self.information[TemplateInfo.fa__]) / \
             (self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__])
        k4 = (self.information[TemplateInfo.fa_] - wa__) / \
             (self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__])
        if band_or_stop:  # True bandPass, False bandReject
            n1, _ = buttord(1, k1, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])
            n2, _ = buttord(1, k2, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])
            n3, _ = buttord(1, k3, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])
            n4, _ = buttord(1, k4, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])
        else:
            n1, _ = buttord(1, 1/k1, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])
            n2, _ = buttord(1, 1/k2, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])
            n3, _ = buttord(1, 1/k3, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])
            n4, _ = buttord(1, 1/k4, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa])

        if n1 <= n2 and n1 <= n3 and n1 <= n4:
            self.information[TemplateInfo.fp_] = wp_
        elif n2 <= n1 and n2 <= n3 and n2 <= n4:
            self.information[TemplateInfo.fp__] = wp__
        elif n3 <= n1 and n3 <= n2 and n3 <= n4:
            self.information[TemplateInfo.fa_] = wa_
        elif n4 <= n1 and n4 <= n2 and n4 <= n2:
            self.information[TemplateInfo.fa__] = wa__

    def __selectivity__(self, filter_in_use: FilterTypes):
        if filter_in_use is FilterTypes.HighPass:
            self.selectivity = self.information[TemplateInfo.fa] / self.information[TemplateInfo.fp]  # K = wa/wp
        elif filter_in_use is FilterTypes.LowPass:
            self.selectivity = self.information[TemplateInfo.fp] / self.information[TemplateInfo.fa]  # K = wp/wa
        elif filter_in_use is FilterTypes.BandPass:
            self.selectivity = (self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__]) / \
                               (self.information[TemplateInfo.fa_] - self.information[TemplateInfo.fa__])  # K = Awa/ Awp
        elif filter_in_use is FilterTypes.BandReject:
            self.selectivity = (self.information[TemplateInfo.fa_] - self.information[TemplateInfo.fa__]) / \
                               (self.information[TemplateInfo.fp_] - self.information[TemplateInfo.fp__])  # K = Awp/ Awa

