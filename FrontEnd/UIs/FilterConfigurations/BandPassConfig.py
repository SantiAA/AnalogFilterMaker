from FrontEnd.UIs.FilterConfigurations.ParameterLayout import ParameterLayout, DefaultNumberEdit, DefaultSlider


class BandPassConfig:
    def __init__(self):
        self.name = "Band Pass"
        self.template_image = "FrontEnd/UIs/figs/filter_templates/bandpasstemplate.png"
        self.parameter_list = [ParameterLayout("Gain [dB]", DefaultNumberEdit(-10000, 10000, 2)),
                               ParameterLayout("Upper Attenuation Freq (Fa+) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Upper Passband Freq (Fp+) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Lower Attenuation Freq (Fa-) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Lower Passband Freq (Fp-) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Mid Freq (Fo) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Passband Atten. (Ap) [dB]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Stopband Atten. (Aa) [dB]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Denorm [%]", DefaultSlider(0, 100)),
                               ParameterLayout("Filter Order", DefaultSlider(0, 10))]

