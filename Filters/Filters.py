# python native modules
from enum import Enum
from numpy import poly
from numpy import sqrt
from numpy import conj
from numpy import angle
from numpy import log10
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
    Normalized = "Normalized"
    Attenuation = "Attenuation"
    Module = "Module"
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
        self.limits = {
            TemplateInfo.Aa.value: (0, 10e9), TemplateInfo.Ap.value: (0, 10e9), TemplateInfo.fa.value: (0, 10e9),
            TemplateInfo.fp.value: (0, 10e9), TemplateInfo.fp_.value: (0, 10e9), TemplateInfo.fp__.value: (0, 10e9),
            TemplateInfo.fa_.value: (0, 10e9), TemplateInfo.fa__.value: (0, 10e9), TemplateInfo.fo.value: (0, 10e9),
            TemplateInfo.ft.value: (0, 10e9), TemplateInfo.gd.value: (0, 10e9), TemplateInfo.tol.value: (0, 1),
            TemplateInfo.k.value: (0, 10e9)
        }
        self.defaults = {
            TemplateInfo.Aa.value: 50, TemplateInfo.Ap.value: 30, TemplateInfo.fa.value: 20000, TemplateInfo.fp.value: 2000,
            TemplateInfo.fp_.value: 30000, TemplateInfo.fp__.value: 3000, TemplateInfo.fa_.value: 45000, TemplateInfo.fa__.value: 2000,
            TemplateInfo.fo.value: 9486, TemplateInfo.ft.value: 10000, TemplateInfo.gd.value: 10e-3, TemplateInfo.tol.value: 0.2,
            TemplateInfo.k.value: 1
        }

    def get_type(self) -> FilterTypes:
        return self.filter

    def get_limit(self, info: TemplateInfo):
        return self.limits[info.value]

    def get_default(self, info: TemplateInfo):
        return self.defaults[info.value]

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
        p = self._agrup_roots(p)     # ordena Re(p) creciente, se asegura que los comp conj tengan el mismo valor
        self.denormalized["Poles"] = p
        while len(p):                 # agrupo en polos complejos conjugados
            # len_in = len(self.denormalized["StagesQ"])
            for i in range(1, len(p)):
                if p[0] == p[i].conjugate():
                    # pairs.append(p[0])
                    wo = sqrt(abs(p[0] * p[i]))
                    q = -wo / (p[0].real + p[i].real)
                    self.denormalized["StagesQ"].append(q)
                    p.remove(p[i])
                    break
            p.remove(p[0])
            # if len_in == len(self.denormalized["StagesQ"]):  # si no le encontre un conjugado
            #    pairs.append([p[0]])  # no lo tiene :(
            #    self.denormalized["StagesQ"].append(-1)
        self.denormalized["MaxQ"] = amax(self.denormalized["StagesQ"])

    def load_normalized_z_p_k(self, z, p, k):
        self.normalized["Zeros"] = z
        self.normalized["Poles"] = p
        self.normalized["Gain"] = k
        self.normalized["Order"] = len(p)

    def get_z_p_k_q(self):
        """ Returns poles ordered: conjugates are next to each other """
        return self.denormalized["Zeros"], self.denormalized["Poles"], self.denormalized["Gain"], \
               self.denormalized["StagesQ"]

    def get_req_limit(self, key: TemplateInfo):
        return self.limits[key]

    def get_all_graphs(self):
        graphs = {}
        trans_func = signal.ZerosPolesGain(self.denormalized["Zeros"], self.denormalized["Poles"], self.denormalized["Gain"])
        norm_trans_func = signal.ZerosPolesGain(self.normalized["Zeros"], self.normalized["Poles"], self.normalized["Gain"])
        w, h = trans_func.freqresp(n=3000)
        f = w/(2*pi)
        mag = 20 * log10(abs(h))
        phase = angle(h)
        w_n, h_n = norm_trans_func.freqresp(n=3000)
        f_n = w_n/(2*pi)
        mag_n = 20 * log10(abs(h_n))
        phase_n = angle(h_n)
        graphs[GraphTypes.Module] = [[f, -mag, False, False, True], ["Frequency [Hz]", "Amplitude [dB]"]]
        graphs[GraphTypes.Attenuation] = [[f, -mag, False, False, True], ["Frequency [Hz]", "Attenuation[dB]"]]   # se pasa una lista de graphvalues
        if self.filter is FilterTypes.GroupDelay:
            graphs[GraphTypes.Normalized] = [[f, -2 * pi * diff(unwrap(phase_n)) / diff(w_n), False, False, True],
                                             ["Frequency[Hz]", "Group delay [s]"]]  # -d(Phase)/df = -dP/dw * dw/df = -dP/dw * 2pi
        else:
            graphs[GraphTypes.Normalized] = [[f_n, -mag_n, False, False, True], ["Frequency[Hz]", "Attenuation[dB]"]]
        graphs[GraphTypes.Phase] = [[f, phase, False, False, True], ["Frequency[Hz]", "Phase[deg]"]]
        graphs[GraphTypes.GroupDelay] = [[f, -2*pi*diff(unwrap(phase))/diff(w), False, False, True], ["Frequency[Hz]", "Group delay [s]"]]  # -d(Phase)/df = -dP/dw * dw/df = -dP/dw * 2pi
        graphs[GraphTypes.PolesZeros] = [[self.denormalized["Zeros"].real, self.denormalized["Zeros"].imag, False, True, False, "Zeros"],
                                [self.denormalized["Poles"].real, self.denormalized["Poles"].imag, True, True, False, "Poles"], ["Re(s)", "Im(s)"]]
        t, imp = signal.impulse(trans_func)
        graphs[GraphTypes.Impulse] = [[t, imp, False, False, False], ["t[s]", "V[V]"]]
        t, step = signal.step(trans_func)
        graphs[GraphTypes.Step] = [[t, step, False, False, False], ["t[s]", "V[V]"]]
        if len(self.denormalized["StagesQ"]):   # los filtros de primer orden no tienen Q
            i = 0
            while i < len(self.denormalized["StagesQ"]):
                graphs[GraphTypes.StagesQ][i].append([[0, self.denormalized["StagesQ"][i]], [i+1, i+1], True, False, False])
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
