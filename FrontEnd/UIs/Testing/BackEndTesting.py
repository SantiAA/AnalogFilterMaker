import matplotlib
from matplotlib import patches

from BackEnd.Output.Dot import Dot, INFINITE
from BackEnd.Output.Square import Square
from BackEnd.Output.plots import GraphTypes, GraphValues
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
                        }), ApproximationTesting("Chebyshev", {
                                                    "MaxQcH" : [[0,57,False], 27],
                                                    "NChe" : [[0,5,True],2],
                                                    "Rango Desn" : [[0,100,False],50]}),
                         ]
            ,
            "High pass": [ApproximationTesting("Butterworth", {
                                                    "Max Q2": [[0, 100, False], 50],
                                                    "n2": [[0, 10, True], 5]})]
        }
        return self.dict, self.approx

    def validate_filter(self, filter):
        return True, "Error in sdasdadadasdasdasdasdasdasdas  "

    def get_template(self, filter):
        rect1 =  Square(Dot(-INFINITE, -INFINITE), Dot(-INFINITE, 300), Dot(50000, 300), Dot(50000,-INFINITE))
        rect2 = Square(Dot(300000, 20), Dot(300000, INFINITE), Dot(450000, INFINITE), Dot(450000,20))
        rect3 = Square(Dot(2000000, -INFINITE), Dot(2000000, 300), Dot(INFINITE, 300), Dot(INFINITE, -INFINITE))
        return [rect1, rect2, rect3]

    def get_graphs(self, filter, approximation):
        graph_dict = {}
        graph_dict[GraphTypes.Attenuation.value] = [[GraphValues([0,10,15,20,25,13000],[50,100,2000,3000,40000,25]), GraphValues([50,5000,50000,60000],[1000,1100,1500,1700])], ["freq", "module"]]
        graph_dict[GraphTypes.GroupDelay.value] = [[GraphValues([0,100,105,2000,2500],[500,1000,20000,30000,400000]), GraphValues([500,50000,504000,600500],[10050,14100,15800,17500])], ["freq", "module"]]
        graph_dict[GraphTypes.PolesZeros.value] = [[GraphValues([50,500,5000,50000], [10,100,1000,10000], True, False, "Zeros"), GraphValues([550,5050,50500,550000], [150,1500,10050,100500], True, True, "Poles")], ["Re", "Im"]]
        return graph_dict