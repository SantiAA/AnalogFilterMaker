# python native modules
from enum import Enum

from numpy import conjugate, amax, amin
from numpy import argmin
from numpy import full
from numpy import log10
from enum  import Enum

# AFM project modules
from Filters.Filters import Filter
from StagesManager.Pole import Pole
from StagesManager.Zero import Zero

class ShowType(Enum):
    Selected = "Selected",
    Accumulative = "Accumulative",
    Superposed = "Superposed"


class StagesManager(object):

    def __init__(self, fil: Filter):
        self.p_pairs = [] # va a tener arreglo de Poles
        self.z_pairs = [] # va a tener arreglos de Zeros
        self.sos = []
        """ Guarda todos los polos y ceros agrupados en etapas de 1/2do orden """
        z, p, self.k_tot, q = fil.get_z_p_k_q()
        saved = False
        while len(p):  # guardo en self.p_pairs los pares de polos complejos conjugados como [wo,Q]
            if len(p) > 1:
                if p[0] == conjugate(p[1]):
                    #self.p_pairs.append([abs(p[0]), q[0]])
                    self.p_pairs.append(Pole(p))
                    p.remove(p[1])
                    saved = True
            if not saved:
                self.p_pairs.append([abs(p[0])])  # si no tiene Q
            p.remove(p[0])
            saved = False
        while len(z):  # guardo en self.z_pairs los pares de ceros complejos conjugados como [wo,n]
            if len(z) > 1:
                if z[0] == conjugate(z[1]):
                    self.z_pairs.append(Zero(abs(z[0].im), 2))
                    z.remove(z[1])
                    saved = True
            if not saved:
                self.z_pairs.append([abs(z[0])])  # si no tiene
            z.remove(z[0])
            saved = False
        self.p_pairs.sort(key=lambda x: x.q, reverse=True)  # ordeno polos por Q decreciente
        self.z_pairs.sort(key=lambda x: x.n, reverse=True)  # ordeno ceros por orden decreciente

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

        return self.sos

    def get_stages(self):
        """" Returns Stages list """
        return self.sos

    def add_stage(self, p_str: str, z_str: str) -> (bool,str):
        """ Devuelve True es valida la etapa solicitada, False si no """

        # self.sos[i]["Poles"] = p
        # self.sos[i]["Zeros"] = z

    def shift_stages(self, indexes: list, left):
        """ Shifts the stages indicated at the indexes list. Shifts left if left == True,shifts rigth otherwise"""
        pass

    def delete_stages(self, indexes: list):
        """" Deletes stages indicated by indexes list """
        if amax(indexes) < len(self.sos):
            self.sos.remove(self.sos[indexes])
        else:
            print("Indexes list out of range!")

    def calc_rd(self):
        # vi_max = self.requirements[StageInfo.Vo_max]
        # for s in self.sos:
        #     vi_max /= s["Gain"]
        # rd = 20*log10(vi_max/self.requirements[StageInfo.Vi_min]
        return rd

    def set_gain(self, i, k) -> (bool, str):
        if i < len(self.sos):
            partial_gain = 0
            for k in range(len(self.sos)):
                partial_gain += self.sos[k].k if k != i else k
            if partial_gain <= self.k_tot:
                self.sos[i].k = k
                return True, ""
            else:
                return False, "Total gain can't exceed" + str(self.k_tot) + "dB"
        else:
            return False, "Stage" + str(i + 1) + "doesn't exist."
    def get_z_p_plot(self):
        """" Returns poles and zeros diagram with number of repeticiones of each pole and zero """


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


    def get_z_p_dict(self):
        """ Returns a dictionary with all zeros and poles:
         { "Poles": {"1st order": [Poles], "2nd order": [Poles]}
           "Zeros": {"1st order": [Zeros], "2nd order": [Zeros]} } """
        ret = {"Poles": {"1st order": [], "2nd order": []}, "Zeros": {"1st order": [], "2nd order": []}}
        for p in self.p_pairs:
            key2 = "1st order" if p.q < 0 else "2nd order"
            ret["Poles"][key2].append(p)
        for z in self.z_pairs:
            key2 = "1st order" if z.n == 1 else "2nd order"
            ret["Zeros"][key2].append(z)
        return ret

    def get_stages_plot(self, i, ):
        plot_list = [[], []]
        for st in self.sos:
            plot_list[0].append(st.get_tf_plot())
        plot_list[1] = ["Frequency [Hz]", "Amplitude [dB]"]
        return plot_list

    def get_dr(self, vi_min, vo_max):
        """Returns a tuple:
            (True, dr) if everytihing ok, (False, err_str) if error
            Could fail because of: Invalid vi values, or not all stages loaded"""
        ret = ""
        ok = False
        if vi_min < vo_max:
            if vi_min <= 2:
                if vo_max >= 3:
                    max_rd = 0
                    for i in range(len(self.sos)):
                        rd = self._get_stg_dr(i, vi_min, vo_max)
                        if rd > max_rd:
                            max_rd = rd
                    ok = True
                else:
                    ret = "Vo max should be greater than 3V"
            else:
                ret = "Vi min should be smaller than 2V (go to a less noisy place!)"
        else:
            ret = "Vo_max must be greater than vi_min"
        return ok, ret

    def _get_stg_dr(self, i, vi_min, vo_max):
        """ Returns stage i dynamic range """
        partial_gain = 0
        for j in range(i): # recorro todas las etapas hasta la que quiero calcular el rango dinamico
            partial_gain += self.sos[j].k
        vi_max = amin(vo_max, vo_max/partial_gain)
        vi_min = amax(vi_min, vi_min/partial_gain) # vi_min: minimo valor a la entrada tal que la salida no este en el piso de ruido y la entrada no este en el piso de ruido
        return 20*log10(vi_max/vi_min)

    def get_const_data(self, i, vi_min, vo_max):
        """Returns a dictionary with string values of the stage i"""
        ret = {"Q": ["", ""], "fo": ["", "Hz"], "DR": ["", "dB"]}
        if type(i) is int:
            if i < len(self.sos):
                q = self.sos[i].p.q
                if q > 0:
                    ret["Q"][0] = str(q)
                ret["fo"][0] = str(self.sos[i].p.fo)
                ret["DR"][0] = str(self._get_stg_dr(i, vi_min, vo_max))


        else:
            # ret = vacio
            pass
        return ret
