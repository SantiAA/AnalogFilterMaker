import copy

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from FrontEnd.UIControl.Approximations import ApproximationNames, Approximations
from FrontEnd.UIs.FilterConfigurations.BandPassConfig import BandPassConfig
from FrontEnd.UIs.FilterConfigurations.HighPassConfig import HighPassConfig
from FrontEnd.UIs.FilterConfigurations.LowPassConfig import LowPassConfig
from FrontEnd.UIs.FilterConfigurations.StopBandConfig import StopBandConfig


class FirstStage(QMainWindow):

    def __init__(self, ui_manager):
        self.graph_widget = None
        self.ui_manager = ui_manager
        self.filters = {
            "Low Pass": LowPassConfig(),
            "High Pass": HighPassConfig(),
            "Band Pass": BandPassConfig(),
            "Stop Band": StopBandConfig()
        }
        self.activeApproximations = []

    def start(self):
        """
        Actions to perform when the window is shown.
        """
        QMainWindow.__init__(self)
        loadUi('FrontEnd/UIs/firststageTest.ui', self)
        self.setWindowTitle("Filter Design Tool")
        for filter in self.filters:
            self.comboFilter.addItem(filter)
        self.update_filter_type()
        self.show()
        self.maxQSlider.valueChanged.connect(self.maxq_slider_changed)
        self.filterOrderSlider.valueChanged.connect(self.filter_order_slider_changed)
        self.addApproxButton.clicked.connect(self.add_approx)
        self.removeApproxButton.clicked.connect(self.remove_approx)
        self.comboFilter.currentIndexChanged.connect(self.update_filter_type)
        self.graph_widget = self.graphWidget
        for approx in ApproximationNames:
            self.approxCombo.addItem(approx.value)

    def update_filter_type(self):
        """
        Changes the filter template image and requirements whenever the current selected filter type is changed.
        """
        for filters in self.filters.values():  # Clearing requirement widgets
            for parameters in filters.parameter_list:
                parameters.setParent(None)

        self.filter = self.filters[self.comboFilter.currentText()]
        self.graphPic.setPixmap(QPixmap(self.filter.template_image))  # filter template image

        self.clear_layout(self.configurationLayout)
        self.show()
        for parameter in self.filter.parameter_list:  # Refilling requierement widgets
            self.configurationLayout.addWidget(parameter)
        self.configurationLayout.addStretch(50)  # space
        self.show()

    def remove_approx(self):
        """
        Removes graphs and text when an active approximation is removed by the user.
        """
        if self.activeApproxsCombo.currentText() is not None or self.activeApproxsCombo.currentText() != "":
            for approx in self.activeApproximations:
                if approx.string == self.activeApproxsCombo.currentText():
                    self.activeApproximations.remove(approx)
            self.__update_active_approx_combo__()

    def add_approx(self):
        """
        Appends user selected approximation to active approximations and applies it to the filter.
        """
        self.activeApproximations.append(
            Approximations(self.approxCombo.currentText(), self.maxQSlider.value(), self.filterOrderSlider.value()))
        self.__update_active_approx_combo__()


        #test
        self.graph_widget.canvas.axes.clear()
        self.graph_widget.canvas.axes.set_title(self.comboGraph.currentText())
        self.graph_widget.canvas.axes.scatter([0, 10, 15, 20, 25],
                                              [40, 50, 60, 90, 120],
                                              color='b')
        self.graph_widget.canvas.axes.set_xscale('log')
        self.graph_widget.canvas.axes.grid(True, which="both")

        self.graph_widget.canvas.draw()  # Redraws

    def __update_active_approx_combo__(self):
        self.activeApproxsCombo.clear()
        for approx in self.activeApproximations:
            self.activeApproxsCombo.addItem(approx.string)

    def maxq_slider_changed(self):
        """
        Relates slider with its assigned label
        """
        val = self.maxQSlider.value()
        self.maxQSliderLabel.setText(str(val))

    def filter_order_slider_changed(self):
        """
        Relates slider with its assigned label
        """
        val = self.filterOrderSlider.value()
        self.filterOrderSliderLabel.setText(str(val))

    def clear_layout(self, layout):
        """
        Clears widgets from a layout.
        :param layout: layout to clear
        """
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
