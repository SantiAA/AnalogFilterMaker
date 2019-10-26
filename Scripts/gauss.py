# third-party modules
from scipy import signal
from math import factorial
from numpy import unwrap
from numpy import diff
from numpy import log
from numpy import divide
import json


def calculate_gauss(n_max: int):
    data = {}
    outfile = open("gauss.json", "w")
    for i in range(1, n_max + 1):
        transfer_function = gauss_approximation(i)
        w, mag, phase = transfer_function.bode()
        gd = -diff(unwrap(phase)) / diff(w)
        gd = divide(gd, gd[0])
        data[str(i)] = {}
        data[str(i)] = {"w": w.tolist(), "|H(jw)[dB]|": mag.tolist(), "Group delay": gd.tolist()}
    json.dump(data, outfile, indent=4)
    outfile.close()


###########################
# Gauss Package Functions #
###########################
def gauss_approximation(n: int):
    """
    Returns the normalized transfer function of the Gauss Approximation
    :param n: Order of the gauss polynomial
    :return: Scipy signal transfer function
    """
    num = [1.]
    den = gauss_approximation_denominator(n)
    transfer_function = signal.TransferFunction(num, den)
    return transfer_function


def gauss_approximation_denominator(n: int):
    """
    :param n: Gauss approximation order
    :return: The Gauss Approximation Denominator
    """
    den = []
    gamma = log(2)
    for k in range(n, 1, -1):
        den.append(gamma**k/factorial(k))
        den.append(0)
    den.append(1.)
    return den


if __name__ == "__main__":
    calculate_gauss(20)
