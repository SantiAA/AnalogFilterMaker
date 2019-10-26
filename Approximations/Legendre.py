"""
Approximation base class
"""

# python native modules

# third-party modules
from sympy import *
from scipy import signal
from scipy import special
import json

from numpy import polymul
from numpy import polyadd
from numpy import polyint
from numpy import polyval
from numpy import polysub
from numpy import poly1d
from numpy import sqrt


# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class Legendre(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Legendre")
        self.application = [FilterTypes.HighPass, FilterTypes.LowPass, FilterTypes.BandPass, FilterTypes.BandReject]
        self.information = {}

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Legendre is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter, n_max=20):
        """ Be careful this function doesn't care of Q !!! """
        if filter_in_use.get_type() is FilterTypes.LowPass:
            """ If the approximation support the filter I continue """
            """ I get the order and the frequency for the -3dB point"""
            # self.information[TemplateInfo.fp], self.information[TemplateInfo.fa],
            # self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa]
            #
            """ Now we limit the order of the filter """
            if n > n_max:
                n = n_max
            """ After getting the order I get the zeros, poles and gain of the filter """
            # filter_in_use.load_z_p_k(z, p, k)
            # filter_in_use.load_order(n)

        elif filter_in_use.get_type() is FilterTypes.HighPass:
            n, w = signal.buttord(self.information[TemplateInfo.fp], self.information[TemplateInfo.fa],
                                  self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

            z, p, k = signal.butter(n, w, analog=True, output='zpk')  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
            filter_in_use.load_order(n)

        elif filter_in_use.get_type() is FilterTypes.BandPass:
            wp = [self.information[TemplateInfo.fp__], self.information[TemplateInfo.fp_]]
            wa = [self.information[TemplateInfo.fa__], self.information[TemplateInfo.fa_]]
            n, w = signal.buttord(wp, wa, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

            z, p, k = signal.butter(n, w, analog=True, output='zpk', btype="band")  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
            filter_in_use.load_order(n)

        elif filter_in_use.get_type() is FilterTypes.BandReject:
            wp = [self.information[TemplateInfo.fp__], self.information[TemplateInfo.fp_]]
            wa = [self.information[TemplateInfo.fa__], self.information[TemplateInfo.fa_]]
            n, w = signal.buttord(wp, wa, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

            z, p, k = signal.butter(n, w, analog=True, output='zpk', btype="stop")  # Desnormalizado
            filter_in_use.load_z_p_k(z, p, k)
            filter_in_use.load_order(n)

#    def _precalc(self, n_max : int, ap: float):
#        data = {}
#        outfile = open("legendre.json", "w")
#        for i in range(1, n_max + 1):
#            transfer_function = legendre_approximation(i, ap)
#            w, mag, phase = transfer_function.bode()
#            data[str(i)] = {}
#            data[str(i)] = {"w": w.tolist(), "|H(jw)[dB]|": mag.tolist()}
#        json.dump(data, outfile, indent=4)

    def _get_tf(self, n: int, ap: float):
        """
        Returns the normalized transfer function of the Legendre Approximation
        :param n: Order of the legendre polynomial
        :param ap: Maximum attenuation of the pass band in dB
        :return: The lti transfer function from scipy signals
        """
        poly = self._den(n, ap)
        gain = sqrt(polyval(poly, 0))
        poles = [
            complex(
                pole.real if abs(pole.real) > 1e-10 else 0,
                pole.imag if abs(pole.imag) > 1e-10 else 0
            )
            for pole in 1j * poly.roots if pole.real < 0
            ]
        for pole in poles:
            gain *= pole
        return signal.lti([], poles, gain)

    def _den(self, n: int, ap: float):
        """
        :param n: Legendre approximation order
        :param ap: Maximum band pass attenuation
        :return: The Legendre Approximation Denominator
        """
        epsilon = self._epsilon(ap) ** 2
        ln = self._odd_poly(n) if (n % 2) else self._even_poly
        ln = epsilon * ln
        return polyadd(poly1d([1]), ln)


    def _epsilon(self, ap: float):
        """
        Returns the legendre epsilon parameter with the given ap in dB
        :param ap: Pass band maximum attenuation in dB
        :return: Epsilon legendre parameter
        """
        return sqrt(10 ** (ap / 10) - 1)


    def _even_poly(self, n: int):
        """
        Returns the integrated Legendre polynomial when the order is even.
        :param n: Even order of the polynomial required
        :return: Ln(x) expressed as poly1d from numpy
        """
        if n % 2:
            raise ValueError("Expecting an even n value for the Legendre polynomial")

        # First, calculate the integration polynomial as a sum of legendre polynomials
        k = n // 2 - 1
        b0 = 1 / sqrt((k + 1)*(k + 2))
        poly = poly1d([b0 if (k % 2) == 0 else 0])

        for i in range(1, k + 1):
            if ((k % 2) == 1 and (i % 2) == 0) or ((k % 2) == 0 and (i % 2) == 1):
                continue
            bi = b0 * (2*i + 1)
            new_poly = bi * self._polynomial(i)
            poly = polyadd(poly, new_poly)

        poly = polymul(poly, poly)
        poly = polymul(poly, poly1d([1, 1]))

        # Calculate the indefinite integration and upper/lower limits
        poly = polyint(poly)
        upper = poly1d([2, 0, -1])
        lower = poly1d([-1])

        # Using barrow and returning the result!
        return polysub(polyval(poly, upper), polyval(poly, lower))


    def _odd_poly(self, n: int):
        """
        Returns the integrated Legendre polynomial when the order is odd.
        :param n: Odd order of the polynomial required
        :return: Ln(x) expressed as poly1d from numpy
        """
        if (n % 2) == 0:
            raise ValueError("Expecting an odd n value for the Legendre polynomial")

        # First, calculate the integration polynomial as a sum of legendre polynomials
        k = (n - 1) // 2
        a0 = 1 / (sqrt(2) * (k + 1))
        poly = poly1d([a0])

        for i in range(1, k + 1):
            ai = a0 * (2*i + 1)
            poli = legendre_polynomial(i)
            new_poly = ai * poli
            poly = polyadd(poly, new_poly)

        poly = polymul(poly, poly)


        # Calculate the indefinite integration and upper/lower limits
        poly = polyint(poly)
        upper = poly1d([2, 0, -1])
        lower = poly1d([-1])

        # Using barrow and returning the result!
        return polysub(polyval(poly, upper), polyval(poly, lower))

    def _polynomial(n: int):
        """
        Returns the polynomial of n-th order from Legendre.
        :param n: Order of the polynomial
        :return: Pn(x) expressed as poly1d from numpy
        """
        if n < 0:
            raise ValueError("LegendrePolynomial received a negative order!")
        return special.legendre(n)

