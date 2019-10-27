from FrontEnd.UIs.FilterConfigurations.ParameterLayout import FilterParameterLayout, DefaultNumberEdit, DefaultSlider
from FrontEnd.UIs.Testing.UIApproximation import UIApproximation

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