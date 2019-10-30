# python native modules

# third-party modules
from numpy import where

# AFM project modules
from Filters.Filters import *
from BackEnd.Output.Dot import Dot, INFINITE
from BackEnd.Output.Square import Square


class GroupDelay(Filter):
    def __init__(self):
        super().__init__(FilterTypes.GroupDelay.value)
        """ Load BandReject requirements for future usage """
        self.requirements = {TemplateInfo.k.value: None,
                             TemplateInfo.ft.value: None,   # frequency of tau=gd*tol
                             TemplateInfo.tol.value: None,  # tolerance
                             TemplateInfo.gd.value: None}   # Group delay

        self.defaults = {TemplateInfo.gd.value: 175, TemplateInfo.tol.value: 0.2,  TemplateInfo.ft.value: 1000,
                         TemplateInfo.k.value: 1}

    def validate_requirements(self) -> (bool, str):
        ret = ""
        for each in self.requirements:
            if self.requirements[each] is None:
                ret = "Please enter a value for " + each[:where(" [")]
                return False, ret  # Check if every spec was loaded

        return True, ret     # si me pasan todos los requirements ya esta, porque ya estan acotados desde el front

    def get_templates(self):
        tol = self.requirements[TemplateInfo.tol.value]
        max_gd = self.requirements[TemplateInfo.gd.value]*(1-tol)
        freq = self.requirements[TemplateInfo.ft.value]
        sq1 = Square(Dot(0, -INFINITE), Dot(0, max_gd), Dot(freq, max_gd), Dot(freq, -INFINITE))
        sq1_n = Square(Dot(0, -INFINITE), Dot(0, 1-tol), Dot(freq*max_gd, 1-tol), Dot(freq, -INFINITE))
        return {GraphTypes.GroupDelay.value: sq1,
                GraphTypes.NormalizedGd.value: sq1_n}