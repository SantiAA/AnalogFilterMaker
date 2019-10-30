# python native modules
from enum import Enum

from numpy import conjugate, amax, amin, pi, real, imag
from numpy import argmin
from numpy import full
from numpy import log10
from enum  import Enum

# AFM project modules
from scipy import signal

from BackEnd.Output.plots import GraphValues
from Filters.Filters import Filter
from StagesManager.Pole import Pole
from StagesManager.Stage import Stage
from StagesManager.Zero import Zero


class ShowType(Enum):
    Selected = "Selected",
    Accumulative = "Accumulative",
    Superposed = "Superposed"


class StagesManager(object):

    def __init__(self):
        self.p_pairs = [] # va a tener arreglo de Poles
        self.z_pairs = [] # va a tener arreglos de Zeros
        self.unused_p = []
        self.unused_z = []
        self.sos = []
        self.k_tot = 0

    def load_filter(self, fil: Filter):
        """ Guarda todos los polos y ceros agrupados en etapas de 1/2do orden """
        z, p, self.k_tot, q = fil.get_z_p_k_q()
        saved = False
        while len(p):  # guardo en self.p_pairs los pares de polos complejos conjugados como [wo,Q]
            if len(p) > 1:
                if p[0] == conjugate(p[1]):
                    self.p_pairs.append(Pole(p))
                    p.remove(p[1])
                    saved = True
            if not saved:
                self.p_pairs.append(p[0])  # si no tiene conjugado deberia ser real
            p.remove(p[0])
            saved = False
        while len(z):  # guardo en self.z_pairs los pares de ceros complejos conjugados como [wo,n]
            if len(z) > 1:
                if z[0] == conjugate(z[1]):
                    self.z_pairs.append(Zero(abs(z[0].im), 2))
                    z.remove(z[1])
                    saved = True
            if not saved:
                self.z_pairs.append(Zero(abs(z[0].im), 1))  # si no tiene conjugado es de primer orden en el origen
            z.remove(z[0])
            saved = False
        self.p_pairs.sort(key=lambda x: x.q, reverse=True)  # ordeno polos por Q creciente
        self.z_pairs.sort(key=lambda x: x.n, reverse=True)  # ordeno ceros por orden creciente
        self.unused_p = self.p_pairs
        self.unused_z = self.z_pairs

    def auto_max_rd(self, vi_min, vi_max):
        # agrupo todas
        self.sos = []
        z_1 = None  # habra como mucho un cero de primer orden
        p_1 = None  # habra como mucho un polo de primer orden
        """ To agrupate nearest poles and zeros """
        if len(self.z_pairs):   # si tiene ceros
                adj_matrix = [] # aqui se guardaran todas las distancias entre frecuencias de corte de polos y ceros
                for i in range(len(self.z_pairs)):      # para cada cero
                    if self.z_pairs[i].n == 2:  # si el cero es de segundo orden
                        for j in range(len(self.p_pairs)):
                            if self.p_pairs[j].q > 0:  # si el polo es de segundo orden
                                dist = abs(self.z_pairs[i].imag - self.p_pairs[j].fo)
                                adj_matrix[i][j] = dist         # guardo la distancia entre cada polo y cero de orden 2
                            else:
                                if p_1 is None:
                                    p_1 = self.p_pairs[j]
                    else:
                        if z_1 is None:
                            z_1 = self.z_pairs[i].n
                used_p = full(adj_matrix.shape(1), False)
                i, j = (0, 0)
                while adj_matrix[i][j] < 1e9:
                    i, j = argmin(adj_matrix)
                    self.sos.append(Stage(self.z_pairs[i], self.p_pairs[j], 1)) # ganancia 1 por defecto
                    self.unused_z.remove(self.z_pairs[i])
                    self.unused_p.remove(self.p_pairs[j])
                    adj_matrix[i] = full(adj_matrix.shape(0),1e9)  # ya no me interesa esta distancia, la hago grande para que no salga elegida
                    adj_matrix[ : ,j] = full(adj_matrix.shape(1), 1e9)
                    used_p[j] = True    # marca que este polo ya se utilizo
                for i in range(adj_matrix.shape(1)):
                    if not used_p[i]:
                        if z_1 is None:
                            self.sos.append(Stage([], self.p_pairs[i], 1))
                        else:   # si hay algun cero de primer oden, se lo agrego a la primera etapa sin ceros que aparezca
                            self.sos.append(Stage(z_1, self.p_pairs[i], 1))
                            self.unused_z.remove(self.z_pairs[i])
                            z_1 = None
                        self.unused_p.remove(self.p_pairs[i])
                if p_1 is not None:
                    zero = complex(0)
                    if z_1 is not None:
                        zero = z_1
                        z_1 = None
                        self.unused_z.remove(z_1)
                    self.sos.append(Stage(zero, p_1, 1))
                    self.unused_p.remove(p_1)
                    p_1 = None
        else:
            self.sos = [Stage([],p,1) for p in self.p_pairs]
            self.unused_p.remove(self.p_pairs)
        self.sos.sort(key=lambda x:x.p.q) # ordena por Q decreciente
        self.sos[-1].set_gain(self.k_tot) # le pongo toda la ganancia a la ultima etapa
        return self.sos

    def get_stages(self):
        """" Returns Stages list """
        return self.sos

    def add_stage(self, p_str: str, z_str: str) -> (bool,str):
        """ Devuelve True es valida la etapa solicitada, False si no """
        ret = ""
        ok = False
        zero = None
        pole = None
        for z in self.z_pairs:
            if z_str == z.get_msg():
                zero = z
                break
        for p in self.p_pairs:
            if p_str == p.get_msg():
                pole = p
            self.sos.append(Stage(zero, pole, 1))
        if not (pole.q < 0 and zero.n == 2):
            pole_n_left = 0
            z_n_left = 0
            for p in self.unused_p:
                pole_n_left += 2 if p.q > 0 else 1
            for z in self.unused_z:
                z_n_left += z.n
            if pole_n_left >= z_n_left:
                ok = True
            else:
                ret = "There must be greater o equal amount of poles than zeros remaing after selection"
        else:
            ret = "Zero's order can't be greater than pole's order"
        return ok, ret

    def shift_stages(self, indexes: list, left):
        """ Shifts the stages indicated at the indexes list. Shifts left if left == True,shifts rigth otherwise"""
        if left:
            step = -1
            i_lim = 0
            i = len(self.sos)
        else:
            step = 1
            i_lim = len(self.sos)
            i = 0

        rep = step
        while i != i_lim:
            if i in indexes:
                while i+rep in indexes:
                    rep += step
                self.sos[i], self.sos[i+rep] = (self.sos[i+rep], self.sos[i])
            i += step
            rep = step

    def delete_stages(self, indexes: list):
        """" Deletes stages indicated by indexes list """
        if amax(indexes) < len(self.sos):
            self.sos.remove(self.sos[indexes])
        else:
            print("Indexes list out of range!")

    def set_gain(self, i, k) -> (bool, str):
        if i < len(self.sos):
            partial_gain = 0
            for j in range(len(self.sos)):
                partial_gain += self.sos[j].k if j != i else 10**(k/20)
            if partial_gain <= self.k_tot:
                self.sos[i].k = 10**(k/20)
                return True, ""
            else:
                return False, "Total gain can't exceed" + str(self.k_tot) + "dB"
        else:
            return False, "Stage" + str(i + 1) + "doesn't exist."

    def get_z_p_plot(self):
        """" Returns poles and zeros diagram with number of repeticiones of each pole and zero """
        repeated_z = []
        z = []
        repeated_p = []
        p = []
        i = 0
        while i < len(self.z_pairs):
            count = self.z_pairs.count(self.z_pairs[i])
            add = 0
            for j in range(count):
                add += self.z_pairs[i + j].n
            repeated_z.append(add)
            z.append(complex(0,self.z_pairs[i].im))
            i += count
        i = 0
        while i < len(self.p_pairs):
            count = self.p_pairs.count(self.p_pairs[i])
            repeated_p.append(count)
            p.append(self.p_pairs[i].p)
            i += count
        return [[GraphValues(real(z), imag(z), True, False, False, "Zeros", repeated_z), GraphValues(real(p),
                        imag(p), True, True, False, "Poles", repeated_p)], ["Re(s)[rad/sec]", "Im(s)[rad/sec]"]]


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

    def get_stages_plot(self, i, type: ShowType):
        plot_list = [[], []]
        if type is ShowType.Accumulative.value:
            z = []
            p = []
            for s in self.sos:
                z += s.z
                p += s.p
            transf = signal.ZerosPolesGain(z,p,self.k_tot)
            w, mag = transf.freqresp(n=3000)
            f = w/(2*pi)
            plot_list = [[GraphValues(f, mag, False, False, True)], ["Frequency [Hz]", "Amplitude [dB]"]]
        else:
            if type is ShowType.Superposed:
                i = list(range(len(self.sos)))
            for st in self.sos[i]:
                plot_list[0].append(st.get_tf_plot())
            plot_list[1] = ["Frequency [Hz]", "Amplitude [dB]"]
        return plot_list

    def get_dr(self, vi_min, vo_max):
        """Returns a tuple:
            (True, dr) if everytihing ok, (False, err_str) if error
            Could fail because of: Invalid vi values, or not all stages loaded"""
        valid = self._validate_vi(vi_min, vo_max)
        ok = valid[0]
        ret = valid[1]
        if valid[0]:
            max_rd = 0
            for i in range(len(self.sos)):
                rd = self._get_stg_dr(i, vi_min, vo_max)
                if rd > max_rd:
                    max_rd = rd
                ret = str(max_rd)
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
                if self._validate_vi(vi_min, vo_max)[0]:
                    ret["DR"][0] = str(self._get_stg_dr(i, vi_min, vo_max))
        return ret

    @staticmethod
    def _validate_vi(vi_min, vo_max):
        ok = False
        ret = ""
        if vi_min < vo_max:
            if vi_min <= 2:
                if vo_max >= 3:
                    ok = True
                else:
                    ret = "Vo max should be greater than 3V"
            else:
                ret = "Vi min should be smaller than 2V (go to a less noisy place!)"
        else:
            ret = "Vo_max must be greater than vi_min"
        return ok, ret