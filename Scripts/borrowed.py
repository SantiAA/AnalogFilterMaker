""" Legendre Function for Analog Filters
    The main execution of the program calculates the normalized transfer function to match
    the normalized template given in the order of ap, aa and wa from the command-line arguments.
    Author: Lucas A. Kammann
"""

# python native modules
import sys

# third-party modules
from scipy import special
from scipy import signal

from numpy import polymul
from numpy import polyadd
from numpy import polyint
from numpy import polyval
from numpy import polysub
from numpy import poly1d
from numpy import sqrt
from numpy import log10

import json

from matplotlib import pyplot


def calculate_legendre(
        transfer_calculator: callable,
        *args):
    n_min = 1
    n_max = 30
    for n in range(n_min, n_max + 1):
        zpk = transfer_calculator(n, ap, *args)
        transfer = zpk.to_tf()



def verifies_filter_template(transfer, ap: float, aa: float, wa: float) -> bool:
    """
    Returns whether the normalized transfer function verifies or not the given normalized template.
    :param transfer: TransferFunction from the Scipy Signal package
    :param ap: Maximum pass band attenuation
    :param aa: Minimum stop band attenuation
    :param wa: Normalized stop band rad/sec frequency
    :return: boolean False or True
    """
    w, h = signal.freqresp(transfer, [1, wa])
    h = 20 * log10(abs(h))
    return h[0] >= -ap and h[1] <= -aa


##############################
# Legendre Package Functions #
##############################
def legendre_approximation(n: int, ap: float):
    """
    Returns the normalized transfer function of the Legendre Approximation
    :param n: Order of the legendre polynomial
    :param ap: Maximum attenuation of the pass band in dB
    :return: The lti transfer function from scipy signals
    """
    poly = legendre_approximation_denominator(n, ap)
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


def legendre_approximation_denominator(n: int, ap: float):
    """
    :param n: Legendre approximation order
    :param ap: Maximum band pass attenuation
    :return: The Legendre Approximation Denominator
    """
    epsilon = legendre_epsilon(ap) ** 2
    ln = legendre_odd_integrated_polynomial(n) if (n % 2) else legendre_even_integrated_polynomial(n)
    ln = epsilon * ln
    return polyadd(poly1d([1]), ln)


def legendre_epsilon(ap: float):
    """
    Returns the legendre epsilon parameter with the given ap in dB
    :param ap: Pass band maximum attenuation in dB
    :return: Epsilon legendre parameter
    """
    return sqrt(10 ** (ap / 10) - 1)


def legendre_even_integrated_polynomial(n: int):
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
        new_poly = bi * legendre_polynomial(i)
        poly = polyadd(poly, new_poly)

    poly = polymul(poly, poly)
    poly = polymul(poly, poly1d([1, 1]))

    # Calculate the indefinite integration and upper/lower limits
    poly = polyint(poly)
    upper = poly1d([2, 0, -1])
    lower = poly1d([-1])

    # Using barrow and returning the result!
    return polysub(polyval(poly, upper), polyval(poly, lower))


def legendre_odd_integrated_polynomial(n: int):
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


def legendre_polynomial(n: int):
    """
    Returns the polynomial of n-th order from Legendre.
    :param n: Order of the polynomial
    :return: Pn(x) expressed as poly1d from numpy
    """
    if n < 0:
        raise ValueError("LegendrePolynomial received a negative order!")
    return special.legendre(n)


if __name__ == "__main__":
    ap = float(sys.argv[1])
    aa = float(sys.argv[2])
    wa = float(sys.argv[3])

    transfer = match_filter_template(legendre_approximation, ap, aa, wa)
    w, module, phase = transfer.bode(n=1000)

    pyplot.figure()
    pyplot.semilogx(w, module)
    pyplot.show()

    input("Press any key to exit the program...")