import webbrowser
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from FrontEnd.UIControl.Approximations import ApproximationNames, Approximations
from FrontEnd.UIs.Testing.BackEndTesting import BackEndTesting
from FrontEnd.UIs.FilterConfigurations.Config import Config


class FirstStage(QMainWindow):

    def __init__(self, ui_manager):
        self.graph_widget = None
        self.ui_manager = ui_manager
        self.a = 0
        self.filters = {}
        self.backend = BackEndTesting()
        self.filters_received, self.approximations_received = self.backend.get_util()
        '''
        self.window_configuration = {
            "active_filter": "",
            "n_of_requirements": 0,
            "requirement_current_values": []
        }
        '''
        self.activeApproximations = []

    def start(self):
        """
        Actions to perform when the window is shown.
        """
        QMainWindow.__init__(self)
        loadUi('FrontEnd/UIs/firststageTest2.ui', self)
        self.setWindowTitle("Filter Design Tool")
        self.comboFilter.clear()
        for filter in self.filters_received:
            self.comboFilter.addItem(filter)
            self.filters[filter] = Config(filter, self.filters_received[filter], self.approximations_received[filter])

        self.update_filter_type()
        self.show()
        self.addApproxButton.clicked.connect(self.add_approx)
        self.removeApproxButton.clicked.connect(self.remove_approx)
        self.filterTypeLabel.clicked.connect(self.filter_type_label_clicked)
        self.approximationLabel.clicked.connect(self.approximation_label_clicked)
        self.parametersLabels.clicked.connect(self.parameters_label_clicked)
        self.comboFilter.currentIndexChanged.connect(self.update_filter_type)
        self.approxCombo.currentIndexChanged.connect(self.update_approximation)
        self.plotTemplateButton.clicked.connect(self.plot_template_button_clicked)
        self.graph_widget = self.graphWidget
        self.graph_widget.canvas.axes.autoscale(True)

    '''
    def load_current_state(self, configuration_dict):

        index = self.comboFilter.findText(configuration_dict["active_filter"], QtCore.Qt.MatchFixedString)
        self.comboFilter.setCurrentIndex(index)
    
    def save_current_state(self):
        self.window_configuration["active_filter"] = self.comboFilter.currentText()
        self.window_configuration["n_of_requirements"] = len(
            self.filters[self.comboFilter.currentText()].parameter_list)
        self.window_configuration["requirement_current_values"] = [0, 0, 0, 0]
        self.ui_manager.program_state["active_window_configuration"] = self.window_configuration
        Save = self.ui_manager.program_state  # Saves the desired class AND a chosen attribute
        pickle.dump(Save, open("Save File", "wb"))  # Creates the file and puts the data into the file
        '''

    def plot_template_button_clicked(self):
        self.filter = self.filters[self.comboFilter.currentText()]
        dict = self.filter.make_feature_dictionary()
        validated, error_string =  self.backend.validate_filter([self.filter.name, dict])
        if validated:
            squares = self.backend.get_template([self.filter.name, dict])
            for square in squares:
                self.plot_rectangle(square)
                self.show()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(error_string)
            msg.setWindowTitle("Error")
            msg.exec_()
        i =0
        '''
        me = pickle.load(open("Save File", "rb"))  # Loads the file
        uu = 0  # Prints the stats out to verify the load has successfully happened'''

    def approximation_label_clicked(self):
        webbrowser.open('http://dsp-book.narod.ru/HFTSP/8579ch12.pdf')

    def parameters_label_clicked(self):
        webbrowser.open('https://electronicspani.com/electric-filter-types-of-filter/')

    def filter_type_label_clicked(self):
        webbrowser.open('https://www.allaboutcircuits.com/technical-articles/an-introduction-to-filters/')

    def update_filter_type(self):
        """
        Changes the filter template image and requirements whenever the current selected filter type is changed.
        """

        for filters in self.filters.values():  # Clearing requirement widgets
            for parameters in filters.parameter_list:
                parameters.setParent(None)
            for approx in filters.approximation_list:
                for parameter in approx.parameter_list:
                    parameter.setParent(None)

        self.filter = self.filters[self.comboFilter.currentText()]
        self.approxCombo.clear()

        for approximation in self.filter.approximation_list:
            self.approxCombo.addItem(approximation.name)

        self.update_approximation()
        self.graphPic.setPixmap(QPixmap(self.filter.template_image))  # filter template image

        self.clear_layout(self.configurationLayout)
        self.show()
        for parameter in self.filter.parameter_list:  # Refilling requierement widgets
            self.configurationLayout.addWidget(parameter)
        self.configurationLayout.addStretch(50)  # space
        self.show()
        # self.save_current_state()

    def update_approximation(self):
        for filters in self.filters.values():  # Clearing requirement widgets
            for approx in filters.approximation_list:
                for parameter in approx.parameter_list:
                    parameter.setParent(None)
        self.filter = self.filters[self.comboFilter.currentText()]
        self.clear_layout(self.approxConfigurationLayout)
        self.show()

        for approximation in self.filter.approximation_list:
            if approximation.name == self.approxCombo.currentText():
                for parameter in approximation.parameter_list:
                    self.approxConfigurationLayout.addWidget(parameter)
        self.configurationLayout.addStretch(2)  # space
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

        # test
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




    def clear_layout(self, layout):
        """
        Clears widgets from a layout.
        :param layout: layout to clear
        """
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def plot_rectangle(self, square):
        self.graph_widget.canvas.axes.set_title(self.comboGraph.currentText())
        self.graph_widget.canvas.axes.set_xscale('log')
        self.graph_widget.canvas.axes.grid(True, which="both")


        self.graph_widget.canvas.axes.add_patch(square)
        self.graph_widget.canvas.draw()  # Redraws