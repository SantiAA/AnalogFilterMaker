from FrontEnd.UIs.FilterConfigurations.ParameterLayout import ParameterLayout, DefaultNumberEdit, DefaultSlider


class StopBandConfig:
    def __init__(self):
        self.name = "Stop Band"
        self.template_image = "FrontEnd/UIs/figs/filter_templates/stopbandtemplate.png"
        self.parameter_list = [ParameterLayout("Gain [dB]", DefaultNumberEdit(-10000,10000,2)),
                               ParameterLayout("Denorm [%]",  DefaultNumberEdit(0,100))]

