# python native modules

# third-party modules
from scipy import signal
import numpy as np

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class Transitional(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Transitional")
        self.application = [FilterTypes.HighPass, FilterTypes.LowPass, FilterTypes.BandPass, FilterTypes.BandReject]
        self.approximations = ["Butterworth", "Cauer", "Chevy1", "Chevy2", "Legendre"]
        self.dict = {
            "N max": [(0, 20, False), None],
            "Q max": [(0, 10, False), None],
            "Fixed N": [(0, 20, True), None],
            "Denorm.": [(0, 100, False), None]
        }
        self.extra_combos = 2

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Transitional filters are not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter, n_max=20, denorm=0):
        self.approx1.calculate(filter_in_use, n_max, denorm)
        z1, p1, k1 = filter_in_use.get_z_p_k()
        self.approx2.calculate(filter_in_use, n_max, denorm)
        z2, p2, k2 = filter_in_use.get_z_p_k()
        p = p1**self.m * p2**(1-self.m)
        # z= tengo que ver como se calculan polos y ceros
        # k= tengo que ver como se calcula la ganancia
        filter_in_use.load_z_p_k(z, p, k)