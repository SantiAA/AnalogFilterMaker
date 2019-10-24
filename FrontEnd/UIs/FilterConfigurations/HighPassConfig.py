from FrontEnd.UIs.FilterConfigurations.ParameterLayout import ParameterLayout, DefaultNumberEdit, DefaultSlider


class HighPassConfig:
    def __init__(self):
        self.name = "High Pass"
        self.template_image = "FrontEnd/UIs/figs/filter_templates/highpasstemplate.png"
        self.parameter_list = [ParameterLayout("Gain [dB]", DefaultNumberEdit(-10000,10000,2)),
                               ParameterLayout("Denorm [%]",  DefaultNumberEdit(0,100))]

