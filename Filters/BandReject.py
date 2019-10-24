# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import *


class BandReject(Filter):
    def __init__(self):
        super().__init__(FilterTypes.BandReject)
        """ Load BandReject requirements for future usage """
        self.requirements = {TemplateInfo.Aa: None,
                             TemplateInfo.Ap: None,
                             TemplateInfo.fa_: None,  # fa+
                             TemplateInfo.fa__: None,  # fa-
                             TemplateInfo.fp_: None,  # fp+
                             TemplateInfo.fp__: None}  # fp-

    def validate_requirements(self) -> bool:
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded

        if self.requirements[TemplateInfo.Aa] > self.requirements[TemplateInfo.Ap]:
            if self.requirements[TemplateInfo.fp__] > self.requirements[TemplateInfo.fa__]:
                if self.requirements[TemplateInfo.fa_] > self.requirements[TemplateInfo.fp_]:
                    return True

        """ If there is something wrong in the attenuations or frequencies I return False"""
        return False
