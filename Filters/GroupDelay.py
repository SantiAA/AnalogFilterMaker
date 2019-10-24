# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import *


class GroupDelay(Filter):
    def __init__(self):
        super().__init__(FilterTypes.GroupDelay)
        """ Load BandReject requirements for future usage """
        self.requirements = {TemplateInfo.ft: None,   # frequency of tau=gd*tol
                             TemplateInfo.fp: None,   # fp
                             TemplateInfo.tol: None,  # tol
                             TemplateInfo.gd: None}   # Group delay

    def validate_requirements(self) -> bool:
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded

        if self.requirements[TemplateInfo.ft] > 0:
            if self.requirements[TemplateInfo.fp] > 0:
                if self.requirements[TemplateInfo.gd] > 0:
                    if self.requirements[TemplateInfo.tol] > 0:
                        return True

        """ If there is something wrong in the specs I return False"""
        return False


