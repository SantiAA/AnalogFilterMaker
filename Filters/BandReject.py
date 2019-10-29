# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import *


class BandReject(Filter):
    def __init__(self):
        super().__init__(FilterTypes.BandReject.value)
        """ Load BandReject requirements for future usage """
        self.requirements = {TemplateInfo.Aa.value: None,
                             TemplateInfo.Ap.value: None,
                             TemplateInfo.fa_.value: None,  # fa+
                             TemplateInfo.fa__.value: None,  # fa-
                             TemplateInfo.fp_.value: None,  # fp+
                             TemplateInfo.fp__.value: None}  # fp-

    def validate_requirements(self) -> bool:
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded

        if self.requirements[TemplateInfo.Aa.value] > self.requirements[TemplateInfo.Ap.value]:
            if self.requirements[TemplateInfo.fp__.value] > self.requirements[TemplateInfo.fa__.value]:
                if self.requirements[TemplateInfo.fa_.value] > self.requirements[TemplateInfo.fp_.value]:
                    return True

        """ If there is something wrong in the attenuations or frequencies I return False"""
        return False
