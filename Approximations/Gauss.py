"""
Approximation base class
"""

# third-party modules
from sympy import *
from scipy import signal
import json

from numpy import unwrap
from numpy import diff
from numpy import log
from numpy import divide
from numpy import where
from numpy import pi
from numpy import amax

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class Gauss(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Gauss")
        self.application = [FilterTypes.GroupDelay]
        self.information = {}
        self._pre_calc(20)  # n_max = 20

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Gauss is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter, n_max=20, denorm=0):
        if filter_in_use.get_type() is FilterTypes.GruopDelay:
            """ If the approximation supports the filter I continue """
            """ Using the precalculated plots I get the order and the frequency for the -3dB point"""
            n = self._ord()
            """ Now we limit the order of the filter """
            n = amax([n, n_max])
            """ After getting the order I get the zeros, poles and gain of the filter """
            z_n, p_n, k_n = self._gauss_norm(n)
            filter_in_use.load_normalized_z_p_k(z_n, p_n, k_n)
            z, p, k = self._gauss_des(z_n, p_n)
            filter_in_use.load_z_p_k(z, p, k)


    " ONCE I HAVE THE SPECS I CALL THIS METHOD "
    def _ord(self):
        plots_file = open("PreCalc/gauss.json")
        data = json.load(plots_file)
        n = 0
        for n_i in data:
            tol = data[n_i]["Group delay"][where(data[n_i]["w"] >= 1)[0]]
            # wt = data[n_i]["w"][where(data[n_i]["Group Delay"] <= self.information[TemplateInfo.tol])[0]]
            if tol >= self.information[TemplateInfo.tol]:
                n = int(n_i)
                break
        return n

    def _gauss_norm(self, n: int):
        " Returns zeros, poles and gain of Gauss normalized approximation "
        transfer_function = self._get_tf(n)
        trans_zpk = transfer_function.to_zpk()
        return trans_zpk.zeros, trans_zpk.poles, trans_zpk.gain

    def _gauss_des(self, z_n, p_n):
        " Returns zeros, poles and gain of Gauss denormalized approximation "
        p = p_n/self.information[TemplateInfo.gd]
        k = prod(abs(p))
        return z_n, p, k

    def _pre_calc(self, n_max: int):
        data = {}
        outfile = open("gauss.json", "w")
        for i in range(2, n_max + 1):
            transfer_function = self._get_tf(i)
            w, mag, phase = transfer_function.bode(n=1500)
            gd = -diff(unwrap(phase)) / diff(w)
            gd = divide(gd, gd[0])
            data[str(i)] = {}
            # data[str(i)] = {"w": w.tolist(), "|H(jw)[dB]|": mag.tolist(), "Group delay": gd.tolist()}
            data[str(i)] = {"w": w.tolist(), "Group delay": gd.tolist()}    # guardo solo retardo de grupo que es lo que me van a pedir cumplit
        json.dump(data, outfile, indent=4)
        outfile.close()

    def _get_tf(self, n: int):
        """
        Returns the normalized transfer function of the Gauss Approximation
        :param n: Order of the gauss polynomial
        :return: Scipy signal transfer function
        """
        z, p, k = self._get_zpk(n)
        transfer_function = signal.ZerosPolesGain(z, p, k)
        return transfer_function

    @staticmethod
    def _get_zpk(n: int):
        """
        :param n: Gauss approximation order. N_MIN = 2
        :return: The Gauss Approximation Zeros, Poles and Gain
        """
        num = [1.]
        den = []
        for k in range(n+1, 1, -1):
            # den.append((-1)**k*gamma**k/factorial(k))
            den.append(1 / factorial(k))    # normalizamos con gamma=1
            den.append(0)
        den.append(1.)
        transfer_function = signal.TransferFunction(num, den)   # tengo la transferencia al cuadrado
        p = transfer_function.poles
        p = p[where(p.real < -1e-10)]    # me quedo con los polos del semiplano izquierdo. -1e-10 xq sino n=7 me quedaba inestable, problema: queda de un orden menos para n impar!!!!!
        k = prod(abs(p))                      # para que la ganancia sea 1
        return [], p, k
