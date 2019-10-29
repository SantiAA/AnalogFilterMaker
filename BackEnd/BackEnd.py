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
                useful_dict[request] = [fil.get_limit(request), fil.get_default(request)]
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
        if my_filter.get_type() is FilterTypes.LowPass.value:
            fa = my_filter.get_req_value(TemplateInfo.fa.value)
            fp = my_filter.get_req_value(TemplateInfo.fp.value)
            Ap = my_filter.get_req_value(TemplateInfo.Ap.value)
            Aa = my_filter.get_req_value(TemplateInfo.Aa.value)
            sq1 = Square(Dot(0, Aa), Dot(0, INFINITE), Dot(fp, INFINITE), Dot(fp,  Ap))
            sq2 = Square(Dot(fa, -INFINITE), Dot(fa,  Aa), Dot(INFINITE, Aa), Dot(-INFINITE, -INFINITE))
            return [sq1, sq2]
        elif my_filter.get_type() is FilterTypes.HighPass.value:
            fa = my_filter.get_req_value(TemplateInfo.fa.value)
            fp = my_filter.get_req_value(TemplateInfo.fp.value)
            Ap = my_filter.get_req_value(TemplateInfo.Ap.value)
            Aa = my_filter.get_req_value(TemplateInfo.Aa.value)
            req = my_filter.get_requirements()
            sq1 = Square(Dot(0, -INFINITE), Dot(0, Aa), Dot(fa, Aa), Dot(fa, -INFINITE))
            sq2 = Square(Dot(fp, Ap), Dot(fp, INFINITE), Dot(INFINITE, INFINITE), Dot(INFINITE, Aa))
            return [sq1, sq2]
        elif my_filter.get_type() is FilterTypes.BandPass.value:
            fa_ = my_filter.get_req_value(TemplateInfo.fa_.value)
            fp_ = my_filter.get_req_value(TemplateInfo.fp_.value)
            fa__ = my_filter.get_req_value(TemplateInfo.fa__.value)
            fp__ = my_filter.get_req_value(TemplateInfo.fp__.value)
            Ap = my_filter.get_req_value(TemplateInfo.Ap.value)
            Aa = my_filter.get_req_value(TemplateInfo.Aa.value)
            sq1 = Square(Dot(0, -INFINITE), Dot(0, Aa), Dot(fa__, Aa), Dot(fa__, -INFINITE))
            sq2 = Square(Dot(fp__, Ap), Dot(fp__, INFINITE), Dot(fp_, INFINITE), Dot(fp_, Ap))
            sq3 = Square(Dot(fa_, -INFINITE), Dot(fa_, Aa), Dot(INFINITE, Aa), Dot(-INFINITE, -INFINITE))
            return [sq1, sq2, sq3]
        elif my_filter.get_type() is FilterTypes.BandReject.value:
            fa_ = my_filter.get_req_value(TemplateInfo.fa_.value)
            fp_ = my_filter.get_req_value(TemplateInfo.fp_.value)
            fa__ = my_filter.get_req_value(TemplateInfo.fa__.value)
            fp__ = my_filter.get_req_value(TemplateInfo.fp__.value)
            Ap = my_filter.get_req_value(TemplateInfo.Ap.value)
            Aa = my_filter.get_req_value(TemplateInfo.Aa.value)
            sq1 = Square(Dot(0, Ap), Dot(0, INFINITE), Dot(fp__, INFINITE), Dot(fp__, Ap))
            sq2 = Square(Dot(fa__, -INFINITE), Dot(fa__, Aa), Dot(fa_, Aa), Dot(fa_, -INFINITE))
            sq3 = Square(Dot(fp_, Ap), Dot(fp_, INFINITE), Dot(INFINITE, INFINITE), Dot(INFINITE, Ap))
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
            specs[aspect] = front_end_filter[1][aspect]
        filters.load_requirements(specs)
        return filters
