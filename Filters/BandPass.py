# python native modules

# third-party modules
from numpy import where

# AFM project modules
from Filters.Filters import *
from BackEnd.Output.Dot import Dot, INFINITE
from BackEnd.Output.Square import Square


class BandPass(Filter):
    def __init__(self):
        super().__init__(FilterTypes.BandPass.value)
        """ Load BandPass requirements for future usage """
        self.requirements = {TemplateInfo.k.value: None,
                             TemplateInfo.Aa.value: None,
                             TemplateInfo.Ap.value: None,
                             TemplateInfo.fa_.value: None,  # fa+
                             TemplateInfo.fa__.value: None,  # fa-
                             TemplateInfo.fp_.value: None,  # fp+
                             TemplateInfo.fp__.value: None}  # fp-
        self.defaults = {
            TemplateInfo.Aa.value: 40, TemplateInfo.Ap.value: 5,
            TemplateInfo.fp_.value: 30000, TemplateInfo.fp__.value: 3000, TemplateInfo.fa_.value: 45000,
            TemplateInfo.fa__.value: 2000,
            TemplateInfo.k.value: 1
        }

    def validate_requirements(self) -> (bool, str):
        ret = ""
        for each in self.requirements:
            if self.requirements[each] is None:
                ret = "Please enter a value for " + each[:where(" [")]
                return False, ret  # Check if every spec was loaded

        if self.requirements[TemplateInfo.Aa.value] > self.requirements[TemplateInfo.Ap.value]:
            if self.requirements[TemplateInfo.fp__.value] > self.requirements[TemplateInfo.fa__.value]:
                if self.requirements[TemplateInfo.fa_.value] > self.requirements[TemplateInfo.fp_.value]:
                    self.selectivity = (self.requirements[TemplateInfo.fp_.value] -
                                        self.requirements[TemplateInfo.fp__.value]) / \
                                       (self.requirements[TemplateInfo.fa_.value] -
                                        self.requirements[TemplateInfo.fa__.value])  # K = Awa/ Awp

                    return True, ret
                else:
                    ret = "fa+ must me greater than fp+"
            else:
                ret = "fp- must be greater than fa-"
        else:
            ret = "Aa must be greater than Ap"

        """ If there is something wrong in the attenuations or frequencies I return False"""
        return False, ret

    def get_templates(self):
        fa = self.requirements[TemplateInfo.fa.value]
        fp = self.requirements[TemplateInfo.fp.value]
        Ap = self.requirements[TemplateInfo.Ap.value]
        Aa = self.requirements[TemplateInfo.Aa.value]
        sq1 = Square(Dot(0, Ap), Dot(0, INFINITE), Dot(fp, INFINITE), Dot(fp, Ap))
        sq2 = Square(Dot(fa, -INFINITE), Dot(fa, Aa), Dot(INFINITE, Aa), Dot(INFINITE, -INFINITE))

        sq1_n = Square(Dot(0, Ap), Dot(0, INFINITE), Dot(1, INFINITE), Dot(1, Ap))
        sq2_n = Square(Dot(self, -INFINITE), Dot(fa, Aa), Dot(INFINITE, Aa), Dot(INFINITE, -INFINITE))

        return [sq1, sq2], [sq1_n, sq2_n]
