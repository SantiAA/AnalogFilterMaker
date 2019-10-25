from FrontEnd.UIs.FilterConfigurations.ParameterLayout import ParameterLayout, DefaultNumberEdit, DefaultSlider


class HighPassConfig:
    def __init__(self):
        self.name = "High Pass"
        self.template_image = "FrontEnd/UIs/figs/filter_templates/highpasstemplate.png"
        self.parameter_list = [ParameterLayout("Gain [dB]", DefaultNumberEdit(-10000, 10000, 2)),
                               ParameterLayout("Attenuation Freq (Fa) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Passband Freq (Fp) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Passband Atten. (Ap) [dB]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Stopband Atten. (Aa) [dB]", DefaultNumberEdit(0, 10000000, 0)),
                               ParameterLayout("Denorm [%]", DefaultSlider(0, 100)),
                               ParameterLayout("Filter Order", DefaultSlider(0, 10))]

