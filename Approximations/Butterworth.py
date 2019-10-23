"""
Approximation base class
"""

# python native modules

# third-party modules
from sympy import *

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo


class Butterwoth(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Butterwoth")
        self.application = [FilterTypes.HighPass, FilterTypes.LowPass, FilterTypes.BandPass, FilterTypes.BandReject]
        self.information = {}

    def load_information(self, filter_type, specs):

        if filter_type not in self.application:
            print("Something done wrong, this approximation is not valid for ", filter_type)
            return False

        if filter_type is FilterTypes.LowPass:
            try:
                self.information[TemplateInfo.Aa] = specs[TemplateInfo.Aa]
                self.information[TemplateInfo.Ap] = specs[TemplateInfo.Ap]
                self.information[TemplateInfo.fa] = specs[TemplateInfo.fa]
                self.information[TemplateInfo.fp] = specs[TemplateInfo.fp]
            except Exception:
                print("Not enough information or wrong loaded")
                return False

            pass
