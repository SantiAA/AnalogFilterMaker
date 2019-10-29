# python native modules
from enum import Enum

from numpy import conjugate

# AFM project modules
from Filters.Filters import Filter


class SignalTypes(Enum):
    LowSignal = "Low Signal (Vi \\approx Vimin)"
    HighSignal = "High Signal (Vi >> Vimin)"
    MedSignal = "Intermmediate Signal"


class StageInfo(Enum):
    Vi_min = "Vi min (Noise floor)"
    Vo_max = "Vo max"


class StagesManager(object):

    def __init__(self):
        self.requirements = {StageInfo.Vi_min: None,
                             StageInfo.Vo_max: None}
        self.limits = {StageInfo.Vi_min: (0, 1), StageInfo.Vo_max: (0, 1e9)}
        self.p_pairs = [] # va a tener arreglos de polos de 1er o 2do orden, guarda wo y Q (Q solo en 2do)
        self.z_pairs = [] # va a tener arreglos de ceros de 1er y 2do orden, guarda wo y orden (siempre estan sobre el eje im)
        self.k = 0
        self.stages = []

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
        for each in self.requirements:
            if self.requirements[each] is None:
                return False  # Check if every spec was loaded
            
        if self.requirements[StageInfo.Vi_min] < self.requirements[StageInfo.Vo_max]:
            return True
        
        return False

    def load_filter(self, fil: Filter):
        """ Guarda todos los polos y ceros agrupados en etapas de 1/2do orden """
        z, p, k, q = fil.get_z_p_k_q()
        saved = False
        while len(p):   # guardo en self.p_pairs los pares de polos complejos conjugados como [wo,Q]
            if len(p) > 1:
                if p[0] == conjugate(p[1]):
                    self.p_pairs.append([abs(p[0]),q[0]])   
                    q.remove(q[0])
                    p.remove(p[1])
                    saved = True
            if not saved:
                self.p_pairs.append([abs(p[0])])  # si no tiene
            p.remove(p[0])
            saved = False
        while len(z):   # guardo en self.z_pairs los pares de ceros complejos conjugados como [wo,n]
            if len(z) > 1: 
                if z[0] == conjugate(z[1]):
                    self.z_pairs.append([abs(z[0]), 2]) 
                    z.remove(z[1])
                    saved = True
            if not saved:
                self.z_pairs.append([abs(z[0])])  # si no tiene
            z.remove(z[0])
            saved = False
        self.p_pairs.sort(key=lambda x:x[0]) # ordeno polos por wo creciente
        self.z_pairs.sort(key=lambda x:x[0]) # ordeno ceros por wo creciente
        self.k = k

    def get_stages(self):
        """ Returns tuple with 1st/2nd order pole stages and 1st/2nd order zeros stages"""
        return self.z_pairs, self.p_pairs

    def get_max_rd_stages(self, sig_type: SignalTypes):
        # agrupo todas
        self.stages = None
        # self
        if sig_type is SignalTypes.LowSignal:
            self.stages.sort(self.)
        elif sig_type is SignalTypes.HighSignal:
            pass
        elif sig_type is SignalTypes.MedSignal:
            pass
        return self.stages

    def