# python native modules

# third-party modules
from numpy import where

# AFM project modules
from Filters.Filters import *


class HighPass(Filter):
    def __init__(self):
        super().__init__(FilterTypes.HighPass.value)
        """ Load HighPass requirements for future usage """
        self.requirements = {TemplateInfo.k.value: None,
                             TemplateInfo.Aa.value: None,
                             TemplateInfo.Ap.value: None,
                             TemplateInfo.fa.value: None,
                             TemplateInfo.fp.value: None}

        self.defaults = {
            TemplateInfo.Aa.value: 40, TemplateInfo.Ap.value: 5, TemplateInfo.fa.value: 2000,
            TemplateInfo.fp.value: 20000,
            TemplateInfo.k.value: 1
        }

    def validate_requirements(self) -> (bool, str):
        ret = ""
        for each in self.requirements:
            if self.requirements[each] is None:
                ret = "Please enter a value for " + each[:where(" [")]
                return False, ret  # Check if every spec was loaded

        if self.requirements[TemplateInfo.Aa.value] > self.requirements[TemplateInfo.Ap.value]:
            if self.requirements[TemplateInfo.fp.value] > self.requirements[TemplateInfo.fa.value]:
                self.selectivity = self.requirements[TemplateInfo.fa.value] / self.requirements[
                    TemplateInfo.fp.value]  # K = wa/wp
                return True, ret
            else:
                ret = "fp must be greater than fa"
        else:
            ret = "Aa must be greater than Ap"

        """ If there is something wrong in the attenuations or frequencies I return False"""
        return False, ret
