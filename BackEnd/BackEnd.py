from Approximations.Butterworth import Butterworth
from Approximations.Chevy1 import ChevyI
from Approximations.Chevy2 import ChebyII
from Approximations.Cauer import Cauer
from Approximations.Bessel import Bessel
from Approximations.Gauss import Gauss
from Approximations.Legendre import Legendre

from Filters.Filters import Filter
from Filters.LowPass import LowPass
from Filters.HighPass import HighPass
from Filters.BandPass import BandPass
from Filters.BandReject import BandReject
from Filters.GroupDelay import GroupDelay


class BackEnd:
    def __init__(self):
        self.lp = LowPass
        self.all_filters = [LowPass(), HighPass(), BandPass(), BandReject(), GroupDelay()]
        self.all_approximations = [Bessel(), Butterworth(), ChevyI(), ChebyII(), Cauer(), Gauss(), Legendre()]
        self.fil_dict = {}
        for fil in self.all_filters:
            self.fil_dict[fil.get_type()] = {  for req in fil.get_requirements()}

    """ Returns """
    def get_util(self):
        pass

    def validate_filter(self, filter: Filter) -> (bool, str):
        pass

    def get_template(self, filter):
        pass

    def get_graphics(self):
        pass