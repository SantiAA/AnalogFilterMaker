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
        self.application = [FilterTypes.HighPass.value, FilterTypes.LowPass.value, FilterTypes.BandPass.value, FilterTypes.BandReject.value]
        self.dict["Denorm."] = [(0, 100, False, int()), 0]
        self.dict["m"] = [(0, 100, False, int()), 50]
        approximations = ["Butterworth", "Cauer", "Chebyshev I", "Chebyshev II", "Legendre"]
        self.extra_combos.append(approximations)
        self.extra_combos.append(approximations)

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Transitional filters are not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter, **kwargs):
        self.approx1.calculate(filter_in_use, **kwargs)
        z1, p1, k1 = filter_in_use.get_z_p_k_q()
        self.approx2.calculate(filter_in_use, **kwargs)
        z2, p2, k2 = filter_in_use.get_z_p_k_q()
        p = p1**self.m * p2**(1-self.m)
        # z= tengo que ver como se calculan ceros
        z = z1 ** self.m * z2 ** (1 - self.m)
        # k= tengo que ver como se calcula la ganancia
        k = k1 ** self.m * k2 ** (1 - self.m)
        filter_in_use.load_z_p_k(z, p, k)
