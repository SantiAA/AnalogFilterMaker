from enum import Enum


class Approximations:
    def __init__(self, approximation_name, max_q, filter_order):
        self.approximation_name = approximation_name
        self.max_q = max_q
        self.filter_order = filter_order
        self.string = approximation_name + "; Filter Order: " + str(filter_order) + "; Max Q: " + str(max_q)

    def update_string(self):
        self.string = self.approximation_name + "; Filter Order: " + str(self.filter_order) + "; Max Q: " + str(
            self.max_q)


class ApproximationNames(Enum):
    Butterworth = 'Butterworth'
    Bessel = 'Bessel'
    Chebyshev = 'Chebyshev'
    Chebyshev_inverso = 'Inverse Chebyshev'
    Legendre = 'Legendre'
    Gauss = 'Gauss'
    Cauer = 'Cauer'
