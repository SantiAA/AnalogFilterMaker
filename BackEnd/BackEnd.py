# python native modules

# third-party modules

# AFM project modules
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
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo

from BackEnd.Output.Dot import Dot, INFINITE
from BackEnd.Output.Square import Square

class BackEnd:
    def __init__(self):
        self.lp = LowPass
        self.all_filters = [LowPass(), HighPass(), BandPass(), BandReject(), GroupDelay()]
        self.all_approximations = [Bessel(), Butterworth(), ChevyI(), ChebyII(), Cauer(), Gauss(), Legendre()]
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
        my_filter = self._parse_filter(filter)
        if my_filter.validate_requirements():
            return True, ""
        else:
            return False, "BackEnd.py: I don't know the error yet, sorry"

    def get_template(self, filtro):
        my_filter = self._parse_filter(filtro)
        if my_filter.get_type() is FilterTypes.LowPass:
            req = my_filter.get_requirements()
            sq1 = Square(Dot(0, req[TemplateInfo.Ap]), Dot(0, INFINITE), Dot(req[TemplateInfo.fp], INFINITE)
                         , Dot(req[TemplateInfo.fp],  req[TemplateInfo.Ap]))
            sq2 = Square(Dot(req[TemplateInfo.fa], -INFINITE), Dot(req[TemplateInfo.fa],  req[TemplateInfo.Aa]),
                         Dot(INFINITE, req[TemplateInfo.Aa]), Dot(-INFINITE, -INFINITE))
            return [sq1, sq2]
        elif my_filter.get_type() is FilterTypes.HighPass:
            req = my_filter.get_requirements()
            sq1 = Square(Dot(0, -INFINITE), Dot(0, req[TemplateInfo.Aa]),
                         Dot(req[TemplateInfo.fa], req[TemplateInfo.Aa]), Dot(req[TemplateInfo.fa], -INFINITE))
            sq2 = Square(Dot(req[TemplateInfo.fp], req[TemplateInfo.Ap]), Dot(req[TemplateInfo.fp], INFINITE),
                         Dot(INFINITE, INFINITE), Dot(INFINITE, req[TemplateInfo.Aa]))
            return [sq1, sq2]
        elif my_filter.get_type() is FilterTypes.BandPass:
            req = my_filter.get_requirements()
            sq1 = Square(Dot(0, -INFINITE), Dot(0, req[TemplateInfo.Aa]),
                         Dot(req[TemplateInfo.fa__], req[TemplateInfo.Aa]), Dot(req[TemplateInfo.fa__], -INFINITE))
            sq2 = Square(Dot(req[TemplateInfo.fp__], req[TemplateInfo.Ap]), Dot(req[TemplateInfo.fp__], INFINITE),
                         Dot(req[TemplateInfo.fp_], INFINITE), Dot(req[TemplateInfo.fp_], req[TemplateInfo.Ap]))
            sq3 = Square(Dot(req[TemplateInfo.fa_], -INFINITE), Dot(req[TemplateInfo.fa_], req[TemplateInfo.Aa]),
                         Dot(INFINITE, req[TemplateInfo.Aa]), Dot(-INFINITE, -INFINITE))
            return [sq1, sq2, sq3]
        elif my_filter.get_type() is FilterTypes.BandReject:
            req = my_filter.get_requirements()
            sq1 = Square(Dot(0, req[TemplateInfo.Ap]), Dot(INFINITE, req[TemplateInfo.Ap]),
                         Dot(req[TemplateInfo.fp__], INFINITE), Dot(req[TemplateInfo.fp__], req[TemplateInfo.Ap]))
            sq2 = Square(Dot(req[TemplateInfo.fa__], -INFINITE), Dot(req[TemplateInfo.fa__], req[TemplateInfo.Aa]),
                         Dot(req[TemplateInfo.fa_], req[TemplateInfo.Aa]), Dot(req[TemplateInfo.fa_], -INFINITE))
            sq3 = Square(Dot(req[TemplateInfo.fp_], req[TemplateInfo.Ap]), Dot(req[TemplateInfo.fp_], INFINITE),
                         Dot(INFINITE, INFINITE), Dot(INFINITE, req[TemplateInfo.Ap]))
            return [sq1, sq2, sq3]

    def get_graphics(self, filtro, aproximacion):
        pass

    def _parse_filter(self, front_end_filter) -> Filter:
        """ Busco el tipo de filtro que esta seleccionado """
        filters = None
        for fil in self.all_filters:
            if fil.get_type() is front_end_filter[0]:
                """ Creo dinamicamente un filtro del tipo requerido """
                filters = fil.__new__(type(fil))
                filters.__init__()

        specs = {}
        for aspect in front_end_filter[1]:
            specs[aspect] = front_end_filter[1][1]
        filters.load_requirements(specs)
        return filters
