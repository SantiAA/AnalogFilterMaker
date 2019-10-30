# python native modules

# third-party modules
from numpy import where

# AFM project modules
from Filters.Filters import *


class BandReject(Filter):
    def __init__(self):
        super().__init__(FilterTypes.BandReject.value)
        """ Load BandReject requirements for future usage """
        self.requirements = {TemplateInfo.k.value: None,
                             TemplateInfo.Aa.value: None,
                             TemplateInfo.Ap.value: None,
                             TemplateInfo.fa_.value: None,  # fa+
                             TemplateInfo.fa__.value: None,  # fa-
                             TemplateInfo.fp_.value: None,  # fp+
                             TemplateInfo.fp__.value: None}  # fp-
        self.defaults = {
            TemplateInfo.Aa.value: 40, TemplateInfo.Ap.value: 5,
            TemplateInfo.fp_.value: 45000, TemplateInfo.fp__.value: 2000, TemplateInfo.fa_.value: 30000,
            TemplateInfo.fa__.value: 3000,
            TemplateInfo.k.value: 1
        }

    def validate_requirements(self) -> (bool, str):
        ret = ""
        for each in self.requirements:
            if self.requirements[each] is None:
                ret = "Please enter a value for " + each[:where(" [")]
                return False, ret  # Check if every spec was loaded

        if self.requirements[TemplateInfo.Aa.value] > self.requirements[TemplateInfo.Ap.value]:
            if self.requirements[TemplateInfo.fp__.value] < self.requirements[TemplateInfo.fa__.value]:
                if self.requirements[TemplateInfo.fp_.value] > self.requirements[TemplateInfo.fa_.value]:
                    self.selectivity = (self.requirements[TemplateInfo.fa_.value] -
                                        self.requirements[TemplateInfo.fa__.value])/ \
                                       (self.requirements[TemplateInfo.fp_.value] -
                                        self.requirements[TemplateInfo.fp__.value])  # K = Awp/ Awa

                    return True, ret
                else:
                    ret = "fp+ must be greater than fa+"
            else:
                ret = "fa- must be greater than fp-"
        else:
            ret = "Aa must be greater than Ap"

        """ If there is something wrong in the attenuations or frequencies I return False"""
        return False, ret
