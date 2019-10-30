# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import *


class GroupDelay(Filter):
    def __init__(self):
        super().__init__(FilterTypes.GroupDelay.value)
        """ Load BandReject requirements for future usage """
        self.requirements = {TemplateInfo.k.value: None,
                             TemplateInfo.ft.value: None,   # frequency of tau=gd*tol
                             TemplateInfo.tol.value: None,  # tolerance
                             TemplateInfo.gd.value: None}   # Group delay

        self.defaults = {TemplateInfo.gd.value: 10e-3, TemplateInfo.tol.value: 0.2,  TemplateInfo.ft.value: 10000,
                         TemplateInfo.k.value: 1}

    def validate_requirements(self) -> bool:
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded

        return True     # si me pasan todos los requirements ya esta, porque ya estan acotados desde el front
