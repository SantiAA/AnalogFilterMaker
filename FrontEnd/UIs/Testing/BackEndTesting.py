import matplotlib
from matplotlib import patches

from FrontEnd.UIs.Testing.ApproximationTesting import ApproximationTesting


class BackEndTesting:
    def __init__(self):
        self.dict = {}
        self.approx = {}

    def get_util(self):
        self.dict = {
            "Low pass": {"Gain [dB]": [[0, 100], 50],
                         "Attenuation [dB]": [[10, 20], 15]},
            "High pass": {"GaAAin [dB]": [[0, 1000], 500],
                          "Attenuation222 [dB]": [[100, 250], 150]}
        }
        self.approx = {
            "Low pass": [ApproximationTesting("Butterworth", {
                                                    "Max Q": [[0, 100, False], 50],
                                                    "n": [[0, 10, True], 5]
                        }), ApproximationTesting("Chebushev", {
                                                    "MaxQcH" : [[0,57,False], 27],
                                                    "nche" : [[0,5,True],2]}) ]
            ,
            "High pass": [ApproximationTesting("Butterworth", {
                                                    "Max Q2": [[0, 100, False], 50],
                                                    "n2": [[0, 10, True], 5]})]
        }
        return self.dict, self.approx

    def validate_filter(self, filter):
        return True, "Error in sdasdadadasdasdasdasdasdasdas  "

    def get_template(self, filter):
        rect1 =  patches.Rectangle((0,0), 1000, 1000)
        return [rect1, patches.Rectangle((10000,5000), 100000, 100000)]
