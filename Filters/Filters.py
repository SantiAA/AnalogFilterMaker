# python native modules
from enum import Enum
from numpy import poly
from numpy import sqrt
from numpy import conj
from numpy import amax
from numpy import unwrap
from numpy import diff
from numpy import pi
from scipy import signal
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
    k = "Gain"


class GraphTypes(Enum):
    Norm_Attenuation = "Normalized attenuation"
    Attenuation = "Attenuation"
    Phase = "Phase"
    PolesZeros = "Zeros and Poles"
    Step = "Step response"
    Impulse = "Impulse response"
    GroupDelay = "Group delay"
    StagesQ = "Q"


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
                             "StagesQ": None,
                             "MaxQ": None}
        self.limits = {TemplateInfo.Aa: (0, 1e9), TemplateInfo.Ap: (0, 1e9), TemplateInfo.fa: (0, 1e9),
                       TemplateInfo.fp: (0, 1e9), TemplateInfo.fp_: (0, 1e9), TemplateInfo.fp__: (0, 1e9),
                       TemplateInfo.fa_: (0, 1e9), TemplateInfo.fa__: (0, 1e9), TemplateInfo.fo: (0, 1e9),
                       TemplateInfo.ft: (0, 1e9), TemplateInfo.gd: (0, 1e9), TemplateInfo.tol: (0, 1), TemplateInfo.k: (0, 1e9)}

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

    def get_max_q(self):
        return self.denormalized["MaxQ"]

    def load_z_p_k(self, z, p, k):
        self.denormalized["Zeros"] = z
        self.denormalized["Gain"] = k
        self.denormalized["Order"] = len(p)
        max_q = 0
        p = self._agrup_roots(p)     #ordena por parte real creciente y se asegura que los complejos conjugados tengan el mismo valor
        self.denormalized["Poles"] = p
        pairs = []
        while len(p):                 # agrupo en polos complejos conjugados
            len_in = len(pairs)
            for i in range(1, len(p)):
                if p[0] ==  p[i].conjugate():
                    pairs.append(p[0])
                    p.remove(p[i])
                    break
            if len_in == len(pairs):  # si no le encontre un conjugado
                pairs.append([p[0]])  # no lo tiene :(
            p.remove(p[0])

        for p_i in pairs:
            if len(p_i) == 2:
                den = poly(p_i, True)     # busco coeficientes del denominador
                q = sqrt(den[2])/den[1]   # formula para Q en funcion de los coeficientes
                self.denormalized["StagesQ"].append(q)
            else:
                self.denormalized["StagesQ"].append(-1)
        self.denormalized["MaxQ"] = amax(self.denormalized["StagesQ"])

    def load_normalized_z_p_k(self, z, p, k):
        self.normalized["Zeros"] = z
        self.normalized["Poles"] = p
        self.normalized["Gain"] = k
        self.normalized["Order"] = len(p)

    def get_req_limit(self, key: TemplateInfo):
        return self.limits[key]

    def get_all_graphs(self):
        graphs = {}
        trans_func = signal.ZerosPolesGain(self.denormalized["Zeros"], self.denormalized["Poles"], self.denormalized["Gain"])
        norm_trans_func = signal.ZerosPolesGain(self.normalized["Zeros"], self.normalized["Poles"], self.normalized["Gain"])
        w, mag, phase = trans_func.bode(n=1500)
        f = w/(2*pi)
        w_n, mag_n, phase_n = norm_trans_func.bode(n=1500)
        f_n = w_n/(2*pi)
        graphs[GraphTypes.Attenuation] = [[f, -mag, False, False], ["f[Hz]", "At[dB]"]]   # se pasa una lista de graphvalues
        graphs[GraphTypes.Norm_Attenuation] = [[f_n, -mag_n, False, False], ["f[Hz]", "At[dB]"]]
        graphs[GraphTypes.Phase] = [[f, phase, False, False], ["f[Hz]", "phase[deg]"]]
        graphs[GraphTypes.GroupDelay] = [[f, -2*pi*diff(unwrap(phase))/diff(w), False, False], ["f[Hz]", "Group delay [s]"]]  # -d(Phase)/df = -dP/dw * dw/df = -dP/dw * 2pi
        graphs[GraphTypes.PolesZeros] = [[self.denormalized["Zeros"].real, self.denormalized["Zeros"].imag, False, True],
                                 [self.denormalized["Poles"].real, self.denormalized["Poles"].imag, True, True], ["Re(s)", "Im(s)"]]
        t, imp = signal.impulse(trans_func)
        graphs[GraphTypes.Impulse] = [[t, imp, False, False], ["t[s]", "V[V]"]]
        t, step = signal.step(trans_func)
        graphs[GraphTypes.Step] = [[t, step, False, False], ["t[s]", "V[V]"]]
        i = 0
        while i < len(self.denormalized["StagesQ"]):
            graphs[GraphTypes.StagesQ][i].append([[0, self.denormalized["StagesQ"][i]], [i+1, i+1], True, False])
            i += 1
        graphs[GraphTypes.StagesQ][i].append(["Q", "Q N°"])
        return graphs

    @staticmethod
    def _agrup_roots(p):
        new_p = []
        p.sort(key=lambda x: x.real)  # ordeno por parte real creciente
        while len(p):
            len_in = len(new_p)
            for i in range(1, len(p)):
                if (abs(p[0].real - p[i].real) < 1e-10) and (abs(p[0].imag + p[i].imag) < 1e-10):
                    new_p.append(p[0])
                    new_p.append(complex(p[0].real, -p[0].imag))    # fuerzo que sean valores iguales
                    p.remove(p[i])
                    break
            if len_in == len(new_p):  # si no le encontre un conjugado
                new_p.append([p[0]])  # no lo tiene :(
                p.remove(p[0])
        return new_p
