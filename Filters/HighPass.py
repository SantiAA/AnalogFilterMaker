# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import *


class HighPass(Filter):
    def __init__(self):
        super().__init__(FilterTypes.HighPass)
        """ Load HighPass requirements for future usage """
        self.requirements = {TemplateInfo.Aa.value: None,
                             TemplateInfo.Ap.value: None,
                             TemplateInfo.fa.value: None,
                             TemplateInfo.fp.value: None}

    def validate_requirements(self) -> bool:
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded

        if self.requirements[TemplateInfo.Ap.value] > self.requirements[TemplateInfo.Aa.value]:
            if self.requirements[TemplateInfo.fp.value] > self.requirements[TemplateInfo.fa.value]:
                return True

        """ If there is something wrong in the attenuations or frequencies I return False"""
        return False
