import copy

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from FrontEnd.UIs.FilterConfigurations.BandPassConfig import BandPassConfig
from FrontEnd.UIs.FilterConfigurations.HighPassConfig import HighPassConfig
from FrontEnd.UIs.FilterConfigurations.LowPassConfig import LowPassConfig
from FrontEnd.UIs.FilterConfigurations.StopBandConfig import StopBandConfig


class FirstStage(QMainWindow):

    def __init__(self, ui_manager):  # Conecta los componentes del .ui realizado en QT con el programa en python
        self.ui_manager = ui_manager
        self.filters = {
            "Low Pass" : LowPassConfig(),
            "High Pass": HighPassConfig(),
            "Band Pass": BandPassConfig(),
            "Stop Band": StopBandConfig()
        }


    def start(self):
        QMainWindow.__init__(self)
        loadUi('FrontEnd/UIs/firststageTest.ui', self)
        self.setWindowTitle("Filter Design Tool")
        for filter in self.filters:
            self.comboFilter.addItem(filter)
        self.update_filter_type()
        self.show()

        #self.graphButton.clicked.connect(self.graph)
        self.comboFilter.currentIndexChanged.connect(self.update_filter_type)
        #self.comboGraph.currentIndexChanged.connect(self.graph)
        self.graph_widget = self.graphWidget  # GraphWidget instance.

    def update_filter_type(self):
        for filters in self.filters.values():
            for parameters in filters.parameter_list:
                parameters.setParent(None)
        self.filter = self.filters[self.comboFilter.currentText()]
        self.graphPic.setPixmap(QPixmap(self.filter.template_image))

        self.clearLayout(self.configurationLayout)
        self.show()
        for parameter in self.filter.parameter_list:
            self.configurationLayout.addWidget(parameter)
        self.configurationLayout.addStretch(50)
        self.show()


    def graph(self):
        self.graph_widget.canvas.axes.clear()
        self.graph_widget.canvas.axes.set_title(self.comboGraph.currentText())
        self.graph_widget.canvas.axes.scatter([0,10,15,20,25],
                                         [40,50,60,90,120],
                                         color='b')
        self.graph_widget.canvas.axes.set_xscale('log')
        self.graph_widget.canvas.axes.grid(True, which="both")

        self.graph_widget.canvas.draw()  # Redraws

    def slider_changed(self):
        val = self.sliderRange.value()
        self.sliderValue.setText(str(val))

    def clearLayout(self, layout):
        # clear a layout and delete all widgets
        # aLayout is some QLayout for instance
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()









