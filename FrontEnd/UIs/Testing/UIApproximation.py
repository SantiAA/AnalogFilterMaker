from FrontEnd.UIs.FilterConfigurations.ParameterLayout import ApproximationParameterLayout, DefaultSlider


class UIApproximation:
    def __init__(self,approximation):
        self.name = approximation.name
        self.parameter_list = []
        dict_of_features = approximation.dict
        for feature in dict_of_features:
            self.parameter_list.append(ApproximationParameterLayout(feature, DefaultSlider(dict_of_features[feature][0][0],
                                                                                  dict_of_features[feature][0][1],
                                                                                  dict_of_features[feature][1]), dict_of_features[feature][0][2]))

    def make_approx_dict(self):
        dict = {}
        for parameter in self.parameter_list:
            if not parameter.toggleable or not parameter.auto:
                dict[parameter.name] = [[parameter.widget.min, parameter.widget.max, parameter.toggleable], parameter.widget.slider.value()]
            else:
                dict[parameter.name] = [[parameter.widget.min, parameter.widget.max, parameter.toggleable],
                                      None]
        return dict
