# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import *


class GroupDelay(Filter):
    def __init__(self):
        super().__init__(FilterTypes.GroupDelay)
        """ Load BandReject requirements for future usage """
        self.requirements = {TemplateInfo.ft: None,   # frequency of tau=gd*tol
                             TemplateInfo.tol: None,  # tolerance
                             TemplateInfo.gd: None}   # Group delay

    def validate_requirements(self) -> bool:
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded

        return True     # si me pasan todos los requirements ya esta, porque ya estan acotados desde el front
