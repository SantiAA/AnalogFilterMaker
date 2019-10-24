"""
Approximation base class
"""

# python native modules

# third-party modules
from scipy import signal

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class ChevyI(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Chevy I")
        self.application = [FilterTypes.HighPass, FilterTypes.LowPass, FilterTypes.BandPass, FilterTypes.BandReject]
        self.information = {}

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Chevy I is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter):
        if filter_in_use.get_type() is FilterTypes.LowPass:
            """ If the approximation support the filter I continue """
            """ Then using buttlord I get the order and the frequency for the -3dB point"""
            n, w = signal.cheb1ord(self.information[TemplateInfo.fp], self.information[TemplateInfo.fa],
                                  self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)
            """ After getting the order I get the zeros, poles and gain of the filter """
            z, p, k = signal.butter(n, w, analog=True, output='zpk')  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
