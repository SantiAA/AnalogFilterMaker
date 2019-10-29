from Approximations.Butterworth import Butterwoth
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
        self.all_approximations = [Bessel(), Butterwoth(), ChevyI(), ChebyII(), Cauer(), Gauss(), Legendre()]
        self.dynamic_filters = []
        self.fil_dict = {}
        self.filters_specs = {}
        for fil in self.all_filters:
            approximations = []
            for approx in self.all_approximations:
                if approx.is_available(fil.get_type()):
                    approximations.append(approx)
            self.fil_dict[fil.get_type()] = approximations
            specs = fil.get_requirements()
            useful_dict = {}
            for request in specs:
                useful_dict[request] = [fil.get_limit(request), None]
            self.filters_specs[fil.get_type()] = useful_dict
    """ Returns """

    def get_util(self):
        return self.filters_specs, self.fil_dict

    def validate_filter(self, filter) -> (bool, str):  # Recibo [FilterType, data] VER
        """ Busco el tipo de filtro que esta seleccionado """
        for fil in self.all_filters:
            if fil.get_type() is filter[0]:
                """ Creo dinamicamente un filtro del tipo requerido """
                filters = fil.__new__(type(fil))
                filters.__init__()
                self.dynamic_filters.append(filters)
        specs = {}
        for aspect in filter[1]:
            specs[aspect] = filter[1][1]
        filters.load_requirements(specs)
        if filters.validate_requirements():
            return True, ""
        else:
            return False, "BackEnd.py: I don't know the error yet, sorry"

    def get_template(self, filter):
        pass

    def get_graphics(self):
        pass