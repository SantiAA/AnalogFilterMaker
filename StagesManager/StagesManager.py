# python native modules
from enum import Enum

from numpy import conjugate
from numpy import argmin
from numpy import full


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
        self.sos = []

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
                self.p_pairs.append([abs(p[0])])  # si no tiene Q
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
        self.p_pairs.sort(key=lambda x:x[1], reverse=True) # ordeno polos por Q decreciente
        self.z_pairs.sort(key=lambda x:x[1], reverse=True) # ordeno ceros por orden decreciente
        self.k = k

    def get_singularities(self):
        """ Returns tuple with 1st/2nd order poles and 1st/2nd order zeros """
        return self.z_pairs, self.p_pairs

    def get_max_rd_stages(self, sig_type: SignalTypes):
        # agrupo todas
        self.sos = []
        """ To agrupate nearest poles and zeros """
        if len(self.z_pairs):   # si tiene ceros
                adj_matrix = [] # aqui se guardaran todas las distancias entre frecuencias de corte de polos y ceros
                for i in range(len(self.z_pairs)):      # para cada cero
                    if self.z_pairs[i][1] > 1:  # si el cero es de segundo orden
                        for j in range(len(self.p_pairs)):
                            if len(self.p_pairs[j]) > 1:  # si el polo es de segundo orden
                                dist = abs(self.z_pairs[i][0] - self.p_pairs[j][0])
                                adj_matrix[i][j] = dist         # guardo la distancia entre cada polo y cero de orden 2
                k = 0
                k_max = len(self.z_pairs)
                used_p = full(adj_matrix.shape(1), False)
                while k < k_max:
                    i, j = argmin(adj_matrix)
                    self.sos.append([self.p_pairs[j], self.z_pairs[i]])
                    adj_matrix[i][j] = 1e9  # ya no me interesa esta distancia, la hago grande para que no salga elegida
                    used_p[j] = True    # marca que este polo ya se utilizo
                    k += 1
                for i in range(adj_matrix.shape(1)):
                    if not used_p[i]:
                        self.sos.append([self.p_pairs[i], None])
                # ver que hacer con los polos y ceros de primer orden aaaaaaaaa
        else:
            self.sos = [ [p, None] for p in self.p_pairs]
        """" The order of the stages depends on the input signal """
        if sig_type is SignalTypes.LowSignal:
            self.sos.sort(key=lambda x:x[0][1], reverse=True) # ordena por Q decreciente
            # k a la primera celda
        elif sig_type is SignalTypes.HighSignal:
            self.sos.sort(key=lambda x:x[0][1], reverse=True) # ordena por Q creciente
            # k a la ultima celda
        elif sig_type is SignalTypes.MedSignal:
            # preguntarle a dani
            pass
        return self.sos

    def