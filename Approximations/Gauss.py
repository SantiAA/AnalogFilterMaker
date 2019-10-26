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
        self.ft_n = 0

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Gauss is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter, n_max = 20):
        if filter_in_use.get_type() is FilterTypes.GruopDelay:
            """ If the approximation supports the filter I continue """
            """ Using the precalculated plots I get the order and the frequency for the -3dB point"""
            self.ft_n = self.information[TemplateInfo.ft] / self.information[TemplateInfo.fp]   # normalize ft
            n = self._ord()

            """ Now we limit the order of the filter """
            n = amax([n, n_max])
            """ After getting the order I get the zeros, poles and gain of the filter """

            z, p, k = self._gauss_des(n)
            # filter_in_use.load_z_p_k(z, p, k)
            z_n, p_n, k_n = self._gauss_norm(n)
            # filter_in_use.load_normalized(z_n, p_n, k_n)


    " ONCE I HAVE THE SPECS I CALL THIS METHOD "
    def _ord(self):
        plots_file = open("PreCalc/gauss.json")
        data = json.load(plots_file)
        n1 = 0
        n2 = 0
        works = False
        for n_i in data:
            wt = where(data[n_i]["Group Delay"] < self.information[TemplateInfo.tol])[0]
            if wt > self.ft_n * 2 * pi:
                n1 = int(n_i)
                break

        if n1:
            for n_i in data:
                wp = where(data[n_i]["|H(jw)[dB]|"] < -self.information[TemplateInfo.Ap])[0]
                if wp > 2 * pi:
                    n2 = int(n_i)
                    break
        n = amax([n1, n2])
        w = data[str(n)]["w"]
        return n, w

    def _gauss_des(self, n: int):
        " Returns zeroes, poles and gain of Gauss denormalized approximation "
        return

    def _gauss_norm(self, n: int):
        " Returns zeroes, poles and gain of Gauss normalized approximation "
        transfer_function = self._get_tf(n)
        trans_zpk = transfer_function.to_zpk()
        return trans_zpk.zeros, trans_zpk.poles, trans_zpk.gain

    def _pre_calc(self, n_max: int):
        data = {}
        outfile = open("PreCalc/gauss.json", "w")
        for i in range(1, n_max + 1):
            transfer_function = self._get_tf(i)
            w, mag, phase = transfer_function.bode()
            gd = -diff(unwrap(phase)) / diff(w)
            gd = divide(gd, gd[0])
            data[str(i)] = {}
            data[str(i)] = {"w": w.tolist(), "|H(jw)[dB]|": mag.tolist(), "Group delay": gd.tolist()}
        json.dump(data, outfile, indent=4)
        outfile.close()

    def _get_tf(self, n: int):
        """
        Returns the normalized transfer function of the Gauss Approximation
        :param n: Order of the gauss polynomial
        :return: Scipy signal transfer function
        """
        num = [1.]
        den = self._den(n)
        transfer_function = signal.TransferFunction(num, den)
        return transfer_function

    def _den(self, n: int):
        """
        :param n: Gauss approximation order
        :return: The Gauss Approximation Denominator
        """
        den = []
        gamma = log(2)
        for k in range(n, 1, -1):
            den.append(gamma ** k)
            den.append(0)
        den.append(1.)
        return den
