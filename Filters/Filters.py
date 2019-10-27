# python native modules
from enum import Enum
from numpy import poly
from numpy import sqrt
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
        self.normalized = {"Order": None,
                           "Zeros": [],
                           "Poles": [],
                           "Gain": None}
        self.denormalized = {"Order": None,
                             "Zeros": [],
                             "Poles": [],
                             "Gain": None,
                             "MaxQ": None}
        self.limits = {TemplateInfo.Aa: (0, 1e9), TemplateInfo.Ap: (0, 1e9), TemplateInfo.fa: (0, 1e9),
                       TemplateInfo.fp: (0, 1e9), TemplateInfo.fp_: (0, 1e9), TemplateInfo.fp__: (0, 1e9),
                       TemplateInfo.fa_: (0, 1e9), TemplateInfo.fa__: (0, 1e9), TemplateInfo.fo: (0, 1e9),
                       TemplateInfo.ft: (0, 1e9), TemplateInfo.gd: (0, 1e9), TemplateInfo.tol: (0, 1)}

    def get_type(self) -> FilterTypes:
        return self.filter

    def get_requirements(self):
        return [key for key in self.requirements]

    def get_order(self):
        return self.normalized["Order"], self.denormalized["Order"]

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
        self.denormalized["Zeros"] = z
        self.denormalized["Poles"] = p
        self.denormalized["Gain"] = k
        self.denormalized["Order"] = len(z)
        max_q = 0
        p_pairs = self._agrup_poles(p)
        for p_i in p_pairs:
            if len(p_i) == 2:
                den = poly(p_i, True)     # busco coeficientes del denominador
                q = sqrt(den[2])/den[1]   # formula para Q en funcion de los coeficientes
                if q > max_q:
                    max_q = q
        self.denormalized["MaxQ"] = max_q

    def load_normalized_z_p_k(self, z, p, k):
        self.normalized["Zeros"] = z
        self.normalized["Poles"] = p
        self.normalized["Gain"] = k
        self.normalized["Order"] = len(z)

    def get_req_limit(self, key: TemplateInfo):
        return self.limits[key]

    @staticmethod
    def _agrup_poles(p):
        pairs = []
        p.sort(key=lambda x: x.real)  # ordeno por parte real creciente
        while len(p):
            len_in = len(pairs)
            for i in range(1, len(p)):
                if (abs(p[0].real - p[i].real) < 1e-10) and (abs(p[0].imag + p[i].imag) < 1e-10):
                    pairs.append([p[0], p[i]])
                    p.remove(p[i])
                    break
            if len_in == len(pairs):  # si no le encontre un conjugado
                pairs.append([p[0]])  # no lo tiene :(
            p.remove(p[0])
        return pairs
