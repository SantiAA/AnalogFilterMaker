# python native modules
from enum import Enum

from numpy import conjugate
from numpy import argmin
from numpy import full
from numpy import log10


# AFM project modules
from Filters.Filters import Filter


class StagesManager(object):

    def __init__(self, fil: Filter):
        self.p_pairs = [] # va a tener arreglos de polos de 1er o 2do orden, guarda wo y Q (Q solo en 2do)
        self.z_pairs = [] # va a tener arreglos de ceros de 1er y 2do orden, guarda wo y orden (siempre estan sobre el eje im)
        self.sos = []
        """ Guarda todos los polos y ceros agrupados en etapas de 1/2do orden """
        z, p, self.k, q = fil.get_z_p_k_q()
        saved = False
        while len(p):  # guardo en self.p_pairs los pares de polos complejos conjugados como [wo,Q]
            if len(p) > 1:
                if p[0] == conjugate(p[1]):
                    self.p_pairs.append([abs(p[0]), q[0]])
                    q.remove(q[0])
                    p.remove(p[1])
                    saved = True
            if not saved:
                self.p_pairs.append([abs(p[0])])  # si no tiene Q
            p.remove(p[0])
            saved = False
        while len(z):  # guardo en self.z_pairs los pares de ceros complejos conjugados como [wo,n]
            if len(z) > 1:
                if z[0] == conjugate(z[1]):
                    self.z_pairs.append([abs(z[0]), 2])
                    z.remove(z[1])
                    saved = True
            if not saved:
                self.z_pairs.append([abs(z[0])])  # si no tiene
            z.remove(z[0])
            saved = False
        self.p_pairs.sort(key=lambda x: x[1], reverse=True)  # ordeno polos por Q decreciente
        self.z_pairs.sort(key=lambda x: x[1], reverse=True)  # ordeno ceros por orden decreciente
        self.sos = []


    def load_filter(self, fil: Filter):


    def get_singularities(self):
        """ Returns tuple with 1st/2nd order poles and 1st/2nd order zeros """
        return self.z_pairs, self.p_pairs

    def auto_max_rd(self, vi_min, vi_max):
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
                    self.sos.append({"Poles": self.p_pairs[j], "Zeros": self.z_pairs[i], "Gain": 1})    # ganancia 1 por defecto
                    adj_matrix[i][j] = 1e9  # ya no me interesa esta distancia, la hago grande para que no salga elegida
                    used_p[j] = True    # marca que este polo ya se utilizo
                    k += 1
                for i in range(adj_matrix.shape(1)):
                    if not used_p[i]:
                        self.sos.append({"Poles": self.p_pairs[i], "Zeros": None, "Gain": 1})
                # ver que hacer con los polos y ceros de primer orden aaaaaaaaa
        else:
            self.sos = [{"Poles": p, "Zeros": None, "Gain": 1} for p in self.p_pairs]
        """" The order of the stages depends on the input signal """
        self.sos.sort(key=lambda x:x["Poles"][1], reverse=True) # ordena por Q decreciente
        # k a la primera celda

            pass
        return self.sos

    def add_stage(self, p: Pole, z: Zero) -> (bool,str):
        """ Devuelve True si ya estan cargadas todas las etapas, False si no """
        # self.sos[i]["Poles"] = p
        # self.sos[i]["Zeros"] = z

    def shift_stages(self, indexes: list, left):
        """ Shifts the stages indicated at the indexes list. Shifts left if left == True,shifts rigth otherwise"""
        pass

    def delete_stages(self, indexes: list):
        """" Deletes stages indicated by indexes list """
        pass

    def calc_rd(self):
        # vi_max = self.requirements[StageInfo.Vo_max]
        # for s in self.sos:
        #     vi_max /= s["Gain"]
        # rd = 20*log10(vi_max/self.requirements[StageInfo.Vi_min])

        return rd

    def set_gain(self, i, k):
        self.sos[i]["Gain"] = k

    def get_z_p_plot(self):
        """" Returns poles and zeros diagram with number of repeticiones of each pole and zero """

    def get_z_p_dict(self):
        """ Returns a dictionary with all zeros and poles:
         { "Poles": {"1st order": [Poles], "2nd order": [Poles]}
           "Zeros": {"1st order": [Zeros], "2nd order": [Zeros]} } """

        # i = 0
        # while i < len(self.denormalized["Zeros"]):
        #     count = self.denormalized["Zeros"].count(self.denormalized["Zeros"][i])
        #     repeated_z.append(count)
        #     z.append(self.denormalized["Zeros"][i])
        #     i += count
        # i = 0
        # while i < len(self.denormalized["Poles"]):
        #     count = self.denormalized["Poles"].count(self.denormalized["Poles"][i])
        #     repeated_p.append(count)
        #     p.append(self.denormalized["Poles"][i])
        #     i += count

        # graphs[GraphTypes.PolesZeros.value] = [[GraphValues(real(z),
        #                                                     imag(z), True, False, False,
        #                                                     "Zeros", repeated_z),
        #                                         GraphValues(real(p),
        #                                                     imag(p), True, True, False,
        #                                                     "Poles", repeated_p)], ["Re(s)[rad/sec]", "Im(s)[rad/sec]"]]
    def get_stages_plot(self):
        pass


    def get_dr(self),vi_min, vi_max):
        """Returns a tuple:
            (True, dr) if everytihing ok, (False, err_str) if error
            Could fail because of: Invalid vi values, or not all stages loaded"""
        pass

    def get_const_data(self, i):
        """Returns a dictionary with string values of the stage i"""
        # ret = { "Q": "", "fo": "", "DR": ""}
        if type(i) is int:
            pass
        else:
            pass
        return ret
