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

# AFM project modules
from Approximations.Approx import Approximation
from Approximations.PreCalc.gauss import calculate_gauss
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class Gauss(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Gauss")
        self.application = [FilterTypes.GroupDelay]
        self.information = {}
        self._precalc(20)

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Gauss is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter):
        if filter_in_use.get_type() is FilterTypes.LowPass:
            """ If the approximation support the filter I continue """
            """ Using the precalculated plots I get the order and the frequency for the -3dB point"""

            """ After getting the order I get the zeros, poles and gain of the filter """
            # z, p, k =
            # filter_in_use.load_z_p_k(z, p, k)

        elif filter_in_use.get_type() is FilterTypes.HighPass:
            # z, p, k =
            # filter_in_use.load_z_p_k(z, p, k)

        elif filter_in_use.get_type() is FilterTypes.BandPass:
            # z, p, k =
            # filter_in_use.load_z_p_k(z, p, k)

        elif filter_in_use.get_type() is FilterTypes.BandReject:
            # z, p, k =
            # filter_in_use.load_z_p_k(z, p, k)

    def _precalc(self, n_max: int):
        data = {}
        outfile = open("PreCalc/gauss.json", "w")
        for i in range(1, n_max + 1):
            transfer_function = self._get_tf(i)
            w, mag, phase = transfer_function.bode()
            gd = -diff(unwrap(phase)) / diff(w)
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
