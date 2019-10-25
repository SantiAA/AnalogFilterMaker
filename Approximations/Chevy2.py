# python native modules

# third-party modules
from scipy import signal

# AFM project modules
from Approximations.Approx import Approximation
from Filters.Filters import FilterTypes
from Filters.Filters import TemplateInfo
from Filters.Filters import Filter


class ChebyII(Approximation):

    def __init__(self):
        Approximation.__init__(self, "Cheby II")
        self.application = [FilterTypes.HighPass, FilterTypes.LowPass, FilterTypes.BandPass, FilterTypes.BandReject]
        self.information = {}

    def load_information(self, filter_in_use: Filter):

        if filter_in_use.get_type() not in self.application:
            print("Something done wrong, Cheby II is not valid for ", filter_in_use.get_type())
            return False

        specs = filter_in_use.get_requirements()
        for each in specs:
            self.information[each] = filter_in_use.get_req_value(each)
        return True

    def calculate(self, filter_in_use: Filter, n_max=20):
        """ Be careful this function doesn't care of Q !!! """
        w = None
        n = 0
        type_ = ""
        if filter_in_use.get_type() is FilterTypes.LowPass:
            """ If the approximation support the filter I continue """
            type_ = "low"
            """ Then using cheb2ord I get the order and the frequency for the -3dB point"""
            n, w = signal.cheb2ord(self.information[TemplateInfo.fp], self.information[TemplateInfo.fa],
                                   self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                   analog=True)
            """ Now we limit the order of the filter """
            if n > n_max:
                n = n_max

        elif filter_in_use.get_type() is FilterTypes.HighPass:
            n, w = signal.cheb2ord(self.information[TemplateInfo.fp], self.information[TemplateInfo.fa],
                                  self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

        elif filter_in_use.get_type() is FilterTypes.BandPass:
            wp = [self.information[TemplateInfo.fp__], self.information[TemplateInfo.fp_]]
            wa = [self.information[TemplateInfo.fa__], self.information[TemplateInfo.fa_]]
            n, w = signal.cheb2ord(wp, wa, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

        elif filter_in_use.get_type() is FilterTypes.BandReject:
            wp = [self.information[TemplateInfo.fp__], self.information[TemplateInfo.fp_]]
            wa = [self.information[TemplateInfo.fa__], self.information[TemplateInfo.fa_]]
            n, w = signal.cheb2ord(wp, wa, self.information[TemplateInfo.Ap], self.information[TemplateInfo.Aa],
                                  analog=True)

            if n > n_max:
                n = n_max

        """ After getting the order I get the zeros, poles and gain of the filter """
        z, p, k = signal.cheby2(n, w, self.information[TemplateInfo.Aa], analog=True, output='zpk',
                                btype=type_)  # Desnormalizado
        filter_in_use.load_z_p_k(z, p, k)
        filter_in_use.load_order(n)
