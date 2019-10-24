# python native modules
from enum import Enum

# third-party modules

# AFM project modules


class FilterTypes(Enum):
    LowPass = "Low Pass"
    HighPass = "High Pass"
    BandPass = "Band Pass"
    BandReject = "Notch"
    GroupDelay = "Group Delay"


class TemplateInfo(Enum):
    Ap = "Ap"
    Aa = "Aa"
    fo = "fo"
    fa = "fa"
    fp = "fp"
    fa_ = "fa+"
    fa__ = "fa-"
    fp_ = "fp+"
    fp__ = "fp-"
    gd = "Group delay"
    ft = "ft"
    tol = "Tolerance"


class Filter(object):

    def __init__(self, filter_type: FilterTypes):
        self.filter = filter_type
        self.requirements = {}
        self.zeros = []
        self.poles = []
        self.gain = None

    def get_type(self) -> FilterTypes:
        return self.filter

    def get_requirements(self):
        return [key for key in self.requirements]

    def load_requirements(self, specs):
        for each in specs:
            if each in self.requirements.keys():
                self.requirements[each] = specs[each]
            else:
                print("Key not found in requirements")
                return False
        if not self.validate_requirements():
            return False

    def validate_requirements(self) -> bool:
        pass

    def get_req_value(self, key: TemplateInfo):
        return self.requirements[key]

    def load_z_p_k(self, z, p, k):
        self.zeros = z
        self.poles = p
        self.gain = k
