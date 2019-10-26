from FrontEnd.UIs.FilterConfigurations.ParameterLayout import ApproximationParameterLayout, DefaultSlider


class UIApproximation:
    def __init__(self,approximation):
        self.name = approximation.name
        self.parameter_list = []
        dict_of_features = approximation.dict
        for feature in dict_of_features:
            self.parameter_list.append(ApproximationParameterLayout(feature, DefaultSlider(dict_of_features[feature][0][0],
                                                                                  dict_of_features[feature][0][1],
                                                                                  dict_of_features[feature][1]), True))

