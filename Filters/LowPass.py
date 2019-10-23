# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import *


class LowPass(Filter):
    def __init__(self):
        super().__init__(FilterTypes.LowPass)
        """ Load LowPass requirements for future usage """
        self.requirements = {TemplateInfo.Aa: None,
                             TemplateInfo.Ap: None,
                             TemplateInfo.fa: None,
                             TemplateInfo.fp: None}

    def validate_requirements(self) -> bool:
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded

        if self.requirements[TemplateInfo.Aa] > self.requirements[TemplateInfo.Ap]:
            if self.requirements[TemplateInfo.fa] > self.requirements[TemplateInfo.fp]:
                return True

        """ If there is something wrong in the attenuations or frequencies I return False"""
        return False
