from FrontEnd.UIs.FilterConfigurations.ParameterLayout import FilterParameterLayout, DefaultNumberEdit, DefaultSlider
from FrontEnd.UIs.Testing.UIApproximation import UIApproximation


class LowPassConfig:
    def __init__(self):
        self.name = "Low Pass"
        self.template_image = "FrontEnd/UIs/figs/filter_templates/lowpasstemplate.png"
        self.parameter_list = [FilterParameterLayout("Gain [dB]", DefaultNumberEdit(-10000, 10000, 2)),
                               FilterParameterLayout("Attenuation Freq (Fa) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               FilterParameterLayout("Passband Freq (Fp) [Hz]", DefaultNumberEdit(0, 10000000, 0)),
                               FilterParameterLayout("Passband Atten. (Ap) [dB]", DefaultNumberEdit(0, 10000000, 0)),
                               FilterParameterLayout("Stopband Atten. (Aa) [dB]", DefaultNumberEdit(0, 10000000, 0)),
                               FilterParameterLayout("Denorm [%]", DefaultSlider(0, 100))
                               ]


class Config:
    def __init__(self, name, dict_of_features, approximation_list_received):
        self.name = name
        self.dict_of_features = dict_of_features
        self.template_image = "FrontEnd/UIs/figs/filter_templates/" + self.name.replace(" ", "").lower() + "template" \
                                                                                                           ".png"
        self.parameter_list = []
        for feature in dict_of_features:
            self.parameter_list.append(FilterParameterLayout(feature, DefaultNumberEdit(dict_of_features[feature][0][0],
                                                                                        dict_of_features[feature][0][1], 2,
                                                                                        dict_of_features[feature][1])))
        self.approximation_list = []
        for approximation in approximation_list_received:
            self.approximation_list.append(UIApproximation(approximation))

    def make_feature_dictionary(self):
        dict = {}
        for parameter in self.parameter_list:
            dict[parameter.name] = [[parameter.widget.min, parameter.widget.max], parameter.widget.value()]
        return dict